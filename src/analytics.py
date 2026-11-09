"""POLGB analytics: pricing, duration, curve fit, rich/cheap, ASW, carry/roll split, index stats.

Conventions (Polish fixed-rate govvies): annual coupon on the 25th of the maturity month,
Act/Act (ICMA) accrual, annual-compounding street yield, clean prices, T+2 settlement.
OK-series are zero-coupon and use the same annual-period yield convention.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import pathlib
from dataclasses import dataclass, field

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, least_squares

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PL_HOLIDAYS = {dt.date(2026, 11, 11), dt.date(2026, 12, 24), dt.date(2026, 12, 25), dt.date(2026, 12, 26),
               dt.date(2027, 1, 1), dt.date(2027, 1, 6)}


def add_bdays(d: dt.date, n: int) -> dt.date:
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in PL_HOLIDAYS:
            n -= 1
    return d


def add_months(d: dt.date, m: int) -> dt.date:
    y, mo = divmod(d.month - 1 + m, 12)
    y += d.year
    mo += 1
    day = min(d.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1])
    return dt.date(y, mo, day)


def yf(d0: dt.date, d1: dt.date) -> float:
    return (d1 - d0).days / 365.25


# --------------------------------------------------------------------------- bond math
@dataclass
class Bond:
    ticker: str
    isin: str
    coupon: float
    maturity: dt.date

    @property
    def is_zero(self) -> bool:
        return self.coupon == 0.0

    def schedule(self, settle: dt.date):
        """(previous anniversary, [future coupon/anniversary dates])."""
        ds, d = [], self.maturity
        while d > settle:
            ds.append(d)
            d = d.replace(year=d.year - 1)
        return d, ds[::-1]

    def accrued(self, settle: dt.date) -> float:
        if self.is_zero:
            return 0.0
        prev, ds = self.schedule(settle)
        return self.coupon * (settle - prev).days / (ds[0] - prev).days

    def flows(self, settle: dt.date):
        """[(t_years_icma, date, amount)] for flows strictly after settle."""
        prev, ds = self.schedule(settle)
        f = (ds[0] - settle).days / (ds[0] - prev).days
        out = []
        for i, d in enumerate(ds):
            amt = (0.0 if self.is_zero else self.coupon) + (100.0 if d == self.maturity else 0.0)
            if amt:
                out.append((f + i, d, amt))
        return out

    def dirty_from_yield(self, y: float, settle: dt.date) -> float:
        return sum(a / (1 + y) ** t for t, _, a in self.flows(settle))

    def clean_from_yield(self, y: float, settle: dt.date) -> float:
        return self.dirty_from_yield(y, settle) - self.accrued(settle)

    def yield_from_clean(self, clean: float, settle: dt.date) -> float:
        return brentq(lambda y: self.clean_from_yield(y, settle) - clean, -0.5, 1.0, xtol=1e-12)

    def risk(self, y: float, settle: dt.date):
        fl = self.flows(settle)
        pv = [a / (1 + y) ** t for t, _, a in fl]
        p = sum(pv)
        mac = sum(t * v for (t, _, _), v in zip(fl, pv)) / p
        conv = sum(t * (t + 1) * v for (t, _, _), v in zip(fl, pv)) / (p * (1 + y) ** 2)
        return dict(dirty=p, mac=mac, mod=mac / (1 + y), conv=conv)

    def ttm(self, settle: dt.date) -> float:
        return yf(settle, self.maturity)


# --------------------------------------------------------------------------- curve fit
def nss_zero(tau, p):
    """Nelson-Siegel-Svensson continuously-compounded zero rate (decimal)."""
    b0, b1, b2, b3, l1, l2 = p
    tau = np.maximum(np.asarray(tau, float), 1e-6)
    x1, x2 = tau / l1, tau / l2
    f1 = (1 - np.exp(-x1)) / x1
    f2 = f1 - np.exp(-x1)
    f3 = (1 - np.exp(-x2)) / x2 - np.exp(-x2)
    return b0 + b1 * f1 + b2 * f2 + b3 * f3


@dataclass
class Curve:
    params: np.ndarray

    def z(self, tau):
        return nss_zero(tau, self.params)

    def price(self, bond: Bond, settle: dt.date, spread: float = 0.0, shift_years: float = 0.0) -> float:
        """Dirty price discounting each flow at z(tau) + spread (cont. comp). tau measured Act/365.25
        from settle (+shift: horizon pricing with the same curve-by-maturity)."""
        tot = 0.0
        for _, d, a in bond.flows(settle):
            tau = yf(settle, d)
            if tau <= 0:
                continue
            tot += a * math.exp(-(float(self.z(tau)) + spread) * tau)
        return tot

    def par_yield(self, T: float) -> float:
        """Annual-pay par yield for a T-year bullet (for plotting a smooth 'fitted yield' line)."""
        n = max(1, int(math.ceil(T - 1e-9)))
        ts = [T - k for k in range(n)][::-1]
        ts = [t for t in ts if t > 0]
        df = [math.exp(-float(self.z(t)) * t) for t in ts]
        acc = ts[0]  # fraction of first period
        # dirty par-ish: coupon c s.t. sum(c*df) + df_T = 1 + c*(1-acc)  (clean = 100)
        return (1 - df[-1]) / (sum(df) - (1 - acc)) * 100


def fit_curve(bonds, cleans, settle, weights=None, anchors=()):
    """anchors: [(tau_years, annual_zero_rate_pct, weight)] pseudo-observations (front-end money-market anchor)."""
    targets = []
    for b, c in zip(bonds, cleans):
        y = b.yield_from_clean(c, settle)
        r = b.risk(y, settle)
        targets.append((b, c + b.accrued(settle), r["dirty"] * r["mod"]))
    w = np.ones(len(bonds)) if weights is None else np.asarray(weights, float)

    def resid(p):
        cv = Curve(p)
        r = [(cv.price(b, settle) - P) / dv * 1e4 for b, P, dv in targets]  # in bp of yield
        a = [(float(cv.z(t)) - math.log(1 + z / 100)) * 1e4 * aw for t, z, aw in anchors]
        return np.concatenate([np.array(r) * w, np.array(a, float)])

    p0 = np.array([0.060, -0.022, 0.0, 0.0, 1.5, 6.0])
    lb = [0.0, -0.15, -0.3, -0.3, 0.2, 2.5]
    ub = [0.15, 0.15, 0.3, 0.3, 6.0, 30.0]
    best = None
    for l1 in (0.7, 1.5, 3.0):
        for l2 in (4.0, 8.0, 15.0):
            p0[4], p0[5] = l1, l2
            r = least_squares(resid, p0, bounds=(lb, ub), loss="soft_l1", f_scale=3.0)
            if best is None or r.cost < best.cost:
                best = r
    return Curve(best.x)


def zspread(bond, curve, dirty, settle):
    return brentq(lambda s: curve.price(bond, settle, s) - dirty, -0.05, 0.05, xtol=1e-12)


# --------------------------------------------------------------------------- IRS curve
def irs_curve(mi):
    piv = {float(k): v for k, v in mi["irs"]["pillars"].items()}
    xs = [0.5] + sorted(piv)
    ys = [mi["money_market"]["wibor_6m"]] + [piv[k] for k in sorted(piv)]
    f = PchipInterpolator(xs, ys, extrapolate=False)
    slope = (piv[10.0] - piv[5.0]) / 5.0 * 0.5

    def irs(T):
        if T <= xs[0]:
            return ys[0]
        if T <= xs[-1]:
            return float(f(T))
        return ys[-1] + slope * (T - xs[-1]) * (1 - (T - xs[-1]) / 60)  # gently damped
    return irs


# --------------------------------------------------------------------------- carry / roll
def horizon_split(bond, clean0, y0, curve, zs, settle, months, fund):
    """Decompose expected horizon return (per 100 nominal; % of dirty price) under an unchanged curve.

    coupon   : coupon income accrued + paid over the horizon
    pull     : clean-price drift toward par at the bond's own constant yield (pull-to-par)
               (coupon + pull = 'yield carry' ~= YTM x h)
    roll     : extra price gain from rolling down the (unchanged) fitted curve, residual z-spread held
    funding  : cost of financing the dirty price at the repo/funding rate
    """
    H = add_months(settle, months)
    h = (H - settle).days / 365.0
    d0 = clean0 + bond.accrued(settle)
    paid = sum(a for _, d, a in bond.flows(settle) if d <= H)
    pct = lambda x: x / d0 * 100
    if bond.maturity <= H:  # matures inside the horizon: redeem at par, park cash at the funding rate
        cpn_paid = paid - 100.0
        reinv = (100.0 + cpn_paid) * fund / 100 * (H - bond.maturity).days / 365.0
        coupon_inc = cpn_paid - bond.accrued(settle) + reinv
        pull = 100.0 - clean0
        funding = d0 * fund / 100 * h
        tot = pct(coupon_inc + pull)
        net = tot - pct(funding)
        return dict(months=months, coupon=pct(coupon_inc), pull=pct(pull), roll=0.0, total=tot,
                    funding=pct(funding), net=net, roll_bp=0.0, breakeven_bp=None,
                    ann_total=tot / h, ann_net=net / h, matures=True)
    clean_H_y = bond.clean_from_yield(y0, H)
    ai_H = bond.accrued(H)
    coupon_inc = (ai_H - bond.accrued(settle)) + (paid if not bond.is_zero else 0.0)
    pull = clean_H_y - clean0
    dirty_H_roll = curve.price(bond, H, zs)
    dirty_H_y = clean_H_y + ai_H
    roll = dirty_H_roll - dirty_H_y
    funding = d0 * fund / 100 * h
    pct = lambda x: x / d0 * 100
    tot = pct(coupon_inc + pull + roll)
    # yield the bond will have at H under the rolled curve -> horizon duration for breakeven
    y_H = bond.yield_from_clean(dirty_H_roll - ai_H, H)
    md_H = bond.risk(y_H, H)["mod"]
    net = tot - pct(funding)
    return dict(months=months, coupon=pct(coupon_inc), pull=pct(pull), roll=pct(roll), total=tot,
                funding=pct(funding), net=net, roll_bp=(y0 - y_H) * 1e4,
                breakeven_bp=net / md_H * 100 if md_H > 0 else None,
                ann_total=tot / h, ann_net=net / h)


# --------------------------------------------------------------------------- main build
def load_json(p):
    return json.loads(pathlib.Path(p).read_text())


def build(market_file, asof: dt.date):
    static = load_json(DATA / "bonds_static.json")["bonds"]
    mi = load_json(DATA / "market_inputs.json")
    ip = load_json(DATA / "index_portfolios.json")
    mk = load_json(market_file)
    settle = add_bdays(asof, 2)
    fund = mi["money_market"]["funding_rate"]
    irs = irs_curve(mi)

    fix = {f["ticker"]: f for f in mk["fixing"]}
    qts = {q["ticker"]: q for q in mk["quotes"]}
    bonds, rows = [], []
    for s in static:
        b = Bond(s["ticker"], s["isin"], s["coupon"], dt.date.fromisoformat(s["maturity"]))
        if b.maturity <= settle:
            continue
        src, clean, ba = None, None, None
        f = fix.get(b.ticker)
        if f and f.get("fix_price"):
            clean, src = f["fix_price"], "fixing"
            if f.get("bid") and f.get("ask"):
                ba = f["ask"] - f["bid"]
        elif b.ticker in qts and qts[b.ticker]["bid"] and qts[b.ticker]["ask"]:
            q = qts[b.ticker]
            clean, src, ba = (q["bid"] + q["ask"]) / 2, f"mid {mk['quotes_date']}", q["ask"] - q["bid"]
        if clean is None:
            continue
        y = b.yield_from_clean(clean, settle)
        r = b.risk(y, settle)
        bonds.append(b)
        rows.append(dict(ticker=b.ticker, isin=b.isin, coupon=b.coupon, maturity=b.maturity.isoformat(),
                         ttm=b.ttm(settle), clean=clean, accrued=b.accrued(settle), dirty=r["dirty"],
                         ytm=y * 100, mac=r["mac"], mod=r["mod"], conv=r["conv"],
                         dv01=r["dirty"] * r["mod"] / 100 * 100,  # PLN per 1bp per 1m PLN nominal
                         src=src, bid_ask=ba, bs_yield=(f or {}).get("fix_yld")))

    # ---- curve fit (exclude <0.75y bills-like paper and very wide quotes)
    # weights: fixings 1.0; sub-0.75y paper and non-fixing mids down-weighted; OK0127 (bill-like,
    # stale wide quote) excluded. WS0447 kept at low weight so the >10Y extrapolation is anchored.
    def fit_w(r):
        if r["ttm"] < 0.35:
            return 0.0
        w = 1.0 if r["src"] == "fixing" else 0.4
        if r["ttm"] < 0.75:
            w *= 0.5
        if (r["bid_ask"] or 0) > 0.6:
            w *= 0.6
        return w
    fit_idx = [i for i, r in enumerate(rows) if fit_w(r) > 0]
    weights = [fit_w(rows[i]) for i in fit_idx]
    front = mi["curve"]["front_anchor"]
    curve = fit_curve([bonds[i] for i in fit_idx], [rows[i]["clean"] for i in fit_idx], settle, weights,
                      anchors=[(front["tau"], front["rate"], front["weight"])])

    for b, r in zip(bonds, rows):
        fitted_dirty = curve.price(b, settle)
        r["fit_ytm"] = b.yield_from_clean(fitted_dirty - b.accrued(settle), settle) * 100
        r["in_fit"] = rows.index(r) in fit_idx
        r["rc_bp"] = (r["ytm"] - r["fit_ytm"]) * 100 if r["in_fit"] else None  # + = cheap (yields above curve)
        zs = zspread(b, curve, r["dirty"], settle)
        r["irs"] = irs(r["ttm"])
        r["asw_bp"] = (r["ytm"] - r["irs"]) * 100
        r["asw_extrap"] = r["ttm"] > 10.0 or r["ttm"] < 0.5
        r["h3"] = horizon_split(b, r["clean"], r["ytm"] / 100, curve, zs, settle, 3, fund)
        r["h12"] = horizon_split(b, r["clean"], r["ytm"] / 100, curve, zs, settle, 12, fund)
        r["running_carry_bp"] = (r["ytm"] - fund) * 100
        r["asw_carry_bp"] = r["asw_bp"] + (mi["money_market"]["wibor_6m"] - fund) * 100

    # ---- ASW by tenor bucket (yield-to-swap spread)
    buckets = [("1Y", 0.75, 1.5), ("2Y", 1.5, 2.5), ("3Y", 2.5, 3.5), ("4Y", 3.5, 4.5), ("5Y", 4.5, 5.5),
               ("6-7Y", 5.5, 7.5), ("8-9Y", 7.5, 9.75), ("10Y", 9.75, 11.0), ("20Y", 15, 25)]
    asw_b = []
    for name, lo, hi in buckets:
        mem = [r for r in rows if lo <= r["ttm"] < hi]
        if not mem:
            continue
        mid = (lo + hi) / 2
        asw_b.append(dict(bucket=name, n=len(mem), bonds=[m["ticker"] for m in mem],
                          avg_asw=sum(m["asw_bp"] for m in mem) / len(mem),
                          min_asw=min(m["asw_bp"] for m in mem), max_asw=max(m["asw_bp"] for m in mem),
                          avg_ytm=sum(m["ytm"] for m in mem) / len(mem), irs=irs(mid),
                          widest=max(mem, key=lambda m: m["asw_bp"])["ticker"]))

    # ---- curve grid for charts
    grid = []
    for T in np.round(np.arange(0.5, 21.01, 0.25), 2):
        grid.append(dict(t=float(T), fit=curve.par_yield(float(T)), irs=irs(float(T))))

    # ---- indices
    by = {r["ticker"]: r for r in rows}
    indices = {}
    for code, ix in ip["indices"].items():
        mv = {t: u * 1000 / 100 * by[t]["dirty"] for t, u in ix["units"].items()}
        tot = sum(mv.values())
        w = {t: v / tot for t, v in mv.items()}
        agg = lambda k: sum(w[t] * by[t][k] for t in w)
        cons = []
        for t in sorted(w, key=lambda t: by[t]["ttm"]):
            cons.append(dict(ticker=t, weight=w[t] * 100, ytm=by[t]["ytm"], mod=by[t]["mod"], ttm=by[t]["ttm"],
                             dur_contrib=w[t] * by[t]["mod"], rc_bp=by[t]["rc_bp"], asw_bp=by[t]["asw_bp"]))
        hz = {}
        for h in ("h3", "h12"):
            keys = ["coupon", "pull", "roll", "total", "funding", "net"]
            hz[h] = {k: sum(w[t] * by[t][h][k] for t in w) for k in keys}
            hz[h]["breakeven_bp"] = hz[h]["net"] / agg("mod") * 100
        scen = {}
        for name, fn in SCENARIOS.items():
            pnl = 0.0
            for t in w:
                b = next(bb for bb in bonds if bb.ticker == t)
                dy = fn(by[t]["ttm"]) / 1e4
                p1 = b.dirty_from_yield(by[t]["ytm"] / 100 + dy, settle)
                pnl += w[t] * (p1 / by[t]["dirty"] - 1) * 100
            scen[name] = dict(instant=pnl, twelve_m=pnl + hz["h12"]["total"])
        # portfolio yield as IRR of the aggregated cash flows (better than MV-weighted YTM on a steep curve)
        cfs = []
        for t, u in ix["units"].items():
            b = next(bb for bb in bonds if bb.ticker == t)
            cfs += [(tt, a * u * 10) for tt, _, a in b.flows(settle)]
        irr = brentq(lambda y: sum(a / (1 + y) ** tt for tt, a in cfs) - tot, -0.5, 1.0)
        irr_mac = sum(tt * a / (1 + irr) ** tt for tt, a in cfs) / tot
        indices[code] = dict(label=ix["label"], rule=ix["rule"], official=ix["official"], n=len(w),
                             irr=irr * 100, irr_mod=irr_mac / (1 + irr),
                             mv_bn=tot / 1e9, ytm=agg("ytm"), mod=agg("mod"), mac=agg("mac"), conv=agg("conv"),
                             ttm=agg("ttm"), coupon=agg("coupon"), asw_bp=agg("asw_bp"),
                             dv01_per_mn=agg("mod") * 100, horizons=hz, scenarios=scen, constituents=cons)

    return dict(asof=asof.isoformat(), settle=settle.isoformat(), funding=fund, bonds=rows, curve=grid,
                curve_params=list(map(float, curve.params)), asw_buckets=asw_b, indices=indices,
                market_inputs=mi, portfolio_meta={k: ip[k] for k in ip if k != "indices"},
                tbsp_level=mk.get("tbsp_index"), repo=mk.get("repo"), tbills=mk.get("tbills"),
                fixing_url=mk.get("fixing_url"), quotes_date=mk.get("quotes_date"))


SCENARIOS = {
    "Parallel +50bp": lambda T: 50.0,
    "Parallel -50bp": lambda T: -50.0,
    "Bear flattener (MPC hikes: +60bp 1Y -> +15bp 10Y)": lambda T: max(15.0, 60.0 - 5.0 * max(T - 1, 0)),
    "Bull flattener (fiscal relief: -10bp 1Y -> -60bp 10Y)": lambda T: -min(60.0, 10.0 + 5.6 * max(T - 1, 0)),
    "Bull steepener (cuts priced: -60bp 1Y -> -20bp 10Y)": lambda T: -max(20.0, 60.0 - 4.5 * max(T - 1, 0)),
}


if __name__ == "__main__":
    import sys
    d = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 9)
    out = build(DATA / "market" / f"bondspot_{d:%Y%m%d}.json", d)
    p = DATA / "analytics" / f"analytics_{d:%Y%m%d}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, default=str))
    print("wrote", p)
    print(f"{'tk':7}{'ttm':>6}{'cpn':>6}{'clean':>8}{'ytm':>7}{'fit':>7}{'r/c':>6}{'MD':>6}{'IRS':>6}{'ASW':>6}"
          f"{'cp3':>6}{'pl3':>6}{'rl3':>6}{'net3':>6}{'tot12':>7}{'rl12':>6}{'net12':>7}{'BE12':>6}")
    for r in out["bonds"]:
        h3, h12 = r["h3"] or {}, r["h12"] or {}
        g = lambda h, k: f"{h[k]:6.2f}" if h else "     -"
        print(f"{r['ticker']:7}{r['ttm']:6.2f}{r['coupon']:6.2f}{r['clean']:8.2f}{r['ytm']:7.3f}{r['fit_ytm']:7.3f}"
              f"{(r['rc_bp'] if r['rc_bp'] is not None else float('nan')):6.1f}{r['mod']:6.2f}{r['irs']:6.2f}{r['asw_bp']:6.0f}{g(h3,'coupon')}{g(h3,'pull')}"
              f"{g(h3,'roll')}{g(h3,'net')}{(h12.get('total') or 0):7.2f}{(h12.get('roll') or 0):6.2f}"
              f"{(h12.get('net') or 0):7.2f}{(h12.get('breakeven_bp') or 0):6.0f}")
    for k, v in out["indices"].items():
        o = v["official"]
        print(f"{k:12} n={v['n']} MV={v['mv_bn']:.1f}bn YTM={v['ytm']:.2f} (off {o['ytm']}) MD={v['mod']:.3f} "
              f"(off {o['mod_dur']}) Mac={v['mac']:.2f} (off {o['mac_dur']}) TTM={v['ttm']:.2f} ASW={v['asw_bp']:.0f}")
        print("   h3", {k2: round(x, 2) for k2, x in v["horizons"]["h3"].items()})
        print("   h12", {k2: round(x, 2) for k2, x in v["horizons"]["h12"].items()})
        print("   scen", {k2: (round(x['instant'], 2), round(x['twelve_m'], 2)) for k2, x in v["scenarios"].items()})
    print("ASW buckets", [(b["bucket"], round(b["avg_asw"]), b["widest"]) for b in out["asw_buckets"]])
    print("curve params", out["curve_params"])
