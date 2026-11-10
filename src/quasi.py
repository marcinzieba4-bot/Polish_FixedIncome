"""Polish quasi-sovereigns (BGK FPC/FWSZ, PFR): yields, spread vs the fitted POLGB curve, ASW.

Prices are thin Catalyst prints (retail lots) - indicative only. Spread vs POLGB = bond yield minus the yield the
fitted POLGB zero curve gives for the same cash flows (same method as the rich/cheap residuals).
Usage: python src/quasi.py 2026-11-09  ->  data/quasi.json
"""
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from analytics import DATA, Bond, Curve, add_bdays, irs_curve  # noqa: E402

# ticker, isin, coupon (None = floater), maturity, outstanding PLN bn, Catalyst clean price, price note, 29-Oct auction yield
QUASI = [
    ("FPC0229", "PL0000500443", 5.75, "2029-02-03", 8.75, 101.05, "Catalyst 6 Nov", 5.331),
    ("FPC0630", "PL0000500278", 2.125, "2030-06-05", 34.22, 89.20, "Catalyst 9 Nov", None),
    ("FPC0231", "PL0000500450", 5.75, "2031-02-03", 10.10, 100.20, "Catalyst 9 Nov", 5.946),
    ("FPC0733", "PL0000500294", 2.25, "2033-07-21", 12.17, 79.90, "Catalyst 9 Nov", None),
    ("FPC0235", "PL0000500468", 6.00, "2035-02-03", 17.69, 98.34, "Catalyst 9 Nov", 6.580),
    ("FPC1140", "PL0000500302", 2.375, "2040-11-27", 6.55, 65.00, "Catalyst 9 Nov", None),
    ("FPC0342", "PL0000500385", 6.75, "2042-03-02", 4.25, 105.40, "Catalyst reference price, no trade", None),
]
FLOATERS = [
    ("FPC0631", "6M WIBOR-linked, current 4.44%", "2031-06-12", 29.43, 98.05),
    ("FPC0931", "floating, current ~3.55% (index unverified)", "2031-09-25", 6.24, 93.24),
    ("FPC0332", "floating, current 3.85%", "2032-03-03", 18.34, 95.40),
    ("FWA0931", "avg 3 x 6M WIBOR (FWSZ), current 3.86%", "2031-09-15", 3.00, 95.10),
]
PFR = [("PFR0627", 1.75, "2027-06-07", 10.0), ("PFR0827", 1.375, "2027-08-30", 5.25), ("PFR0927", 1.50, "2027-09-30", 2.0), ("PFR0330", 2.00, "2030-03-05", 3.25)]


def main(asof, snap=None):
    global QUASI, FLOATERS, PFR
    QI = None
    if snap:
        snap = pathlib.Path(snap)
        QI = json.loads((snap / "quasi_inputs.json").read_text())
        QUASI = [tuple(x) for x in QI["fixed"]]
        FLOATERS = [tuple(x) for x in QI.get("floaters", [])]
        PFR = [tuple(x) for x in QI.get("pfr", [])]
        A = json.loads((snap / "analytics.json").read_text())
    else:
        A = json.loads((DATA / "analytics" / f"analytics_{asof:%Y%m%d}.json").read_text())
    settle = add_bdays(asof, 2)
    curve = Curve(A["curve_params"])
    irs = irs_curve(A["market_inputs"])
    rows = []
    for tk, isin, cpn, mat, out, px, note, auc in QUASI:
        b = Bond(tk, isin, cpn, dt.date.fromisoformat(mat))
        y = b.yield_from_clean(px, settle) * 100
        fit_dirty = curve.price(b, settle)
        pol = b.yield_from_clean(fit_dirty - b.accrued(settle), settle) * 100
        T = b.ttm(settle)
        long_end = T > 11
        rows.append(dict(ticker=tk, issuer="BGK · FPC", coupon_desc=f"{cpn:g}% fixed",
                         maturity=mat, ttm=T, outstanding_bn=out, price=px, yield_=y, polgb_same=pol, spread_polgb_bp=(y - pol) * 100,
                         asw_bp=(y - irs(T)) * 100, mod=b.risk(y / 100, settle)["mod"], auction_yield=auc,
                         note=note + ("; POLGB curve extrapolated past 10Y - spread indicative" if long_end else "")))
    for r in rows:
        r["yield"] = r.pop("yield_")
    fl = [dict(ticker=t, issuer=("BGK · FWSZ" if t.startswith("FWA") else "BGK · FPC"), coupon_desc=d, maturity=m, outstanding_bn=o, price=p, yield_=None, polgb_same=None, spread_polgb_bp=None,
               asw_bp=None, note=f"floater, price {p:.2f}; margin not in our sources") for t, d, m, o, p in FLOATERS]
    for r in fl:
        r["yield"] = r.pop("yield_")
    pfr = [dict(ticker=t, issuer="PFR", coupon_desc=f"{c}% fixed", maturity=m, outstanding_bn=o, price=None, yield_=None,
                polgb_same=None, spread_polgb_bp=None, asw_bp=None, note="no current trades (last prints 2025 / Jan 2026)") for t, c, m, o in PFR]
    for r in pfr:
        r["yield"] = r.pop("yield_")
    fixed = [r for r in rows if r["ttm"] <= 11]
    avg_sp = sum(r["spread_polgb_bp"] for r in fixed) / len(fixed)
    best = max(fixed, key=lambda r: r["spread_polgb_bp"])
    widest_asw = max(fixed, key=lambda r: r["asw_bp"])
    Q = dict(
        asof=asof.isoformat(),
        lede=("Issuers: BGK = Bank Gospodarstwa Krajowego, FPC = COVID-19 Fund series, FWSZ = Armed Forces Support Fund series, PFR = Polish Development Fund. BGK bonds for the COVID-19 Fund (FPC) and the Armed Forces Support Fund (FWSZ) carry an explicit State Treasury guarantee, the same credit as POLGBs, "
              "and PFR shield bonds are also guaranteed. Prices are thin Catalyst retail prints, so treat levels as indicative. Spread vs POLGB = yield minus the fitted POLGB curve "
              "for the same cash flows; ASW = yield minus PLN IRS. BGK's own 29 Oct auction yields are shown for reference."),
        bonds=rows + fl + pfr,
        avg_spread_bp=avg_sp,
        takeaways_html=[
            f"<b>FPC fixed lines trade ~{min(r['spread_polgb_bp'] for r in fixed):.0f}-{max(r['spread_polgb_bp'] for r in fixed):.0f}bp over the POLGB curve</b> (average {avg_sp:.0f}bp). That is in line with PKO BP's auction-spread read of ~21-32bp in spring 2026 "
            f"and the ~+29/+38bp at BGK's 29 Oct auction (FPC0229/FPC0235), and well below the 40-60bp peaks of 2023. <b>The quasi premium has been stable while POLGB ASW widened</b>, "
            f"so in swap terms FPC are the widest guaranteed PLN paper: ASW up to {widest_asw['asw_bp']:.0f}bp ({widest_asw['ticker']}).",
            f"<b>Best value: {best['ticker']}</b> ({best['spread_polgb_bp']:+.0f}bp vs POLGB, {best['yield']:.2f}%). For buy-and-hold books, the same guarantee for ~25bp more (up to {best['spread_polgb_bp']:.0f}bp here) is worth more than the liquidity cost. "
            "Buy at BGK auctions (next dates reportedly 13 Nov, 26 Nov, 10 Dec, unverified), not on Catalyst.",
            "<b>Low-coupon FPC0630 / FPC0733</b> (2.125% / 2.25%) trade at deep discounts (89 / 80). Like the low-coupon DS lines they suit pull-to-par and accounting-driven buyers, "
            f"and FPC0733 is the expensive one: only {[r for r in rows if r['ticker'] == 'FPC0733'][0]['spread_polgb_bp']:+.0f}bp over POLGB.",
            "<b>Supply is the swing factor for 2027:</b> about PLN 52bn of FPC and PFR maturities in 2027 are to be refinanced via FPC issuance (MoF debt strategy; FPC plan PLN 18.5bn for 2026). "
            "That argues for spreads drifting wider (PKO expected ~30bp). FWSZ is funded mainly by SAFE and other loans (only ~PLN 1bn of FWSZ bonds Jan-Sep 2026), so FWSZ bond supply is not the risk.",
            "<b>Floaters (FPC0631/FPC0332/FPC0931, FWA0931)</b> trade at 93-98. Their margins aren't in our sources, so no DM is shown. Against the 3-4Y WZ at +67-80bp over WIBOR, a quasi floater needs roughly WZ + 25-35bp to be worth the illiquidity.",
        ],
        sources=("Sources: Catalyst instrument pages and quotes (gpwcatalyst.pl, 6-9 Nov 2026); BGK auction result 29.10.2026 (PDF mirrored on strefainwestorow.pl); PKO BP special reports 23.10.2025, "
                 "15.05.2026 and 05.11.2026; ISBnews 30.07.2026; MoF debt strategy 2027-2030; MoF public-debt bulletin Q1 2026; FWSZ status after Q3 2026 (dziennikzbrojny.pl). "
                 "Yields recomputed here with annual ACT/ACT coupons on each bond's anniversary dates (this method reproduces BGK's 29 Oct auction yields)."),
    )
    if QI:  # snapshot: point-in-time texts supplied with the inputs; {avg}, {best}, {best_sp}, {widest}, {widest_asw}, {lo}, {hi} filled from data
        fm = dict(avg=f"{avg_sp:.0f}", best=best["ticker"], best_sp=f"{best['spread_polgb_bp']:+.0f}", widest=widest_asw["ticker"],
                  widest_asw=f"{widest_asw['asw_bp']:.0f}", lo=f"{min(r['spread_polgb_bp'] for r in fixed):.0f}", hi=f"{max(r['spread_polgb_bp'] for r in fixed):.0f}")
        Q["lede"] = QI.get("lede", Q["lede"])
        Q["takeaways_html"] = [t.format(**fm) for t in QI.get("takeaways_html", [])]
        Q["sources"] = QI.get("sources", "")
    ((snap / "quasi.json") if snap else (DATA / "quasi.json")).write_text(json.dumps(Q, indent=1, ensure_ascii=False))
    for r in rows:
        print(f"{r['ticker']} T={r['ttm']:.2f} px={r['price']} y={r['yield']:.3f} polgb={r['polgb_same']:.3f} sp={r['spread_polgb_bp']:+.0f} asw={r['asw_bp']:+.0f}")
    print("avg spread", round(avg_sp, 1))


if __name__ == "__main__":
    main(dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 9),
         sys.argv[sys.argv.index("--snap") + 1] if "--snap" in sys.argv else None)
