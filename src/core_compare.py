"""Poland vs core markets: curve steepness, carry & roll, spreads history, FX-hedged yields / basis.

Inputs:  data/core/core_rates.json (fetch_core.py), data/core/core_inputs.json (policy, CPI, swaps, FX),
         data/analytics/analytics_<date>.json, data/market/fixing_history.json, data/bonds_static.json
Output:  data/analytics/core_<date>.json
"""
from __future__ import annotations

import datetime as dt
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def interp(xs, ys, x):
    pts = sorted(zip(xs, ys))
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def par_md(y, T):
    """Modified duration of an annual-pay par bond (y in %)."""
    y = y / 100
    return (1 - (1 + y) ** -T) / y if y else T


UST_COLS = {"1 Mo": 1 / 12, "2 Mo": 2 / 12, "3 Mo": 0.25, "4 Mo": 4 / 12, "6 Mo": 0.5, "1 Yr": 1, "2 Yr": 2, "3 Yr": 3,
            "5 Yr": 5, "7 Yr": 7, "10 Yr": 10, "20 Yr": 20, "30 Yr": 30}


def main(asof: dt.date, snapdir=None):
    S_ = pathlib.Path(snapdir) if snapdir else None
    if S_:
        A = load(S_ / "analytics.json")
        C = load(S_ / "core_rates.json")
        I = load(S_ / "core_inputs.json")
        hist = load(S_ / "fixing_history.json")
        static = {b["ticker"]: dt.date.fromisoformat(b["maturity"]) for b in load(S_ / "bonds_static.json")["bonds"]}
    else:
        A = load(DATA / "analytics" / f"analytics_{asof:%Y%m%d}.json")
        C = load(DATA / "core" / "core_rates.json")
        I = load(DATA / "core" / "core_inputs.json")
        hist = load(DATA / "market" / "fixing_history.json")
        static = {b["ticker"]: dt.date.fromisoformat(b["maturity"]) for b in load(DATA / "bonds_static.json")["bonds"]}
    mm = A["market_inputs"]["money_market"]

    # ------------------------------------------------------------------ curve functions
    pl_grid = A["curve"]
    pl = lambda T: interp([g["t"] for g in pl_grid], [g["fit"] for g in pl_grid], T)
    bd = max(C["bund"]["10"])
    de_pts = {float(k): v[bd] for k, v in C["bund"].items() if bd in v}
    de = lambda T: interp(list(de_pts), list(de_pts.values()), T)
    ud = max(C["ust"])
    us_pts = {UST_COLS[k]: v for k, v in C["ust"][ud].items() if k in UST_COLS}
    us = lambda T: interp(list(us_pts), list(us_pts.values()), T)
    curves = {"PL": pl, "DE": de, "US": us}
    m3 = {"PL": mm["wibor_3m"], "DE": I["money"]["EUR"]["3m"], "US": I["money"]["USD"]["3m"]}

    grid = []
    for T in [0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]:
        row = {"t": T}
        for k, fn in curves.items():
            if k == "PL" and T > 21:
                continue
            if (k == "PL" and T < 0.5) or (k == "DE" and T < 1):
                row[k] = None
                continue
            row[k] = fn(T)
        grid.append(row)

    # ------------------------------------------------------------------ carry & roll by market/tenor
    cr = []
    for k, fn in curves.items():
        for T in (2, 5, 10):
            y = fn(T)
            roll = (fn(T) - fn(T - 1)) * 100  # bp over 1Y if the curve is unchanged
            D1 = par_md(y, T - 1)
            carry = (y - m3[k]) * 100
            tot_bp = carry + D1 * roll   # ~ excess return over local 3M cash, bp per year
            D = par_md(y, T)
            cr.append(dict(mkt=k, T=T, y=y, m3=m3[k], carry_bp=carry, roll_bp=roll, roll_ret_bp=D1 * roll,
                           total_bp=tot_bp, md=D, per_dur=tot_bp / D))

    # ------------------------------------------------------------------ PAP cross-country snapshot
    pap = C.get("pap") or {"data": {}, "date": None, "url": None}
    names = {"Polska": "Poland", "Niemcy": "Germany", "USA": "United States", "Wielka Brytania": "United Kingdom",
             "Francja": "France", "Włochy": "Italy", "Hiszpania": "Spain", "Czechy": "Czechia", "Węgry": "Hungary",
             "Japonia": "Japan"}
    snap = []
    de10 = pap["data"]["Niemcy"]["10Y"][0] if "Niemcy" in pap["data"] else None
    for pl_name, en in names.items():
        d = pap["data"].get(pl_name)
        if not d:
            continue
        short = d.get("2Y") or d.get("3Y")
        s_lab = "2Y" if d.get("2Y") else "3Y"
        y10 = d["10Y"]
        snap.append(dict(country=en, short_tenor=s_lab, y2=short[0], y5=d["5Y"][0], y10=y10[0],
                         s2s10=(y10[0] - short[0]) * 100, s5s10=(y10[0] - d["5Y"][0]) * 100,
                         sp_de=(y10[0] - de10) * 100, ch10_1m=(y10[0] - y10[3]) * 100 if y10[3] is not None else None,
                         ch10_3m=(y10[0] - y10[4]) * 100 if y10[4] is not None else None,
                         ch10_12m=(y10[0] - y10[5]) * 100 if y10[5] is not None else None,
                         ch2_12m=(short[0] - short[5]) * 100 if short[5] is not None else None,
                         slope_12m_ago=(y10[5] - short[5]) * 100 if y10[5] is not None and short[5] is not None else None,
                         cb=I.get("policy", {}).get(en)))

    # ------------------------------------------------------------------ spread history (PL CMT from fixings)
    def pl_cmt(day, T):
        d0 = dt.date.fromisoformat(day)
        pts = [((static[t] - d0).days / 365.25, v[1]) for t, v in hist[day].items()
               if t in static and v and v[1] is not None and not t.startswith("_")]
        pts = [p for p in pts if p[0] > 0.9]
        return interp([p[0] for p in pts], [p[1] for p in pts], T) if len(pts) > 5 else None

    hs = []
    for day in sorted(hist):
        if day not in C["bund"]["10"] or day not in C["ust"]:
            continue
        u = C["ust"][day]
        p2, p10 = pl_cmt(day, 2), pl_cmt(day, 10)
        if p2 is None or p10 is None:
            continue
        hs.append(dict(d=day, pl2=p2, pl10=p10, de2=C["bund"]["2"][day], de10=C["bund"]["10"][day],
                       us2=u.get("2 Yr"), us10=u.get("10 Yr")))

    # ------------------------------------------------------------------ FX hedge pickups
    # Market EUR/PLN forward points -> FX-implied PLN rate (OIS-consistent); USD via Fed funds OIS.
    fx = I.get("fx", {})
    if fx.get("fwd_points"):
        S = fx["eurpln_spot"]
        mid = lambda k: sum(fx["fwd_points"][k]) / 2 / 1e4
        fs1 = 1 + mid("1Y") / S                       # F/S over 1Y (365 days from spot)
        fs3 = 1 + mid("3M") / S
        r_eur1 = I["money"]["EUR"]["ois"]["1"] * 365 / 360          # ACT/360 -> annual-ish
        r_usd1 = I["money"]["USD"]["ois"]["1"] * 365 / 360
        r_pln1 = ((1 + r_eur1 / 100) * fs1 - 1) * 100                 # FX-implied PLN 1Y rate
        hedge_method = "1Y EUR/PLN forward points (market); USD via Fed funds OIS"
        p3m = (fs3 - 1) * 365 / 92 * 100
    else:  # no forward points available point-in-time: covered parity on 1Y money/OIS rates
        h = I["hedge_rates_1y"]
        r_pln1, r_eur1, r_usd1 = h["PLN"], h["EUR"], h["USD"]
        hedge_method = h.get("method", "covered interest parity on 1Y rates")
        p3m = None
    r1 = {"PLN": r_pln1, "EUR": r_eur1, "USD": r_usd1}
    pick = dict(
        eurpln_1y_market=r_pln1 - r_eur1,
        eurpln_3m_market=p3m,
        eurpln_3m_ibor=(((1 + mm["wibor_3m"] / 100 * 92 / 365) / (1 + I["money"]["EUR"]["3m"] / 100 * 92 / 360)) - 1) * 365 / 92 * 100,
        usdpln_1y=r_pln1 - r_usd1, pln_implied_1y=r_pln1, eur_ois_1y=r_eur1, usd_ois_1y=r_usd1)
    ccy = {"PL": "PLN", "DE": "EUR", "US": "USD"}
    hedged = []
    for T in (1, 2, 5, 10):
        for asset, fn in curves.items():
            y = fn(T)
            row = dict(T=T, asset=asset, local=y)
            for base in ("PLN", "EUR", "USD"):
                row[base] = y + (r1[base] - r1[ccy[asset]])
            hedged.append(row)

    # ------------------------------------------------------------------ Bund swapped into PLN (matched maturity)
    eur_irs = I.get("eur_irs", {}).get("pillars")
    pln_irs = A["market_inputs"]["irs"]["pillars"]
    swap_to_pln = []
    if eur_irs:
        for T in ("2", "5", "10"):
            Tf = float(T)
            bund_y = de(Tf)
            bund_asw = (bund_y - eur_irs[T]) * 100
            pl_y = pl(Tf)
            pl_asw = (pl_y - pln_irs[T]) * 100
            synth = pln_irs[T] + bund_asw / 100  # PLN fixed via EUR IRS + CCS (basis 0) + PLN IRS
            swap_to_pln.append(dict(T=Tf, bund=bund_y, eur_irs=eur_irs[T], bund_asw=bund_asw, pln_irs=pln_irs[T],
                                    synth_pln=synth, polgb=pl_y, pl_asw=pl_asw, adv_pl_bp=(pl_y - synth) * 100))

    # ------------------------------------------------------------------ Poland EUR Eurobonds vs POLGB (local vs hard currency)
    from analytics import irs_curve
    pirs = irs_curve(A["market_inputs"])
    ex = sorted((float(k), v) for k, v in eur_irs.items()) if eur_irs else []
    eirs = lambda T: interp([e[0] for e in ex], [e[1] for e in ex], T)
    eurobonds = []
    for eb in I.get("pl_eurobonds", []):
        T = eb["T"]
        asw_e = (eb["yield"] - eirs(T)) * 100
        pl_y = pl(T)
        asw_p = (pl_y - pirs(T)) * 100
        eurobonds.append(dict(name=eb["name"], T=T, eur_yield=eb["yield"], eur_swap=eirs(T), asw_eur=asw_e, bund=de(T),
                              sp_bund=(eb["yield"] - de(T)) * 100, polgb=pl_y, pln_irs=pirs(T), asw_pln=asw_p,
                              local_premium=asw_p - asw_e, polgb_hedged_eur=pl_y - (r_pln1 - r_eur1),
                              hedged_minus_eurobond=(pl_y - (r_pln1 - r_eur1) - eb["yield"]) * 100, issue=eb["issue"]))

    # ------------------------------------------------------------------ govvies swapped into PLN / EUR (matched maturity)
    SW = load(S_ / "swaps.json") if (S_ and (S_ / "swaps.json").exists()) else (None if S_ else load(DATA / "core" / "swaps.json"))

    def swap_fn(ccy, col=0):
        pts = sorted((float(k), v[col]) for k, v in SW[ccy]["tenors"].items() if len(v) > col and v[col] is not None)
        if len(pts) < 2:
            return lambda T: None
        return lambda T: interp([p[0] for p in pts], [p[1] for p in pts], T)

    mk = {"Poland": ("PLN", "PL"), "Germany": ("EUR", "DE"), "France": ("EUR", "FR"), "Italy": ("EUR", "IT"),
          "Spain": ("EUR", "ES"), "Czechia": ("CZK", "CZ"), "Hungary": ("HUF", "HU"), "United States": ("USD", "US")}
    pap_pl = {"Poland": "Polska", "Germany": "Niemcy", "France": "Francja", "Italy": "Włochy", "Spain": "Hiszpania",
              "Czechia": "Czechy", "Hungary": "Węgry", "United States": "USA"}
    PCOL = {"d6": 1, "m1": 3, "m12": 5}          # PAP columns: now, 1D(=6 Nov), 5D, 1M, 3M, 12M
    swapped = []
    PCOL = I.get("pap_cols", PCOL)
    pln0, eur0 = (swap_fn("PLN"), swap_fn("EUR")) if SW else (None, None)
    for ctry, (ccy, code) in (mk.items() if SW and pap["data"] else []):
        if pap_pl[ctry] not in pap["data"] or ccy not in SW:
            continue
        d = pap["data"][pap_pl[ctry]]
        for lab in ("2Y", "3Y", "5Y", "10Y"):
            if lab not in d or (lab == "3Y" and "2Y" in d):
                continue
            T = float(lab[:-1])
            y6, y1m, y12 = d[lab][PCOL["d6"]], d[lab][PCOL["m1"]], d[lab][PCOL["m12"]]
            s0, s1m, s12 = swap_fn(ccy, 0)(T), swap_fn(ccy, 2)(T), swap_fn(ccy, 3)(T)
            if y6 is None or s0 is None:
                continue
            asw = (y6 - s0) * 100
            swapped.append(dict(country=ctry, code=code, ccy=ccy, tenor=lab, T=T, y=y6, swap=s0, asw=asw,
                                asw_1m=(y1m - s1m) * 100 if (y1m is not None and s1m is not None) else None,
                                asw_12m=(y12 - s12) * 100 if (y12 is not None and s12 is not None) else None,
                                to_pln=pln0(T) + asw / 100, to_eur=eur0(T) + asw / 100))
    for r in swapped:
        pl_same = next((x for x in swapped if x["code"] == "PL" and (x["T"] == r["T"] or (r["T"] == 3 and x["T"] == 2))), None)
        r["vs_pl_bp"] = r["asw"] - pl_same["asw"] if pl_same else None
    swap_meta = {c: dict(dates=SW[c].get("dates"), url=SW[c].get("url")) for c in ("PLN", "EUR", "CZK", "HUF", "USD") if SW and c in SW}

    # ------------------------------------------------------------------ peers FX-hedged into PLN (rolling 1Y IBOR hedge; used when no swap curves)
    hedged_peers = []
    ib = I.get("ibor_1y")
    if ib and pap["data"]:
        mkp = {"Poland": ("PLN", "Polska"), "Germany": ("EUR", "Niemcy"), "France": ("EUR", "Francja"), "Italy": ("EUR", "Włochy"),
               "Spain": ("EUR", "Hiszpania"), "Czechia": ("CZK", "Czechy"), "Hungary": ("HUF", "Węgry"), "United States": ("USD", "USA")}
        col = I.get("pap_cols", {}).get("d6", 0)
        for ctry, (ccy, pn) in mkp.items():
            d = pap["data"].get(pn)
            if not d or ccy not in ib:
                continue
            for lab in ("2Y", "3Y", "5Y", "10Y"):
                if lab not in d or (lab == "3Y" and "2Y" in d) or d[lab][col] is None:
                    continue
                y = d[lab][col]
                pick_pln = ib["PLN"] - ib[ccy]
                hedged_peers.append(dict(country=ctry, ccy=ccy, tenor=lab, y=y, hedge_pln=pick_pln, to_pln=y + pick_pln,
                                         to_eur=y + (ib["EUR"] - ib[ccy])))
        for r in hedged_peers:
            pl_same = next((x for x in hedged_peers if x["country"] == "Poland" and (x["tenor"] == r["tenor"] or (r["tenor"] == "3Y" and x["tenor"] == "2Y"))), None)
            r["vs_pl_bp"] = (r["to_pln"] - pl_same["to_pln"]) * 100 if pl_same else None

    out = dict(asof=asof.isoformat(), bund_date=bd, ust_date=ud, grid=grid, carry_roll=cr, snapshot=snap,
               spread_hist=hs, hedged=hedged, r3=m3, pick=pick, r1=r1, hedge_method=hedge_method, swap_note=I.get("swap_note", ""), swap_to_pln=swap_to_pln, eurobonds=eurobonds, swapped=swapped, swap_meta=swap_meta, hedged_peers=hedged_peers, ibor_1y=ib, inputs=I, pap_date=pap["date"],
               pap_url=pap["url"], estr=C.get("estr"), sofr=C.get("sofr"), euribor=C.get("euribor"))
    p = (S_ / "core.json") if S_ else DATA / "analytics" / f"core_{asof:%Y%m%d}.json"
    p.write_text(json.dumps(out, indent=1))
    print("wrote", p)
    for r in cr:
        print(f"{r['mkt']} {r['T']:>2}Y y={r['y']:.2f} 3m={r['m3']:.2f} carry={r['carry_bp']:6.0f} roll={r['roll_bp']:5.1f}bp "
              f"rollret={r['roll_ret_bp']:5.0f} tot={r['total_bp']:6.0f} MD={r['md']:.2f} per_dur={r['per_dur']:5.0f}")
    for h in hedged:
        print(f"T={h['T']:>2} {h['asset']} local={h['local']:.2f}  inPLN={h['PLN']:.2f} inEUR={h['EUR']:.2f} inUSD={h['USD']:.2f}")
    print("pickups", {k: (round(v, 3) if v is not None else None) for k, v in pick.items()})
    for x in swap_to_pln:
        print({k: round(v, 2) if isinstance(v, float) else v for k, v in x.items()})
    for x in eurobonds:
        print({k: round(v, 2) if isinstance(v, float) else v for k, v in x.items()})
    print("hist", hs[0], hs[-1], len(hs))
    for r in swapped:
        print(f"{r['code']} {r['tenor']:>3} y={r['y']:.2f} swap={r['swap']:.2f} ASW={r['asw']:6.0f} (1m {r['asw_1m']:5.0f}, 12m {r['asw_12m']:5.0f}) "
              f"toPLN={r['to_pln']:.2f} toEUR={r['to_eur']:.2f} vsPL={r['vs_pl_bp']:6.0f}")


if __name__ == "__main__":
    main(dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 9),
         sys.argv[sys.argv.index("--snap") + 1] if "--snap" in sys.argv else None)
