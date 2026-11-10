"""Floaters (WZ = 6M WIBOR flat, NZ = compounded POLSTR flat) and linkers (IZ, CPI-indexed) analytics.

Floaters: discount margin over a single-curve 6M WIBOR projection bootstrapped from the PLN swap curve,
spread duration, effective rate duration, comparison with the asset-swap spread of fixed POLGBs at the
same maturity. NZ uses WIBOR forwards minus a WIBOR-POLSTR basis (realised over the last NZ period).
Linkers: real yield from real (unindexed) prices, breakeven inflation vs the fitted nominal curve,
12M carry vs nominals under CPI scenarios.

Usage: python src/floaters_linkers.py 2026-11-09  ->  data/analytics/fl_<date>.json
"""
from __future__ import annotations

import datetime as dt
import json
import math
import pathlib
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from analytics import DATA, Bond, add_bdays, add_months, irs_curve  # noqa: E402

FLOATERS = {  # ticker: (maturity, coupon months, current coupon %, current period start, outstanding PLN bn)
    "WZ1127": ("2027-11-25", (5, 11), 3.96, "2026-05-25", 40.59),
    "WZ0528": ("2028-05-25", (5, 11), 3.96, "2026-05-25", 28.26),
    "WZ1128": ("2028-11-25", (5, 11), 3.96, "2026-05-25", 45.07),
    "WZ1129": ("2029-11-25", (5, 11), 3.96, "2026-05-25", 56.49),
    "WZ0330": ("2030-03-25", (3, 9), 3.88, "2026-09-25", 56.47),
    "WZ0930": ("2030-09-25", (3, 9), 3.88, "2026-09-25", 43.78),
    "WZ1131": ("2031-11-25", (5, 11), 3.96, "2026-05-25", 24.39),
    "WZ0533": ("2033-05-25", (5, 11), 3.96, "2026-05-25", 3.45),
    "NZ0928": ("2028-09-25", (3, 9), None, "2026-09-25", 13.67),
    "NZ0331": ("2031-03-25", (3, 9), None, "2026-09-25", 60.30),
    "NZ0332": ("2032-03-25", (3, 9), None, "2026-09-25", 7.08),
    "NZ0936": ("2036-09-25", (3, 9), None, "2026-09-25", 3.35),
}
LINKERS = {"IZ0831": ("2031-08-25", 1.75, 9.92), "IZ0836": ("2036-08-25", 2.00, 24.22)}
POLSTR_BASIS = 0.35       # WIBOR 6M minus realised compounded POLSTR (NZ period Mar-Sep 2026: 3.568% vs WIBOR6M ~3.9-4.0%)
NZ_RUNNING = 3.60         # assumed compounded POLSTR for the running NZ period (O/N 3.77%, 3M compounded 3.52%)


def bootstrap(mi, bump=0.0):
    """Annual DFs from PLN par swaps (annual fixed vs 6M WIBOR, single curve). Returns DF(t) via log-linear interp."""
    irs = irs_curve(mi)
    w6 = mi["money_market"]["wibor_6m"] + bump * 100
    dfs = {0.0: 1.0, 0.5: 1 / (1 + (w6 / 100) * 0.5)}
    annuity = 0.0
    for T in range(1, 31):
        S = (irs(float(T)) + bump * 100) / 100
        df = (1 - S * annuity) / (1 + S)
        dfs[float(T)] = df
        annuity += df
    ts = sorted(dfs)
    lg = [math.log(dfs[t]) for t in ts]

    def DF(t):
        if t <= 0:
            return 1.0
        return math.exp(np.interp(t, ts, lg)) if t <= ts[-1] else math.exp(lg[-1] + (lg[-1] - lg[-2]) * (t - ts[-1]))
    return DF


def schedule(mat, months, settle):
    """Coupon dates after settle (25th of the coupon months) up to maturity."""
    d = dt.date.fromisoformat(mat)
    out = []
    while d > settle:
        out.append(d)
        d = add_months(d, -6)
    return d, out[::-1]   # previous coupon date, future dates


def price_floater(tk, DF, settle, dm, basis=0.0):
    mat, months, cpn, start, _ = FLOATERS[tk]
    prev, dates = schedule(mat, months, settle)
    yf = lambda d: (d - settle).days / 365.0
    pv, sd = 0.0, 0.0
    for i, d in enumerate(dates):
        t = yf(d)
        if i == 0:
            rate = cpn if cpn is not None else NZ_RUNNING
        else:
            t0 = yf(dates[i - 1])
            tau = t - t0
            rate = (DF(t0) / DF(t) - 1) / tau * 100 - basis
        cf = rate / 2 + (100.0 if d == dates[-1] else 0.0)
        disc = DF(t) * math.exp(-dm * t)
        pv += cf * disc
        sd += t * cf * disc
    return pv, sd / pv


def accrued_floater(tk, settle):
    mat, months, cpn, start, _ = FLOATERS[tk]
    prev, dates = schedule(mat, months, settle)
    rate = cpn if cpn is not None else NZ_RUNNING
    return rate / 2 * (settle - prev).days / (dates[0] - prev).days


def interp(xs, ys, x):
    return float(np.interp(x, xs, ys))


def main(asof: dt.date, snap=None):
    global FLOATERS, LINKERS, POLSTR_BASIS, NZ_RUNNING
    basis_note = "realised WIBOR-POLSTR gap over the last NZ coupon period"
    cpi_sc = {"3.0%": 3.0, "4.2% (NBP 2027)": 4.2, "5.0%": 5.0}
    if snap:
        snap = pathlib.Path(snap)
        T = json.loads((snap / "floaters.json").read_text())
        FLOATERS = {k: (v["maturity"], tuple(v["months"]), v["coupon"], v["period_start"], v.get("outstanding_bn")) for k, v in T["floaters"].items()}
        LINKERS = {k: (v["maturity"], v["real_coupon"], v.get("outstanding_bn")) for k, v in T["linkers"].items()}
        POLSTR_BASIS, NZ_RUNNING = T["polstr_basis"], T["nz_running"]
        basis_note = T.get("basis_note", basis_note)
        cpi_sc = T.get("cpi_scenarios", cpi_sc)
        A = json.loads((snap / "analytics.json").read_text())
        mk = json.loads((snap / f"bondspot_{asof:%Y%m%d}.json").read_text())
        hist = json.loads((snap / "fixing_history.json").read_text())
    else:
        A = json.loads((DATA / "analytics" / f"analytics_{asof:%Y%m%d}.json").read_text())
        mk = json.loads((DATA / "market" / f"bondspot_{asof:%Y%m%d}.json").read_text())
        hist = json.loads((DATA / "market" / "fixing_history.json").read_text())
    mi = A["market_inputs"]
    settle = add_bdays(asof, 2)
    DF = bootstrap(mi)
    DFb = bootstrap(mi, bump=0.0001)
    irs = irs_curve(mi)
    fix = {f["ticker"]: f for f in mk["fixing"]}
    qts = {q["ticker"]: q for q in mk["quotes"]}
    fixed = [b for b in A["bonds"] if b["ttm"] > 0.9]
    fx_t = [b["ttm"] for b in fixed]
    fx_asw = [b["asw_bp"] for b in fixed]
    fund = A["funding"]

    def px(tk):
        f = fix.get(tk)
        if f and f.get("fix_price"):
            return f["fix_price"], "fixing", (f["ask"] - f["bid"]) if f.get("bid") and f.get("ask") else None
        q = qts.get(tk)
        if q and q.get("bid") and q.get("ask"):
            return (q["bid"] + q["ask"]) / 2, f"mid {mk['quotes_date']}", q["ask"] - q["bid"]
        return None, None, None

    fl = []
    for tk, (mat, months, cpn, start, out_bn) in FLOATERS.items():
        clean, src, ba = px(tk)
        if clean is None:
            continue
        basis = POLSTR_BASIS if tk.startswith("NZ") else 0.0
        ai = accrued_floater(tk, settle)
        dirty = clean + ai
        dm = brentq(lambda s: price_floater(tk, DF, settle, s, basis)[0] - dirty, -0.05, 0.10)
        p0, sdur = price_floater(tk, DF, settle, dm, basis)
        p_up, _ = price_floater(tk, DFb, settle, dm, basis)
        rate_dur = -(p_up - p0) / p0 / 0.0001
        T = (dt.date.fromisoformat(mat) - settle).days / 365.25
        dm_bp = dm * 1e4
        dm_wibor_eq = dm_bp - basis * 100
        fixed_asw = interp(fx_t, fx_asw, T)
        # 3-month price change from fixing history (no curve history -> price only)
        d3 = sorted(d for d in hist if d <= (asof - dt.timedelta(days=91)).isoformat())
        p3 = hist[d3[-1]].get(tk, [None])[0] if d3 else None
        fl.append(dict(ticker=tk, index="POLSTR" if tk.startswith("NZ") else "WIBOR 6M", maturity=mat, ttm=T, clean=clean, accrued=ai,
                       src=src, bid_ask=ba, outstanding_bn=out_bn, current_coupon=cpn if cpn is not None else NZ_RUNNING,
                       dm_bp=dm_bp, dm_wibor_eq_bp=dm_wibor_eq, spread_dur=sdur, rate_dur=rate_dur,
                       fixed_asw_bp=fixed_asw, vs_fixed_bp=dm_wibor_eq - fixed_asw, dm_per_sdur=dm_wibor_eq / sdur,
                       carry_12m=(mi["money_market"]["wibor_6m"] - basis + dm_bp / 100) - fund,
                       px_3m_ago=p3, px_chg_3m=(clean - p3) if p3 else None))

    # ---------------- linkers
    grid = A["curve"]
    nom = lambda T: interp([g["t"] for g in grid], [g["fit"] for g in grid], T)
    lk = []
    for tk, (mat, rc, out_bn) in LINKERS.items():
        clean, src, ba = px(tk)
        if clean is None:
            continue
        b = Bond(tk, "", rc, dt.date.fromisoformat(mat))
        ry = b.yield_from_clean(clean, settle) * 100
        r = b.risk(ry / 100, settle)
        T = b.ttm(settle)
        n = nom(T)
        be = ((1 + n / 100) / (1 + ry / 100) - 1) * 100
        # nearest nominal for the 12M comparison
        near = min(fixed, key=lambda x: abs(x["ttm"] - T))
        real_carry = (b.clean_from_yield(ry / 100, add_months(settle, 12)) - clean + rc) / (clean + b.accrued(settle)) * 100
        sc = {k: real_carry + v for k, v in cpi_sc.items()}
        lk.append(dict(ticker=tk, maturity=mat, ttm=T, real_coupon=rc, clean=clean, src=src, bid_ask=ba, outstanding_bn=out_bn,
                       real_yield=ry, real_mod=r["mod"], nominal_fit=n, breakeven=be, nominal_peer=near["ticker"],
                       nominal_peer_12m=near["h12"]["total"], real_carry_12m=real_carry, total_12m=sc,
                       vs_nominal_12m={k: v - near["h12"]["total"] for k, v in sc.items()},
                       be_bid_ask_bp=(ba / r["mod"] * 100) if ba else None))

    out = dict(asof=asof.isoformat(), settle=settle.isoformat(), floaters=fl, linkers=lk, polstr_basis=POLSTR_BASIS,
               nz_running=NZ_RUNNING, basis_note=basis_note, wibor6m=mi["money_market"]["wibor_6m"], funding=fund,
               fwd_6m=[dict(t=t, f=(DF(t) / DF(t + 0.5) - 1) / 0.5 * 100) for t in np.arange(0, 10.01, 0.5).tolist()])
    p = (snap / "fl.json") if snap else DATA / "analytics" / f"fl_{asof:%Y%m%d}.json"
    p.write_text(json.dumps(out, indent=1))
    print("wrote", p)
    print(f"{'tk':7}{'ttm':>6}{'clean':>8}{'DM':>7}{'DMw':>7}{'sDur':>6}{'rDur':>6}{'fixASW':>8}{'vsFix':>7}{'DM/sD':>7}{'carry':>7}")
    for x in fl:
        print(f"{x['ticker']:7}{x['ttm']:6.2f}{x['clean']:8.2f}{x['dm_bp']:7.0f}{x['dm_wibor_eq_bp']:7.0f}{x['spread_dur']:6.2f}{x['rate_dur']:6.2f}"
              f"{x['fixed_asw_bp']:8.0f}{x['vs_fixed_bp']:7.0f}{x['dm_per_sdur']:7.1f}{x['carry_12m']:7.2f}")
    for x in lk:
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in x.items() if k not in ("total_12m", "vs_nominal_12m")},
              {k: round(v, 2) for k, v in x["vs_nominal_12m"].items()})
    print("fwd 6M WIBOR", [(round(f["t"], 1), round(f["f"], 2)) for f in out["fwd_6m"][:8]])


if __name__ == "__main__":
    main(dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 9),
         sys.argv[sys.argv.index("--snap") + 1] if "--snap" in sys.argv else None)
