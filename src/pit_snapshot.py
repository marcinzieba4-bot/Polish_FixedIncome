"""Build a point-in-time snapshot directory from the previous one plus a day spec.

Usage: python src/pit_snapshot.py PREV_DIR OUT_DIR DAY_SPEC.json RAW_DIR
  RAW_DIR holds bondspot_YYYYMMDD.json (fetch_bondspot.py), hist.json (fetch_history.py, may run past the
  cut-off: it is truncated here) and core_YYYYMMDD.json (fetch_core_asof.py for the cut-off).
  DAY_SPEC holds the hand-collected, dated inputs: wibor, polstr, irs, fra, euribor, pribor, bubor, fx, fpc,
  pap, mof_ops_add, policy, facts (see README "Point-in-time reports").

Point-in-time rules applied here:
  * BondSpot pages show the CURRENT TBSP level -> dropped (bondspot and history);
  * history and core series are cut at the market cut-off; SOFR (published T+1 at 08:00 New York time, i.e.
    after the Warsaw pre-open on the report date) is cut at the day before the cut-off;
  * repo funding = nominal-weighted special repo starting within one day and lasting <= 3 days, from the
    BondSpot session of the cut-off date.
"""
import datetime as dt
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATIC = ["bonds_static.json", "index_portfolios.json", "mof_operations_2025H2.json", "floaters.json", "market_inputs.json",
          "core_inputs.json", "quasi_inputs.json", "facts.json"]


def dmy(d):
    d = dt.date.fromisoformat(d) if isinstance(d, str) else d
    return f"{d.day} {d:%b %Y}"


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def dump(p, o, indent=1):
    pathlib.Path(p).write_text(json.dumps(o, indent=indent, ensure_ascii=False))


def repo_stats(repo):
    def start_len(t):
        a, b = (int(x) for x in t.split("/"))
        return a, b - a
    spec = [(r, *start_len(r["term"])) for r in repo if not r["name"].startswith("GC")]
    gc = [r for r in repo if r["name"].startswith("GC")]
    short = [r for r, s, n in spec if s <= 1 and n <= 3]
    rule = "special repo starting within one day, <= 3 days"
    if not short:  # e.g. a Friday with only forward-starting trades: use the nearest start
        s0 = min((s for _, s, _ in spec), default=None)
        short = [r for r, s, n in spec if s == s0 and n <= 3] if s0 is not None else []
        rule = f"nearest-start special repo (start T+{s0})"
        if not short and s0 is not None:  # e.g. Easter, thin days: only longer trades at the nearest start
            n0 = min(n for _, s, n in spec if s == s0)
            short = [r for r, s, n in spec if s == s0 and n == n0]
            rule = f"nearest-start, shortest special repo (start T+{s0}, {n0} days; no trade of <= 3 days)"
    w = lambda rs: sum(r["avg"] * r["nominal_mln"] for r in rs) / sum(r["nominal_mln"] for r in rs) if rs else None
    term = [r["avg"] for r, s, n in spec if n > 3]
    return dict(funding=w(short), rule=rule, n_short=len(short), gc=w(gc), gc_terms=sorted({r["term"] for r in gc}),
                term_lo=min(term) if term else None, term_hi=max(term) if term else None)


def main(prev, out, spec_path, raw):
    prev, out, raw = pathlib.Path(prev), pathlib.Path(out), pathlib.Path(raw)
    S = load(spec_path)
    C, R, I = S["market_cutoff"], S["report_date"], S["info_cutoff"]
    Cs = C.replace("-", "")
    out.mkdir(parents=True, exist_ok=True)
    for f in STATIC:
        shutil.copy(prev / f, out / f)
    if S.get("index_portfolios"):  # periodic index change took effect since the previous snapshot
        shutil.copy(S["index_portfolios"], out / "index_portfolios.json")
    if S.get("bonds_static_add"):  # new fixed-rate line, first seen in the BondSpot fixing of the cut-off
        BS = load(out / "bonds_static.json")
        have = {b["ticker"] for b in BS["bonds"]}
        new = [b for b in S["bonds_static_add"]["bonds"] if b["ticker"] not in have]
        BS["bonds"] = sorted(BS["bonds"] + new, key=lambda b: b["maturity"])
        BS["_source"] += " " + S["bonds_static_add"]["note"]
        dump(out / "bonds_static.json", BS)

    # 1) BondSpot close of C, TBSP level dropped
    B = load(raw / f"bondspot_{Cs}.json")
    assert B["date"] == C and B["quotes_date"] == C, (B["date"], B["quotes_date"])
    B["tbsp_index"] = None
    B["_note"] = "tbsp_index removed: BondSpot fixing page shows the CURRENT index level regardless of date (look-ahead)"
    dump(out / f"bondspot_{Cs}.json", B)

    # 2) fixing history <= C, TBSP level dropped
    H = {d: {k: (None if k == "_tbsp" else v) for k, v in row.items()} for d, row in load(raw / "hist.json").items() if d <= C}
    assert max(H) == C, max(H)
    (out / "fixing_history.json").write_text(json.dumps(dict(sorted(H.items())), indent=0))

    # 3) core curves <= C, SOFR < C, PAP block from the spec
    K = load(raw / f"core_{Cs}.json")
    assert K["cutoff"] == C
    K["sofr"] = {d: v for d, v in K["sofr"].items() if d < C}
    K["pap"] = S["pap"]
    dump(out / "core_rates.json", K)
    ust = K["ust"][max(d for d in K["ust"] if d <= C)]

    # 4) market inputs
    M = load(out / "market_inputs.json")
    M["asof"] = C
    M["policy"].update(S.get("policy", {}))
    w = S["wibor"]
    rp = repo_stats(B["repo"])
    mm = M["money_market"]
    mm.update(wibor_1m=w["1m"], wibor_3m=w["3m"], wibor_6m=w["6m"], wibor_1y=w["1y"], wibor_on=w["on"],
              overnight_label=f"WIBOR O/N {w['on']:.2f}", funding_rate=round(rp["funding"], 3), repo_special_on=round(rp["funding"], 3),
              repo_gc=round(rp["gc"], 3) if rp["gc"] else None)
    lab = f"special {rp['funding']:.2f}"
    if rp["term_lo"] is not None:
        lab += f", term {rp['term_lo']:.2f}-{rp['term_hi']:.2f}" if rp["term_hi"] != rp["term_lo"] else f", term {rp['term_lo']:.2f}"
    lab += f", GC {rp['gc']:.2f}" if rp["gc"] else ", no GC trade"
    mm["repo_label"] = lab
    mm["source"] = (f"WIBOR fixings of {dmy(C)} (GPW Benchmark delayed data); repo from the Treasury BondSpot Poland session of {dmy(C)}. "
                    f"Funding = nominal-weighted {rp['rule']} ({rp['funding']:.2f}%).")
    irs = S["irs"]
    M["irs"].update(pillars={k: v for k, v in irs["pillars"].items() if v is not None}, asof=f"{dmy(C)} close",
                    source=(f"PLN IRS vs 6M WIBOR at the {dmy(C)} close: {irs['src_label']} (table headed {irs['header']}; only the {dmy(C)} levels are used). "
                            f"{irs.get('side_note', 'Bid side, so roughly 1-2bp below mid.')} {irs.get('missing_note', '')} PCHIP interpolation through 6M WIBOR and the pillars; beyond 10Y extrapolated.").replace("  ", " "),
                    short_source=f"PLN IRS at the {dmy(C)} close ({irs.get('short', 'LSEG bid via Erste')}), WIBOR fixings {dmy(C)}")
    sub = [f for f in B["fixing"] if f["ticker"][:2] in ("OK", "PS", "DS") and (dt.date(2000 + int(f["ticker"][4:6]), int(f["ticker"][2:4]), 25) - dt.date.fromisoformat(C)).days < 365 and f["fix_yld"]]
    anchor = sum(f["fix_yld"] for f in sub) / len(sub)
    M["curve"]["front_anchor"]["rate"] = round(anchor, 3)
    M["curve"]["source"] = (f"NSS zero curve fitted to BondSpot closing fixings of {dmy(C)}; front end anchored at a 3M zero of {anchor:.2f}% = average of sub-1Y fixed POLGB yields ("
                            + ", ".join(f"{f['ticker']} {f['fix_yld']:.2f}%" for f in sub) + ").")
    dump(out / "market_inputs.json", M)

    # 5) floaters: POLSTR basis
    FL = load(out / "floaters.json")
    p = S["polstr"]
    for tk, upd in S.get("floaters_update", {}).items():  # coupon resets (MoF rate notices) once the new period has started
        FL["floaters"][tk].update(upd)
    FL["polstr_basis"] = round(w["6m"] - p["value"], 3)
    FL["basis_note"] = (f"WIBOR 6M {w['6m']:.2f}% ({dmy(C)}) minus POLSTR {p['value']:.2f}% (index date {dmy(p['date'])}, published the next business day; "
                        f"later index dates are published after the report time and are not used); running NZ period assumed at {FL['nz_running']:.2f}% compounded POLSTR")
    dump(out / "floaters.json", FL)

    # 6) core inputs: money, CIP hedge rates, 1Y IBORs
    CI = load(out / "core_inputs.json")
    e, sofr = S["euribor"], K["sofr"][max(K["sofr"])]
    estr = K["estr"][max(d for d in K["estr"] if d <= C)]
    CI["money"] = {"EUR": {"3m": e["3m"], "6m": e["6m"], "12m": e["12m"], "estr": estr}, "USD": {"3m": ust["3 Mo"], "sofr": sofr}}
    eur1y = round(e["12m"] * 365 / 360, 3)
    CI["hedge_rates_1y"] = {"PLN": w["1y"], "EUR": eur1y, "USD": ust["1 Yr"],
                            "method": (f"no market forward points were found, so hedges use covered interest parity on 1Y fixings of {dmy(C)} (WIBOR 1Y {w['1y']:.2f}%, "
                                       f"EURIBOR 12M {e['12m']:.3f}% ACT/360, 1Y T-bill {ust['1 Yr']:.2f}%). With NBP cuts priced, the FX-implied PLN rate is likely below WIBOR 1Y, "
                                       "so these pickups are probably an upper bound")}
    CI["ibor_1y"] = {"PLN": w["1y"], "EUR": eur1y, "CZK": round(S["pribor"]["1y"] * 365 / 360, 3), "HUF": round(S["bubor"]["12m"] * 365 / 360, 3), "USD": ust["1 Yr"]}
    dump(out / "core_inputs.json", CI)

    # 7) quasi inputs: Catalyst closes
    Q = load(out / "quasi_inputs.json")
    old_label = dmy(load(prev / "market_inputs.json")["asof"])
    for row in Q["fixed"]:
        x = S["fpc"].get(row[0])
        if not x:
            continue
        row[5] = x["close"]
        if x.get("traded", True):
            row[6] = f"Catalyst close {dmy(C)}" + (f" on {x['vol']:g} bond{'s' if x['vol'] != 1 else ''} (stale: treat as indicative)" if x.get("vol") is not None and x["vol"] < 10 else "")
        else:
            row[6] = f"no trade on {dmy(C)}; last Catalyst close {dmy(x['last_trade_date'])} (stale: treat as indicative)"
    for k in ("lede", "sources"):
        Q[k] = Q[k].replace(old_label, dmy(C))
    if S.get("quasi_lede"):
        Q["lede"] = S["quasi_lede"]
    if S.get("quasi_takeaways"):
        Q["takeaways_html"] = S["quasi_takeaways"]
    dump(out / "quasi_inputs.json", Q)

    # 8) MoF operations
    ops = load(out / "mof_operations_2025H2.json")
    ops += [o for o in S.get("mof_ops_add", []) if o["date"] <= C and o not in ops]
    dump(out / "mof_operations_2025H2.json", sorted(ops, key=lambda o: o["date"]))

    # 9) facts: dates, overrides, standard audit rows
    F = load(out / "facts.json")
    F.update(report_date=R, market_cutoff=C, info_cutoff=I, settlement_note=S.get("settlement_note", ""))
    for k, v in S.get("facts", {}).items():
        if isinstance(v, dict) and isinstance(F.get(k), dict) and not v.get("_replace"):
            F[k].update(v)
        else:
            F[k] = v.get("_value", v) if isinstance(v, dict) and v.get("_replace") else v
    F["calendar"]["events"] = [ev for ev in F["calendar"]["events"] if ev["date"] >= R]
    auto = {
        "POLGB prices & yields": dict(as_of=f"{dmy(C)} close", published=dmy(C), note="TBSP.Index level dropped: the page shows the current value."),
        "PLN IRS curve": dict(as_of=f"{dmy(C)} close", published=irs["published"], source=irs["src_label"], note=irs.get("audit_note", "Only the cut-off-day levels are used.")),
        "WIBOR, POLSTR": dict(as_of=f"{dmy(C)} (WIBOR); {dmy(p['date'])} (POLSTR)", published=f"{dmy(C)} (fixings)", source="GPW Benchmark delayed data",
                              note=f"POLSTR index dates after {dmy(p['date'])} are published after the report time and are not used."),
        "FRA strip": dict(as_of=f"{dmy(C)} close", published=irs["published"], source=irs["src_label"], note=""),
        "Fixing history (auction study, charts)": dict(as_of=f"25 Aug 2025 - {dmy(C)}"),
        "Bund curve, UST curve, €STR, SOFR": dict(as_of=f"{dmy(C)} (SOFR {dmy(max(K['sofr']))})", published=f"<= {dmy(R)} pre-open",
                                                  source=f"Bundesbank BBSIS, US Treasury, ECB, NY Fed (observations <= {dmy(C)}; SOFR < {dmy(C)}: it is published T+1 at 08:00 New York time)"),
        "EURIBOR, PRIBOR, BUBOR": dict(as_of=f"{dmy(C)} (BUBOR {dmy(S['bubor']['date'])})", published="fixing dates", source="EMMI via Bundesbank; CNB; MNB"),
        "Cross-country yields": dict(as_of=S["pap"]["date"], published=S["pap"].get("published", ""), source="PAP/Bloomberg table on strefainwestorow.pl; US from the US Treasury curve",
                                     note="Rows carrying live quotes from the report morning are excluded."),
        "BGK FPC prices & plans": dict(as_of=dmy(C), published="Catalyst daily", note="; ".join(f"{t}: {'no trade' if not x.get('traded', True) else 'vol ' + format(x['vol'], 'g')}" for t, x in S["fpc"].items())),
    }
    for a in F["audit"]:
        if a["input"] in auto:
            a.update(auto[a["input"]])
    for a in F["audit"]:
        if a["input"] in S.get("audit_updates", {}):
            a.update(S["audit_updates"][a["input"]])
    F["audit"] = [a for a in F["audit"] if not a["input"].startswith("New facts")]
    nf = S.get("new_facts_audit")
    if nf:
        F["audit"].insert(len(F["audit"]) - 1, nf)
    dump(out / "facts.json", F)
    print("snapshot", out, "| funding", round(rp["funding"], 3), rp["rule"], "| GC", rp["gc"], "| anchor", round(anchor, 3), "| polstr basis", FL["polstr_basis"])


if __name__ == "__main__":
    main(*sys.argv[1:5])
