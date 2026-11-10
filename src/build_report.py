"""Generic, point-in-time report builder for a snapshot folder (e.g. data/snapshots/2026-01-02).

Everything quantitative comes from files computed from the snapshot's own inputs; every qualitative statement comes
from the snapshot's facts.json, where each fact carries its own publication date and source. Benchmarks, trade ideas
and rebalance projections are chosen by rules, so the text contains nothing written with hindsight.

Usage: python src/build_report.py data/snapshots/2026-01-02  ->  <snap>/dist/index.html
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from analytics import ROOT, irs_curve  # noqa: E402

E = html.escape


def f(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def sg(x, d=2):
    if x is None:
        return "–"
    r = round(x, d)
    return ("+" if r > 0 else "−" if r < 0 else "") + f"{abs(r):.{d}f}"


def load(p):
    p = pathlib.Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def dmy(iso):
    return dt.date.fromisoformat(iso).strftime("%d %b %Y").lstrip("0")


SCEN_LABEL = {
    "Parallel +50bp": "Parallel +50bp",
    "Parallel -50bp": "Parallel −50bp",
    "Bear flattener (MPC hikes: +60bp 1Y -> +15bp 10Y)": "Front end sells off (+60bp 1Y → +15bp 10Y)",
    "Bull flattener (fiscal relief: -10bp 1Y -> -60bp 10Y)": "Long end rallies (−10bp 1Y → −60bp 10Y)",
    "Bull steepener (cuts priced: -60bp 1Y -> -20bp 10Y)": "Front end rallies (−60bp 1Y → −20bp 10Y)",
}


def main(snap: pathlib.Path):
    A = load(snap / "analytics.json")
    F = load(snap / "facts.json") or {}
    IP = load(snap / "index_portfolios.json")
    cyc = load(snap / "auction_cycle.json")
    ops = load(snap / "mof_operations_2025H2.json") or []
    hist = load(snap / "fixing_history.json") or {}
    FL = load(snap / "fl.json")
    K = load(snap / "core.json")
    Q = load(snap / "quasi.json")
    mi = A["market_inputs"]
    mm = mi["money_market"]
    B = {b["ticker"]: b for b in A["bonds"]}
    IX = A["indices"]
    irs = irs_curve(mi)
    fund = A["funding"]
    report_date = F.get("report_date", A["asof"])
    cutoff = F.get("market_cutoff", A["asof"])
    info_cut = F.get("info_cutoff", cutoff)
    fixed = [b for b in A["bonds"] if b["ttm"] > 0.9]

    def bench(T):
        c = [b for b in A["bonds"] if b["src"] == "fixing" and b["ttm"] > 0.9]
        return min(c, key=lambda b: abs(b["ttm"] - T))

    b2, b5, b10 = bench(2), bench(5), bench(10)
    ex_md = lambda b: b["h12"]["net"] / b["mod"] * 100
    s2s10 = (b10["ytm"] - b2["ytm"]) * 100
    s5s10 = (b10["ytm"] - b5["ytm"]) * 100
    irs1, irs2 = irs(1.0), irs(2.0)
    fwd_6x12 = (irs1 - mm["wibor_6m"] * 0.5) / 0.5
    fwd_1y1y = 2 * irs2 - irs1
    pol = F.get("policy", {})
    mac = F.get("macro", {})

    # ---------------- rule-based selections
    front = [b for b in fixed if 1.5 <= b["ttm"] <= 4.2 and b.get("h12") and not b["h12"].get("matures")]
    best_front = max(front, key=ex_md)
    by_md = {}
    for b in fixed:
        if b["ttm"] >= 1.5 and b.get("h12") and not b["h12"].get("matures"):
            by_md[b["ticker"]] = ex_md(b)
    best_md_sector = sorted(by_md.items(), key=lambda kv: -kv[1])[:3]
    # RV switch: same duration (|dMD| < 0.35), maximise rich/cheap gap
    pairs = []
    cand = [b for b in fixed if b["rc_bp"] is not None and b["ttm"] > 1.5]
    for r in cand:
        for c in cand:
            if r is c or abs(r["mod"] - c["mod"]) > 0.35:
                continue
            gap = c["rc_bp"] - r["rc_bp"]
            pairs.append((gap, r, c))
    rv = max(pairs, key=lambda x: x[0]) if pairs else None
    rc_sorted = sorted([b for b in fixed if b["rc_bp"] is not None], key=lambda b: b["rc_bp"])
    rich, cheap = rc_sorted[:5], rc_sorted[::-1][:5]
    aswb = {b["bucket"]: b for b in A["asw_buckets"]}
    sub1 = [b for b in A["bonds"] if b["ttm"] < 1.0]

    # index rebalance projection (rules: 1-3Y / 1-4Y maturity windows at the next periodic change)
    nxt = dt.date.fromisoformat(IP["next_rebalance"])
    tb_units = IP["indices"]["TBSP.Index"]["units"]

    def proj(code, lo, hi):
        units = dict(IP["indices"][code]["units"])
        ttm_at = lambda t: (dt.date.fromisoformat(B[t]["maturity"]) - nxt).days / 365.25
        out = [t for t in units if ttm_at(t) < lo]
        inn = [t for t in tb_units if t not in units and t in B and lo <= ttm_at(t) <= hi]
        for t in out:
            units.pop(t)
        for t in inn:
            units[t] = tb_units[t]
        mv = {t: u * 10 * B[t]["dirty"] for t, u in units.items()}
        tot = sum(mv.values())
        return out, inn, sum(mv[t] / tot * B[t]["mod"] for t in mv)

    p13 = proj("GPWB-B1Y3Y", 1, 3)
    p14 = proj("GPWB-B1Y4Y", 1, 4)

    # ---------------- JS payload
    hist_series = {}
    for t in (b2["ticker"], b5["ticker"], b10["ticker"]):
        hist_series[t] = [[d, v[t][1]] for d, v in sorted(hist.items()) if t in v and v[t][1] is not None]
    labels = list({b2["ticker"], b5["ticker"], b10["ticker"]} | {b["ticker"] for b in rich[:2]} | {b["ticker"] for b in cheap[:2]})
    js = dict(bonds=A["bonds"], curve=A["curve"], asw_buckets=A["asw_buckets"], indices=IX, market_inputs={}, label_bonds=labels,
              highlight=[best_front["ticker"]] + ([rv[1]["ticker"], rv[2]["ticker"]] if rv else []), hist=hist_series,
              auctions=cyc["_meta"]["auctions"] if cyc else [], cycle={k: v for k, v in (cyc or {}).items() if not k.startswith("_")},
              core=({k: K[k] for k in ("grid", "carry_roll", "spread_hist", "swapped") if k in K} if K else None),
              fl=({"floaters": FL["floaters"]} if FL else None))

    o = []
    w = o.append
    # ---------------- header
    w(f"""
<header class="top">
  <div>
    <h1>Polish fixed income desk — {E(dmy(report_date))}</h1>
    <p class="sub">Point-in-time report: POLGB curve, index duration (GPWB 1-3Y, GPWB 1-4Y, TBSP.Index), asset swaps, rich/cheap, floaters &amp; linkers, carry &amp; roll, Poland vs core, auction timing and trade ideas.</p>
    <div class="meta">Market data: close of {E(dmy(cutoff))} (last session before the report date) · information published by {E(dmy(info_cut))} · settlement {E(A['settle'])} · private page, not indexed</div>
  </div>
  <button class="theme-btn" id="themeBtn" type="button">Dark mode</button>
</header>
<div class="note" style="margin-top:14px"><b>Point-in-time discipline.</b> Nothing in this report uses information that was not available before {E(dmy(report_date))}:
prices are the BondSpot close of {E(dmy(cutoff))}, index portfolios are those in force after the {E(dmy(IP['effective']))} rebalance, the swap curve, central-bank and macro facts are dated
on or before {E(dmy(info_cut))}, and the auction-timing study uses only {E(cyc['_meta']['start'] if cyc else '')} – {E(cyc['_meta']['end'] if cyc else '')} data. Trade ideas are generated by rules from these numbers.
The full source-and-date audit is at the bottom.</div>
<nav class="toc" aria-label="Sections">
  <a href="#bottom">Bottom line</a><a href="#indices">Index duration</a><a href="#curve">Curve &amp; ASW</a><a href="#rv">Single bonds</a>
  {'<a href="#floaters">Floaters &amp; IZ</a>' if FL else ''}<a href="#roll">Carry &amp; roll</a>{'<a href="#core">PL vs core</a>' if K else ''}<a href="#auctions">Auctions &amp; timing</a>
  <a href="#ideas">What to play</a><a href="#bonds">All bonds</a><a href="#method">Method &amp; audit</a>
</nav>
""")
    tiles = [
        ("NBP reference", f"{f(pol.get('nbp_reference'))}%", E(pol.get("next_mpc_label", ""))),
        ("WIBOR 3M / 6M", f"{f(mm['wibor_3m'])} / {f(mm['wibor_6m'])}", E(mm.get("overnight_label", ""))),
        ("Repo (funding)", f"{f(fund)}%", E(mm.get("repo_label", ""))),
        (f"POLGB 2Y ({b2['ticker']})", f"{f(b2['ytm'])}%", f"ASW {sg(b2['asw_bp'], 0)}bp"),
        (f"POLGB 5Y ({b5['ticker']})", f"{f(b5['ytm'])}%", f"ASW {sg(b5['asw_bp'], 0)}bp"),
        (f"POLGB 10Y ({b10['ticker']})", f"{f(b10['ytm'])}%", f"ASW {sg(b10['asw_bp'], 0)}bp"),
        ("IRS 2Y / 5Y / 10Y", " / ".join(f(mi['irs']['pillars'].get(k)) for k in ("2", "5", "10")), E(mi["irs"].get("asof", ""))),
        ("2s10s / 5s10s", f"{f(s2s10, 0)} / {f(s5s10, 0)}bp", "benchmark bonds"),
        ("CPI (latest)", f"{f(mac.get('cpi', {}).get('v'), 1)}%", E(mac.get("cpi", {}).get("m", ""))),
        ("Index officials", f"{f(IX['TBSP.Index']['official']['mod_dur'])}", f"TBSP MD as of {E(IP['official_stats_asof'])}"),
    ]
    w('<div class="tiles">' + "".join(f'<div class="tile"><div class="l">{E(a)}</div><div class="v">{E(b)}</div><div class="d">{c}</div></div>' for a, b, c in tiles) + "</div>")

    t13, t14, tb = IX["GPWB-B1Y3Y"], IX["GPWB-B1Y4Y"], IX["TBSP.Index"]
    cyc_txt = ""
    if cyc:
        days_rank = sorted([k for k in cyc if not k.startswith("_") and k != "other"], key=lambda k: -cyc[k]["mean"])
        cheapest_day = days_rank[0]
        cyc_txt = (f"In the {len(cyc['_meta']['auctions'])} auctions from {dmy(cyc['_meta']['start'])} to {dmy(cyc['_meta']['end'])} (basket {sg(cyc['_meta']['total_change_bp'], 0)}bp over the window), "
                   f"the session that cheapened most was {cheapest_day.replace('T+0', 'auction day')} ({sg(cyc[cheapest_day]['mean'], 1)}bp on average, up {cyc[cheapest_day]['up_share'] * 100:.0f}% of the time); "
                   f"other days averaged {sg(cyc['other']['mean'], 1)}bp.")
    fl = FL["floaters"] if FL else []
    wz = [x for x in fl if x["ticker"].startswith("WZ") and x["ttm"] > 0.9]
    wz_best = max(wz, key=lambda x: x["dm_per_sdur"]) if wz else None
    wz_beat = [x for x in wz if x["vs_fixed_bp"] > 5]
    lk = FL["linkers"] if FL else []
    w(f"""
<div class="bottomline" id="bottom">
  <h2>Bottom line — {E(dmy(report_date))}</h2>
  <ol>
    <li><b>Modified duration:</b> GPWB 1-3Y <b>{f(t13['mod'])}</b>, GPWB 1-4Y <b>{f(t14['mod'])}</b>, TBSP.Index <b>{f(tb['mod'])}</b> at the {E(dmy(cutoff))} close
      (GPW Benchmark official at {E(dmy(IP['official_stats_asof']))}: {f(t13['official']['mod_dur'])} / {f(t14['official']['mod_dur'])} / {f(tb['official']['mod_dur'])}). Cash-flow yields {f(t13['irr'])}% / {f(t14['irr'])}% / {f(tb['irr'])}%.
      At the {E(dmy(IP['next_rebalance']))} rebalance: 1-3Y {('loses ' + ', '.join(p13[0])) if p13[0] else 'keeps its members'}{(' and adds ' + ', '.join(p13[1])) if p13[1] else ''} → MD ≈ {f(p13[2])};
      1-4Y {('loses ' + ', '.join(p14[0])) if p14[0] else 'keeps its members'}{(' and adds ' + ', '.join(p14[1])) if p14[1] else ''} → MD ≈ {f(p14[2])}.</li>
    <li><b>Carry + roll per unit of risk is best in {E(best_front['ticker'])}</b> ({f(best_front['ttm'], 1)}Y): {f(best_front['h12']['total'])}% over 12M on an unchanged curve, {sg(best_front['h12']['net'])}% over repo
      ({f(ex_md(best_front), 0)}bp per duration year, 12M breakeven {f(best_front['h12']['breakeven_bp'], 0)}bp). Top three by excess per duration: {', '.join(f"{t} {v:.0f}bp" for t, v in best_md_sector)}.
      The PLN swap curve implies 6M WIBOR ≈ {f(fwd_6x12)}% in six months vs {f(mm['wibor_6m'])}% now and 1y1y ≈ {f(fwd_1y1y)}%. {E(pol.get('pricing_text', ''))}</li>
    <li><b>Asset swaps:</b> {', '.join(f"{k} {sg(v['avg_asw'], 0)}bp" for k, v in aswb.items() if k in ('2Y', '5Y', '8-9Y', '10Y'))} (yield − PLN IRS). Spread over swaps rises with maturity:
      the term premium sits in the bonds. {E(mac.get('fiscal_text', ''))}</li>
    <li><b>Relative value:</b> {(f"sell {rv[1]['ticker']} ({sg(rv[1]['rc_bp'], 1)}bp vs curve) and buy {rv[2]['ticker']} ({sg(rv[2]['rc_bp'], 1)}bp) at similar duration ({f(rv[1]['mod'])} vs {f(rv[2]['mod'])}): "
      f"{sg((rv[2]['ytm'] - rv[1]['ytm']) * 100, 0)}bp of yield, {f(rv[0], 0)}bp of it pure rich/cheap.") if rv else 'no clean same-duration switch.'}
      Cheapest lines: {', '.join(f"{b['ticker']} {sg(b['rc_bp'], 1)}" for b in cheap[:3])}bp; richest: {', '.join(f"{b['ticker']} {sg(b['rc_bp'], 1)}" for b in rich[:3])}bp.
      Sub-1Y paper yields {f(min(b['ytm'] for b in sub1))}-{f(max(b['ytm'] for b in sub1))}% vs repo {f(fund)}%.</li>
    <li><b>Timing:</b> {E(cyc_txt)} {E(F.get('calendar', {}).get('timing_text', ''))}</li>""")
    if FL and wz_best:
        w(f"""
    <li><b>Floaters &amp; linkers:</b> best WZ per unit of spread duration is {E(wz_best['ticker'])} (DM {sg(wz_best['dm_bp'], 0)}bp over 6M WIBOR, {f(wz_best['dm_per_sdur'], 0)}bp per spread-duration year);
      {('WZ pay more than same-maturity fixed ASW in ' + ', '.join(x['ticker'] for x in wz_beat)) if wz_beat else 'no WZ pays more than same-maturity fixed ASW'}.
      {' '.join(f"{x['ticker']}: real yield {f(x['real_yield'])}%, breakeven {f(x['breakeven'])}%." for x in lk)} {E(mac.get('projection_text', ''))}</li>""")
    if K:
        kc = {(c["mkt"], c["T"]): c for c in K["carry_roll"]}
        kh = {(h["asset"], h["T"]): h for h in K["hedged"]}
        last = K["spread_hist"][-1] if K.get("spread_hist") else None
        w(f"""
    <li><b>Versus core:</b> 10Y carry+roll {f(kc[('PL', 10)]['total_bp'], 0)}bp/yr in Poland vs {f(kc[('DE', 10)]['total_bp'], 0)} (Bund) and {f(kc[('US', 10)]['total_bp'], 0)} (UST);
      2Y per duration year {f(kc[('PL', 2)]['per_dur'], 0)} vs {f(kc[('DE', 2)]['per_dur'], 0)} / {f(kc[('US', 2)]['per_dur'], 0)}bp.{(' PL−Bund 10Y ' + f((last['pl10'] - last['de10']) * 100, 0) + 'bp.') if last else ''}
      Hedged into PLN ({E(K.get('hedge_method', ''))}): 1Y Bund {f(kh[('DE', 1)]['PLN'])}% and 1Y UST {f(kh[('US', 1)]['PLN'])}% vs 1Y POLGB {f(kh[('PL', 1)]['local'])}%; 10Y Bund {f(kh[('DE', 10)]['PLN'])}% vs POLGB {f(kh[('PL', 10)]['local'])}%.</li>""")
    w(f"""
  </ol>
  <div class="sub">Funding {f(fund)}% · horizon returns assume an unchanged curve and constant rich/cheap · {E(mi['irs'].get('short_source', ''))}</div>
</div>""")

    # ---------------- indices
    def ixcard(code):
        ix = IX[code]
        of = ix["official"]
        h3, h12 = ix["horizons"]["h3"], ix["horizons"]["h12"]
        return f"""
<div class="ixcard">
  <div class="name">{E(ix['label'])}</div><div class="rule">{E(ix['rule'])} · {ix['n']} bonds · PLN {ix['mv_bn']:.0f}bn index MV</div>
  <div class="hero">{f(ix['mod'])}<small>modified duration</small></div>
  <div class="kv">
    <span>Macaulay duration (yrs)</span><b>{f(ix['mac'])} <span class="off">off. {f(of['mac_dur'])}</span></b>
    <span>Mod. duration — official {E(IP['official_stats_asof'])}</span><b>{f(of['mod_dur'])}</b>
    <span>Yield (IRR of cash flows)</span><b>{f(ix['irr'])}%</b>
    <span>Yield (MV-weighted avg)</span><b>{f(ix['ytm'])}% <span class="off">off. {f(of['ytm'])}%</span></b>
    <span>Avg maturity (yrs) / coupon</span><b>{f(ix['ttm'])} / {f(ix['coupon'])}%</b>
    <span>Convexity</span><b>{f(ix['conv'], 1)}</b>
    <span>DV01 per PLN 1m</span><b>PLN {ix['dv01_per_mn']:.0f}</b>
    <span>Avg ASW (yield − IRS)</span><b>{sg(ix['asw_bp'], 0)}bp</b>
    <span>3M carry+roll / excess vs repo</span><b>{f(h3['total'])}% / {sg(h3['net'])}%</b>
    <span>12M carry+roll / excess vs repo</span><b>{f(h12['total'])}% / {sg(h12['net'])}%</b>
    <span>…of which coupon / pull / roll</span><b>{f(h12['coupon'])} / {f(h12['pull'])} / {f(h12['roll'])}</b>
    <span>Breakeven yield rise 3M / 12M</span><b>{f(h3['breakeven_bp'], 0)} / {f(h12['breakeven_bp'], 0)}bp</b>
    <span>12M excess per unit duration</span><b>{f(h12['net'] / ix['mod'] * 100, 0)}bp</b>
  </div>
</div>"""
    scen_names = list(tb["scenarios"].keys())
    scen_rows = "".join(f"<tr><td class='l'>{E(SCEN_LABEL.get(s, s))}</td>" + "".join(
        f"<td>{sg(IX[c]['scenarios'][s]['instant'])}%</td><td>{f(IX[c]['scenarios'][s]['twelve_m'])}%</td>" for c in IX) + "</tr>" for s in scen_names)
    w(f"""
<section class="card" id="indices">
  <h2>Index modified duration <span class="tag">GPWB 1-3Y · GPWB 1-4Y · TBSP</span></h2>
  <p class="lede">Computed bond by bond from the GPW Benchmark portfolios in force after the {E(dmy(IP['effective']))} periodic change (<a href="{E(IP['source_url'])}" rel="noopener">communiqué</a>, holdings as of 22 Dec 2025),
  re-weighted at {E(dmy(cutoff))} dirty prices. Next periodic change: {E(dmy(IP['next_rebalance']))}.</p>
  <div class="grid3">{ixcard('GPWB-B1Y3Y')}{ixcard('GPWB-B1Y4Y')}{ixcard('TBSP.Index')}</div>
  <div class="note"><b>Next rebalance ({E(dmy(IP['next_rebalance']))}), applying the maturity windows to today's universe:</b>
    GPWB 1-3Y: out {E(', '.join(p13[0]) or 'none')}, in {E(', '.join(p13[1]) or 'none')} → MD {f(t13['mod'])} → ~{f(p13[2])}.
    GPWB 1-4Y: out {E(', '.join(p14[0]) or 'none')}, in {E(', '.join(p14[1]) or 'none')} → MD {f(t14['mod'])} → ~{f(p14[2])}.
    Entrants are bought by trackers into the rebalance; leavers are sold.</div>
  <h3>Contribution to duration, by constituent</h3>
  <div class="tabs" id="ixTabs" role="group" aria-label="Choose index"></div>
  <div class="legend"><span><i style="background:var(--s1)"></i>Weight × modified duration</span></div>
  <div id="ixDetail"></div>
  <h3>Scenario P&amp;L (full repricing)</h3>
  <p class="lede">"Now" = instantaneous price change; "12M" = 12-month total return including carry and roll. All in %.</p>
  <div class="tablewrap"><table class="t">
    <thead><tr><th class="l">Scenario</th>{''.join(f"<th>{E(IX[c]['label'].replace('GPWB ', ''))} now</th><th>{E(IX[c]['label'].replace('GPWB ', ''))} 12M</th>" for c in IX)}</tr></thead>
    <tbody>{scen_rows}</tbody></table></div>
</section>""")

    # ---------------- curve & ASW
    asw_rows = "".join(f"<tr><td class='l'>{E(b['bucket'])}</td><td class='l'>{E(', '.join(b['bonds']))}</td><td>{f(b['avg_ytm'])}</td><td>{f(b['irs'])}</td>"
                       f"<td>{sg(b['avg_asw'], 0)}</td><td>{sg(b['min_asw'], 0)} … {sg(b['max_asw'], 0)}</td><td class='l'>{E(b['widest'])}</td></tr>" for b in A["asw_buckets"])
    irs_s = mi["irs"]["pillars"]
    w(f"""
<section class="card" id="curve">
  <h2>Curve &amp; asset swaps <span class="tag">yield − IRS</span></h2>
  <p class="lede">Dots: BondSpot closing fixings {E(dmy(cutoff))}. Blue line: Nelson-Siegel-Svensson fit; orange: PLN IRS vs 6M WIBOR ({E(mi['irs'].get('asof', ''))}).
  Benchmark 2s10s {f(s2s10, 0)}bp vs IRS 2s10s {f((irs_s['10'] - irs_s['2']) * 100, 0)}bp.</p>
  <div class="legend"><span><i class="dot" style="background:var(--s1)"></i>Bond yield (fixing)</span><span><i class="line" style="background:var(--s1);opacity:.55"></i>Fitted NSS curve</span><span><i class="line" style="background:var(--s2)"></i>PLN IRS</span></div>
  <div class="chart" id="curveChart"></div>
  <h3>ASW by tenor bucket</h3>
  <div class="legend"><span><i style="background:var(--s1)"></i>Average yield − PLN IRS at the same maturity (bp)</span></div>
  <div class="chart" id="aswChart"></div>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bucket</th><th class="l">Bonds</th><th>Avg yield %</th><th>IRS %</th><th>Avg ASW bp</th><th>Range bp</th><th class="l">Widest</th></tr></thead><tbody>{asw_rows}</tbody></table></div>
  <p class="small">IRS curve: {E(mi['irs'].get('source', ''))}</p>
</section>""")

    # ---------------- RV
    li = lambda b: f"<li><b>{E(b['ticker'])}</b> ({f(b['coupon'])}% {E(b['maturity'][:7])}): {sg(b['rc_bp'], 1)}bp vs curve, yield {f(b['ytm'], 3)}%, ASW {sg(b['asw_bp'], 0)}bp</li>"
    w(f"""
<section class="card" id="rv">
  <h2>Single papers that stand out <span class="tag">rich / cheap vs fitted curve</span></h2>
  <p class="lede">Residual = bond yield − yield the fitted zero curve gives for the same cash flows. Positive = cheap. Inside ±2bp is noise.</p>
  <div class="legend"><span><i style="background:var(--pos)"></i>Cheap</span><span><i style="background:var(--neg)"></i>Rich</span></div>
  <div class="chart" id="rcChart"></div>
  <div class="grid2" style="margin-top:12px"><div><h3>Cheapest</h3><ul class="tight">{''.join(li(b) for b in cheap)}</ul></div><div><h3>Richest</h3><ul class="tight">{''.join(li(b) for b in rich)}</ul></div></div>
  {(f'<div class="note"><b>Same-duration switch (rule: |ΔMD| &lt; 0.35, max rich/cheap gap):</b> sell {E(rv[1]["ticker"])} / buy {E(rv[2]["ticker"])} — {sg((rv[2]["ytm"] - rv[1]["ytm"]) * 100, 0)}bp yield, {f(rv[0], 0)}bp rich/cheap, MD {f(rv[1]["mod"])} → {f(rv[2]["mod"])}.</div>') if rv else ''}
</section>""")

    # ---------------- floaters & linkers & quasi
    if FL:
        rows = "".join(
            f"<tr><td class='l'>{E(x['ticker'])}</td><td class='l'>{E(x['index'])}</td><td>{E(x['maturity'])}</td><td>{f(x['ttm'], 2)}</td><td>{f(x['clean'], 2)}</td><td>{f(x['current_coupon'], 2)}</td>"
            f"<td>{sg(x['dm_bp'], 0)}</td><td><b>{sg(x['dm_wibor_eq_bp'], 0)}</b></td><td>{f(x['spread_dur'], 2)}</td><td>{f(x['rate_dur'], 2)}</td><td>{sg(x['fixed_asw_bp'], 0)}</td>"
            f"<td><b>{sg(x['vs_fixed_bp'], 0)}</b></td><td>{f(x['dm_per_sdur'], 1)}</td><td>{sg(x['carry_12m'], 2)}</td><td class='l'>{E(x['src'])}</td></tr>" for x in fl)
        sc_names = list(lk[0]["total_12m"].keys()) if lk else []
        lrows = "".join(
            f"<tr><td class='l'>{E(x['ticker'])}</td><td>{E(x['maturity'])}</td><td>{f(x['real_coupon'], 2)}</td><td>{f(x['clean'], 2)}</td><td><b>{f(x['real_yield'], 2)}</b></td><td>{f(x['nominal_fit'], 2)}</td>"
            f"<td><b>{f(x['breakeven'], 2)}</b></td><td>{f(x['real_mod'], 2)}</td>" + "".join(f"<td>{sg(x['vs_nominal_12m'][k], 2)}</td>" for k in sc_names)
            + f"<td>{f(x['nominal_peer_12m'] - x['real_carry_12m'], 1)}%</td></tr>" for x in lk)
        q_html = ""
        if Q and Q.get("bonds"):
            qrows = "".join(f"<tr><td class='l'>{E(r['ticker'])}</td><td class='l'>{E(r.get('coupon_desc', ''))}</td><td>{E(r.get('maturity', ''))}</td><td>{f(r.get('price'))}</td><td>{f(r.get('yield'))}</td>"
                            f"<td>{f(r.get('polgb_same'))}</td><td><b>{sg(r.get('spread_polgb_bp'), 0)}</b></td><td>{sg(r.get('asw_bp'), 0)}</td><td class='l' style='white-space:normal;max-width:240px'>{E(r.get('note', ''))}</td></tr>" for r in Q["bonds"])
            q_html = f"""<h3>Quasi-sovereigns (BGK FPC)</h3><p class="small">{E(Q.get('lede', ''))}</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Series</th><th class="l">Coupon</th><th>Maturity</th><th>Price</th><th>Yield %</th><th>POLGB same mat. %</th><th>Spread vs POLGB bp</th><th>ASW bp</th><th class="l">Note</th></tr></thead><tbody>{qrows}</tbody></table></div>
  <div class="note"><ul class="tight">{''.join(f'<li>{x}</li>' for x in Q.get('takeaways_html', []))}</ul></div><p class="small">{E(Q.get('sources', ''))}</p>"""
        w(f"""
<section class="card" id="floaters">
  <h2>Floaters (WZ, NZ), linkers (IZ){' &amp; quasi-sovereigns' if q_html else ''} <span class="tag">spread vs duration</span></h2>
  <p class="lede">WZ pay 6M WIBOR flat (semi-annual); NZ pay compounded POLSTR/WIRON flat. Discount margin (DM) = spread over a 6M WIBOR forward curve bootstrapped from the {E(dmy(cutoff))} PLN swap curve
  (6M forward ≈ {f(FL['fwd_6m'][1]['f'])}% six months ahead). NZ forwards = WIBOR forwards − {f(FL['polstr_basis'] * 100, 0)}bp ({E(FL.get('basis_note', ''))}). WIBOR-equivalent DM is comparable with fixed ASW.</p>
  <div class="legend"><span><i class="line" style="background:var(--s1);opacity:.6"></i>Fixed POLGB ASW</span><span><i class="dot" style="background:var(--s2)"></i>WZ DM</span><span><i style="background:var(--s3)"></i>NZ DM (WIBOR-equiv.)</span></div>
  <div class="chart" id="flChart"></div>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bond</th><th class="l">Index</th><th>Maturity</th><th>Yrs</th><th>Price</th><th>Current cpn %</th><th>DM vs index</th><th>DM WIBOR-eq.</th>
  <th>Spread dur.</th><th>Rate dur.</th><th>Fixed ASW same mat.</th><th>Floater − fixed</th><th>DM per spread-dur. yr</th><th>12M carry vs repo %</th><th class="l">Price</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="note"><b>Reading it.</b> <ul class="tight">
    <li>Floater − fixed &gt; 0: the floater pays more spread than a same-maturity fixed bond asset-swapped. {('Positive in ' + ', '.join(x['ticker'] for x in wz_beat) + '.') if wz_beat else 'Negative everywhere: fixed bonds asset-swapped give more spread.'}</li>
    <li>Best DM per spread-duration year: {E(wz_best['ticker']) if wz_best else '–'} ({f(wz_best['dm_per_sdur'], 0) if wz_best else '–'}bp). Floaters carry ~0 rate duration, so they are the way to own spread without a rates view.</li></ul></div>
  <h3>Inflation-linked IZ</h3>
  <p class="small">Real yield from the real (unindexed) price; breakeven = (1+nominal)/(1+real) − 1 vs the fitted nominal curve; 12M vs the nominal neighbour's carry+roll under CPI-indexation scenarios. {E(mac.get('projection_text', ''))}</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bond</th><th>Maturity</th><th>Real cpn %</th><th>Price</th><th>Real yield %</th><th>Nominal (fit) %</th><th>Breakeven %</th><th>Real MD</th>
  {''.join(f'<th>12M vs nominal @ CPI {E(k)}</th>' for k in sc_names)}<th>CPI needed to match nominal</th></tr></thead><tbody>{lrows}</tbody></table></div>
  {q_html}
</section>""")

    # ---------------- carry & roll (same structure as live)
    w(f"""
<section class="card" id="roll">
  <h2>Roll yield, decomposed <span class="tag">effects that overlap, separated</span></h2>
  <div class="decomp-eq">Total = Coupon income + Pull-to-par + Roll-down &nbsp;|&nbsp; Coupon + Pull-to-par = "yield carry" ≈ YTM × h &nbsp;|&nbsp; Excess = Total − Repo funding</div>
  <ul class="tight">
    <li><b>Coupon income</b>: coupon accrued/paid over the horizon (zero for OK bonds). <b>Pull-to-par</b>: clean-price drift to 100 at an unchanged own yield. Together they equal the yield.</li>
    <li><b>Roll-down</b>: extra gain from sliding down the unchanged fitted curve, residual held constant. It only materialises if the curve stays put, so it is a view against the forwards
      (1Y swap {f(irs1)}% → implied 6M WIBOR in 6M ≈ {f(fwd_6x12)}% vs {f(mm['wibor_6m'])}% now).</li>
    <li><b>Funding</b>: repo at {f(fund)}% on the dirty price; <b>breakeven</b> = yield rise over the horizon that wipes out the excess.</li>
  </ul>
  <div class="tabs" id="crTabs" role="group" aria-label="Horizon"></div>
  <div class="legend"><span><i style="background:var(--s1)"></i>Coupon income</span><span><i style="background:var(--s2)"></i>Pull-to-par</span><span><i style="background:var(--s3)"></i>Roll-down</span><span><i class="tick" style="background:var(--ink)"></i>Repo funding cost</span></div>
  <div class="chart" id="crChart"></div>
  <h3>Full decomposition (12M unless noted; % of dirty price)</h3>
  <div id="crTable"></div>
</section>""")

    # ---------------- core
    if K:
        w(core_html(K, F, A, B, cutoff))

    # ---------------- auctions
    cal = F.get("calendar", {})
    ev_rows = "".join(f"<tr><td>{E(dt.date.fromisoformat(e['date']).strftime('%a %d %b %Y'))}</td><td class='l'><span class='pill'>{E(e['type'])}</span></td><td class='l'>{E(e['title'])}</td>"
                      f"<td class='l' style='white-space:normal;min-width:260px'>{E(e.get('note', ''))}</td><td class='l small'>{E(e.get('source_date', ''))}</td></tr>" for e in cal.get("events", []))
    sale = [x for x in ops if x["type"] == "S" and x["op"] in ("AS", "AZ") and x["date"] >= "2025-10-01"]
    ra = "".join(f"<tr><td>{E(x['date'])}</td><td class='l'>{E(x['op'].replace('AS', 'sale').replace('AZ', 'switch'))}</td><td>{sum((l['sold'] or 0) for l in x['lines']) / 1000:.1f}</td>"
                 f"<td>{sum((l['demand'] or 0) for l in x['lines']) / 1000:.1f}</td><td class='l' style='white-space:normal;min-width:300px'>"
                 + E("; ".join(f"{l['series']} {l['sold']:,.0f}" + (f" @{l['avg_yld']:.3f}%" if l['avg_yld'] else "") for l in x["lines"] if l["sold"])) + "</td></tr>" for x in sale[::-1])
    w(f"""
<section class="card" id="auctions">
  <h2>Auctions, flows &amp; when to buy <span class="tag">MoF calendar</span></h2>
  <p class="lede">{E(cal.get('plan_text', ''))}</p>
  <div class="grid2">
    <div><h3>Auction-cycle pattern — {E(cyc['_meta']['start'])} to {E(cyc['_meta']['end'])}</h3>
      <p class="small">Average daily change of a {len(cyc['_meta']['basket'])}-bond 1.5-11Y basket, by session relative to the {len(cyc['_meta']['auctions'])} sale/switch auctions in the window
      (basket {sg(cyc['_meta']['total_change_bp'], 0)}bp over the period). Small sample.</p><div class="chart" id="cycleChart"></div></div>
    <div><h3>Benchmark yields and auction days</h3><div class="legend">{''.join(f'<span><i class="line" style="background:var(--s{i + 1})"></i>{E(t)}</span>' for i, t in enumerate(hist_series))}<span><i class="tick" style="background:var(--axis)"></i>Auction</span></div><div class="chart" id="histChart"></div></div>
  </div>
  <div class="callout"><b>When to buy.</b> {E(cyc_txt)} {E(cal.get('timing_text', ''))}</div>
  <h3>Calendar known on {E(dmy(info_cut))}</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th>Date</th><th class="l">Type</th><th class="l">Event</th><th class="l">Why it matters</th><th class="l">Source date</th></tr></thead><tbody>{ev_rows}</tbody></table></div>
  <h3>Recent auctions (MoF)</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th>Date</th><th class="l">Type</th><th>Sold bn</th><th>Demand bn</th><th class="l">Lines (PLN m @ avg yield)</th></tr></thead><tbody>{ra}</tbody></table></div>
</section>""")

    # ---------------- ideas (rule-based)
    ideas = []
    ideas.append(("go", f"Core: own the best carry-per-risk sector ({', '.join(t for t, _ in best_md_sector)})",
                  f"{best_front['ticker']}: {f(best_front['h12']['total'])}% 12M on an unchanged curve, {sg(best_front['h12']['net'])}% over repo, {f(ex_md(best_front), 0)}bp per duration year, breakeven {f(best_front['h12']['breakeven_bp'], 0)}bp.",
                  "Risk: the forwards (" + f(fwd_6x12) + "% implied 6M WIBOR in 6M) realise or the NBP path changes; " + pol.get("risk_text", "check the next MPC.")))
    if rv:
        ideas.append(("go", f"RV switch: sell {rv[1]['ticker']}, buy {rv[2]['ticker']}",
                      f"{sg((rv[2]['ytm'] - rv[1]['ytm']) * 100, 0)}bp of yield at similar duration ({f(rv[1]['mod'])} → {f(rv[2]['mod'])}); {f(rv[0], 0)}bp is rich/cheap.",
                      "Risk: residuals can persist (coupon/tax effects, index flows)."))
    long_asw = max((b for b in fixed if b["ttm"] > 5), key=lambda b: b["asw_bp"])
    ideas.append(("wait", f"Asset-swap long in the widest long bond ({long_asw['ticker']}, ASW {sg(long_asw['asw_bp'], 0)}bp)",
                  f"Running carry ≈ ASW + (6M WIBOR − repo) ≈ {f(long_asw['asw_bp'] + (mm['wibor_6m'] - fund) * 100, 0)}bp/yr with little rate duration.",
                  "Risk: fiscal/supply news widens ASW. " + mac.get("fiscal_risk_text", "")))
    if wz_best:
        ideas.append(("go" if wz_best["vs_fixed_bp"] > 0 else "wait", f"No-duration spread: {wz_best['ticker']}",
                      f"DM {sg(wz_best['dm_bp'], 0)}bp over WIBOR, {f(wz_best['dm_per_sdur'], 0)}bp per spread-duration year, {sg(wz_best['vs_fixed_bp'], 0)}bp vs same-maturity fixed ASW; 12M carry vs repo {sg(wz_best['carry_12m'])}%.",
                      "Risk: spread widening hits floaters too (spread duration ~" + f(wz_best["spread_dur"], 1) + ")."))
    if lk:
        bl = max(lk, key=lambda x: x["vs_nominal_12m"][sc_names[1]] if sc_names else 0)
        ideas.append(("wait", f"Linker vs nominal: {bl['ticker']}", f"Breakeven {f(bl['breakeven'])}%; on the central CPI scenario it out-carries the nominal neighbour by {sg(bl['vs_nominal_12m'][sc_names[1]])}% over 12M; CPI needed to match ≈{f(bl['nominal_peer_12m'] - bl['real_carry_12m'], 1)}%.",
                      "Risk: CPI undershoots the scenario; wide bid/offer."))
    if K:
        kh = {(h["asset"], h["T"]): h for h in K["hedged"]}
        pick1 = kh[("DE", 1)]["PLN"] - kh[("PL", 1)]["local"]
        ideas.append(("go" if pick1 > 0.15 else "avoid", "PLN cash: 1Y Bund/Schatz hedged into PLN vs short POLGB",
                      f"1Y Bund hedged ≈{f(kh[('DE', 1)]['PLN'])}% vs 1Y POLGB {f(kh[('PL', 1)]['local'])}% ({sg(pick1 * 100, 0)}bp); sub-1Y POLGBs {f(min(b['ytm'] for b in sub1))}-{f(max(b['ytm'] for b in sub1))}%.",
                      "Hedge from " + K.get("hedge_method", "") + "; verify live forward points before executing."))
    if sub1 and max(b["ytm"] for b in sub1) < fund:
        ideas.append(("avoid", "Sub-1Y POLGBs", f"Yield {f(min(b['ytm'] for b in sub1))}-{f(max(b['ytm'] for b in sub1))}% below repo {f(fund)}%: negative carry.", "Use T-bills, deposits or the hedged EUR alternative."))
    lab = {"go": ("go", "Play"), "wait": ("wait", "Play on entry"), "avoid": ("avoid", "Avoid")}
    w('<section class="card" id="ideas"><h2>What is worth playing <span class="tag">rule-based</span></h2><p class="lede">Generated by fixed rules from the numbers above (best carry per duration, max same-duration rich/cheap gap, widest ASW, best floater DM per spread duration, linker carry, hedged front end, negative-carry screen); risks from dated facts.</p><div class="ideas">'
      + "".join(f'<div class="idea"><div class="hd"><b>{E(t)}</b><span class="status {lab[s][0]}">{lab[s][1]}</span></div><p>{E(b)}</p><p class="risk">{E(r)}</p></div>' for s, t, b, r in ideas)
      + f'</div><div class="note"><b>Macro backdrop (as known on {E(dmy(info_cut))}).</b> {E(mac.get("backdrop_text", ""))}</div></section>')

    # ---------------- bonds + method/audit
    audit = F.get("audit", [])
    arows = "".join(f"<tr><td class='l'>{E(a['input'])}</td><td>{E(a['as_of'])}</td><td>{E(a.get('published', ''))}</td><td class='l' style='white-space:normal;min-width:260px'>{E(a.get('source', ''))}</td>"
                    f"<td class='l' style='white-space:normal;min-width:200px'>{E(a.get('note', ''))}</td></tr>" for a in audit)
    w(f"""
<section class="card" id="bonds"><h2>All fixed-rate POLGBs <span class="tag">sortable</span></h2><div id="bondTable"></div></section>
<section class="card" id="method">
  <h2>Method &amp; point-in-time audit</h2>
  <p class="lede">Same engine as the live desk: Act/Act ICMA pricing, NSS zero-curve fit with a money-market anchor, PLN IRS interpolation (PCHIP), horizon decomposition, bootstrapped WIBOR forwards for floaters.
  Settlement {E(A['settle'])} (T+2 from {E(dmy(cutoff))}; 31 Dec 2025 and 1 Jan 2026 not settlement days).</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Input</th><th>As of</th><th>Published</th><th class="l">Source</th><th class="l">Note</th></tr></thead><tbody>{arows}</tbody></table></div>
  <p class="small">Not investment advice. Private, unlinked page.</p>
</section>
<footer>Generated {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · report date {E(report_date)} · market cut-off {E(cutoff)} · information cut-off {E(info_cut)}</footer>
""")
    tpl = (ROOT / "src" / "template.html").read_text().replace("<title>Polish FI Desk</title>", f"<title>Polish FI Desk {E(report_date)}</title>")
    page = tpl.replace("<!--BODY-->", "\n".join(o)).replace("/*DATA*/", json.dumps(js, separators=(",", ":"), default=str).replace("</", "<\\/"))
    out = snap / "dist" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print("wrote", out, f"{len(page) / 1024:.0f} KB")


def core_html(K, F, A, B, cutoff):
    pol = F.get("core_policy", {})
    cpi = F.get("core_cpi", {})
    cr = {(c["mkt"], c["T"]): c for c in K["carry_roll"]}
    hed = {(h["asset"], h["T"]): h for h in K["hedged"]}
    cb_rows = "".join(
        f"<tr><td class='l'><b>{E(p['bank'])}</b> <span class='small'>{E(c)}</span></td><td>{E(p.get('rate_disp', ''))}%</td><td class='l' style='white-space:normal;min-width:140px'>{E(p.get('last', ''))}</td>"
        f"<td class='l'>{E(p.get('next', ''))}</td><td class='l'><span class='status {E(p.get('tone', ''))}'>{E(p.get('stance', ''))}</span></td>"
        f"<td class='l' style='white-space:normal;min-width:170px;max-width:260px'>{E(p.get('pricing', ''))}</td><td title='{E(cpi.get(c, {}).get('m', ''))}'>{f(cpi.get(c, {}).get('v'), 1)}%</td>"
        f"<td><b>{sg((p['rate'] - cpi[c]['v']) if (p.get('rate') is not None and cpi.get(c, {}).get('v') is not None) else None)}</b></td></tr>" for c, p in pol.items())
    lab = {"PL": "POLGB", "DE": "Bund", "US": "UST"}

    def cell(T, a, base):
        best = max(hed[(x, T)][base] for x in ("PL", "DE", "US"))
        v = hed[(a, T)][base]
        return f"<td{' style=\"font-weight:600\"' if abs(v - best) < 1e-9 else ''}>{f(v)}</td>"
    hm = "".join(f"<tr><td class='l'>{T}Y</td><td class='l'>{lab[a]}</td><td>{f(hed[(a, T)]['local'])}</td>{cell(T, a, 'PLN')}{cell(T, a, 'EUR')}{cell(T, a, 'USD')}</tr>" for T in (1, 2, 5, 10) for a in ("PL", "DE", "US"))
    snap_rows = ""
    if K.get("snapshot"):
        snap_rows = "".join(f"<tr{' class=\"hl\"' if s['country'] == 'Poland' else ''}><td class='l'>{E(s['country'])}</td><td>{f(s['y2'])}</td><td>{f(s['y5'])}</td><td>{f(s['y10'])}</td>"
                            f"<td>{sg(s['s2s10'], 0)}</td><td>{sg(s['sp_de'], 0)}</td><td>{sg(s.get('ch10_12m'), 0)}</td></tr>" for s in K["snapshot"])
        snap_rows = f"""<h3>Cross-country snapshot ({E(K.get('pap_date', ''))})</h3><div class="tablewrap"><table class="t"><thead><tr><th class="l">Country</th><th>2Y %</th><th>5Y %</th><th>10Y %</th><th>2s10s bp</th><th>10Y vs Bund bp</th><th>10Y Δ12M bp</th></tr></thead><tbody>{snap_rows}</tbody></table></div>"""
    sw_html = ""
    if K.get("swapped"):
        rows = []
        for ten in ("2Y", "5Y", "10Y"):
            grp = [r for r in K["swapped"] if r["tenor"] == ten or (ten == "2Y" and r["tenor"] == "3Y")]
            for r in sorted(grp, key=lambda x: -x["asw"]):
                rows.append(f"<tr{' class=\"hl\"' if r['code'] == 'PL' else ''}><td class='l'>{E(r['tenor'])}</td><td class='l'>{E(r['country'])}</td><td class='l'>{E(r['ccy'])}</td><td>{f(r['y'])}</td><td>{f(r['swap'])}</td>"
                            f"<td><b>{sg(r['asw'], 0)}</b></td><td>{f(r['to_pln'])}</td><td>{f(r['to_eur'])}</td><td>{sg(r['vs_pl_bp'], 0)}</td></tr>")
        sw_html = f"""<h3>Government bonds swapped into PLN / EUR (matched maturity, basis 0)</h3>
  <div class="grid2"><div><h3>10Y ASW by country (bp)</h3><div class="chart" id="coreAsw10"></div></div><div><h3>5Y ASW by country (bp)</h3><div class="chart" id="coreAsw5"></div></div></div>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Tenor</th><th class="l">Country</th><th class="l">Ccy</th><th>Yield %</th><th>Own swap %</th><th>ASW bp</th><th>Swapped → PLN %</th><th>Swapped → EUR %</th><th>vs POLGB bp</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <p class="small">{E(K.get('swap_note', ''))}</p>"""
    return f"""
<section class="card" id="core">
  <h2>Poland vs core markets <span class="tag">steepness · carry · central banks · FX-hedged</span></h2>
  <p class="lede">Bund curve: Bundesbank fitted yields ({E(K['bund_date'])}); UST par curve ({E(K['ust_date'])}); Polish curve: fitted POLGB curve. Carry+roll = (yield − local 3M rate) + duration × 1Y slide.</p>
  <h3>Central banks (as known on {E(F.get('info_cutoff', ''))})</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bank</th><th>Policy rate</th><th class="l">Last move</th><th class="l">Next meeting</th><th class="l">Stance</th><th class="l">What markets price</th><th>CPI</th><th>Real rate</th></tr></thead><tbody>{cb_rows}</tbody></table></div>
  <p class="small">{E(F.get('core_policy_note', ''))}</p>
  <div class="grid2" style="margin-top:6px">
    <div><h3>Yield curves</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>Poland (fitted)</span><span><i class="line" style="background:var(--s2)"></i>US Treasury</span><span><i class="line" style="background:var(--s3)"></i>Germany</span></div><div class="chart" id="coreCurves"></div></div>
    <div><h3>Carry + roll (bp/yr over local 3M)</h3><div class="legend"><span><i style="background:var(--s1)"></i>Carry</span><span><i style="background:var(--s2)"></i>Roll-down return</span><span>label: total (per duration year)</span></div><div class="chart" id="coreCarry"></div></div>
  </div>
  <div class="grid2">
    <div><h3>Poland spreads</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>PL−DE 10Y</span><span><i class="line" style="background:var(--s2)"></i>PL−US 10Y</span><span><i class="line" style="background:var(--s3)"></i>PL−DE 2Y</span></div><div class="chart" id="coreSpreads"></div></div>
    <div><h3>2s10s slope</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>Poland</span><span><i class="line" style="background:var(--s2)"></i>US</span><span><i class="line" style="background:var(--s3)"></i>Germany</span></div><div class="chart" id="coreSlopes"></div></div>
  </div>
  {snap_rows}
  <h3>FX-hedged yields</h3>
  <p class="small">Hedged yield = local yield + (rate of your currency − rate of the bond's currency). {E(K.get('hedge_method', ''))}. Bold = highest per tenor and currency.</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Tenor</th><th class="l">Bond</th><th>Local %</th><th>Hedged into PLN %</th><th>Hedged into EUR %</th><th>Hedged into USD %</th></tr></thead><tbody>{hm}</tbody></table></div>
  {sw_html}
  <div class="note"><b>Versus core, by the numbers.</b><ul class="tight">
    <li>10Y carry+roll: PL {f(cr[('PL', 10)]['total_bp'], 0)} / DE {f(cr[('DE', 10)]['total_bp'], 0)} / US {f(cr[('US', 10)]['total_bp'], 0)}bp per year; per duration year at 2Y: {f(cr[('PL', 2)]['per_dur'], 0)} / {f(cr[('DE', 2)]['per_dur'], 0)} / {f(cr[('US', 2)]['per_dur'], 0)}bp.</li>
    <li>Hedged into PLN, 1Y: Bund {f(hed[('DE', 1)]['PLN'])}%, UST {f(hed[('US', 1)]['PLN'])}% vs POLGB {f(hed[('PL', 1)]['local'])}%; 10Y: Bund {f(hed[('DE', 10)]['PLN'])}%, UST {f(hed[('US', 10)]['PLN'])}% vs POLGB {f(hed[('PL', 10)]['local'])}%.</li>
    <li>{E(F.get('core_text', ''))}</li></ul></div>
</section>"""


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "snapshots" / "2026-01-02")
