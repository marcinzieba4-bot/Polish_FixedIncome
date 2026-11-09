"""Render the Polish FI dashboard (standalone HTML) from analytics + calendar + inputs.

Usage: python src/build_dashboard.py 2026-11-09   -> dist/dashboard/index.html
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from analytics import Bond, DATA, ROOT, add_bdays, irs_curve  # noqa: E402
from core_section import core_section  # noqa: E402

E = html.escape


def f(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def sg(x, d=2):
    if x is None:
        return "–"
    return ("+" if x > 0 else "−" if x < 0 else "") + f"{abs(x):.{d}f}"


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def main(asof: dt.date):
    A = load(DATA / "analytics" / f"analytics_{asof:%Y%m%d}.json")
    cal = load(DATA / "calendar.json")
    cyc = load(DATA / "analytics" / "auction_cycle.json")
    hist = load(DATA / "market" / "fixing_history.json")
    core_p = DATA / "analytics" / f"core_{asof:%Y%m%d}.json"
    K = load(core_p) if core_p.exists() else None
    mi = A["market_inputs"]
    mm, pol, mac = mi["money_market"], mi["policy"], mi["macro"]
    B = {b["ticker"]: b for b in A["bonds"]}
    IX = A["indices"]
    irs = irs_curve(mi)
    fund = A["funding"]

    # ------------------------------------------------------------------ derived numbers
    irs1, irs2 = irs(1.0), irs(2.0)
    fwd_1y1y = 2 * irs2 - irs1
    implied_6m_up = fwd_1y1y - mm["wibor_6m"]
    s2s10 = (B["DS0436"]["ytm"] - B["OK0129"]["ytm"]) * 100
    s2s5 = (B["PS1031"]["ytm"] - B["OK0129"]["ytm"]) * 100
    s5s10 = (B["DS0436"]["ytm"] - B["PS1031"]["ytm"]) * 100
    front_jump = (B["OK0129"]["ytm"] - B["OK0128"]["ytm"]) * 100
    rv_pick = (B["PS0130"]["ytm"] - B["DS1029"]["ytm"]) * 100
    rv_rc = (B["PS0130"]["rc_bp"] or 0) - (B["DS1029"]["rc_bp"] or 0)

    def proj(code, out, add_t, add_units):
        """Index MD after end-Jan rebalance at today's prices (step change)."""
        ix = load(DATA / "index_portfolios.json")["indices"][code]
        units = {k: v for k, v in ix["units"].items() if k != out}
        units[add_t] = add_units
        mv = {t: u * 10 * B[t]["dirty"] for t, u in units.items()}
        tot = sum(mv.values())
        return sum(mv[t] / tot * B[t]["mod"] for t in mv), sum(mv[t] / tot * B[t]["ytm"] for t in mv)

    p13 = proj("GPWB-B1Y3Y", "OK0128", "PS0130", 55439705)
    p14 = proj("GPWB-B1Y4Y", "OK0128", "PS0131", 56695631)

    ex_md = lambda t: B[t]["h12"]["net"] / B[t]["mod"] * 100  # bp of 12M excess per unit MD
    if K:
        kh = {(h["asset"], h["T"]): h for h in K["hedged"]}
        kc = {(c["mkt"], c["T"]): c for c in K["carry_roll"]}
        k_last = K["spread_hist"][-1]
        k_de1 = kh[("DE", 1)]["PLN"]
        k_sub1 = max(B["PS0527"]["ytm"], B["DS0727"]["ytm"])
    best_front = max(["OK0129", "WS0429", "PS0729", "DS1029", "PS0130"], key=ex_md)

    # ------------------------------------------------------------------ data passed to JS
    labels = ["OK0128", "OK0129", "DS1029", "PS1031", "DS1033", "DS0436", "WS0447", "PS0527"]
    hist_series = {}
    for t in ["OK0129", "PS0731", "DS0436"]:
        hist_series[t] = [[d, v[t][1]] for d, v in sorted(hist.items()) if t in v and v[t][1] is not None]
    auc_dates = cyc["_meta"]["auctions"]
    js = dict(bonds=A["bonds"], curve=A["curve"], asw_buckets=A["asw_buckets"], indices=IX,
              market_inputs={"asw_lseg_2026_11_06": mi["asw_lseg_2026_11_06"]}, label_bonds=labels,
              highlight=["OK0129", "PS0729", "PS0130", "PS1031", "DS1035", "DS0436"],
              hist=hist_series, auctions=auc_dates, cycle={k: v for k, v in cyc.items() if not k.startswith("_")},
              core=({k: K[k] for k in ("grid", "carry_roll", "spread_hist")} if K else None))

    # ------------------------------------------------------------------ HTML pieces
    o = []
    w = o.append
    settle = A["settle"]
    w(f"""
<header class="top">
  <div>
    <h1>Polish fixed income desk</h1>
    <p class="sub">POLGB curve, index duration (GPWB 1-3Y, GPWB 1-4Y, TBSP.Index), asset swaps, rich/cheap, carry &amp; roll, Poland vs core markets (incl. FX-hedged), auction timing and trade ideas.</p>
    <div class="meta">Prices: Treasury BondSpot Poland fixing {E(A['asof'])} · settlement {E(settle)} · private page, not indexed</div>
  </div>
  <button class="theme-btn" id="themeBtn" type="button">Dark mode</button>
</header>
<nav class="toc" aria-label="Sections">
  <a href="#bottom">Bottom line</a><a href="#indices">Index duration</a><a href="#curve">Curve &amp; ASW</a>
  <a href="#rv">Single bonds</a><a href="#roll">Carry &amp; roll</a><a href="#core">PL vs core</a><a href="#auctions">Auctions &amp; timing</a>
  <a href="#ideas">What to play</a><a href="#bonds">All bonds</a><a href="#method">Method</a>
</nav>
""")
    tiles = [
        ("NBP reference", f"{f(pol['nbp_reference'])}%", "MPC next: 1-2 Dec"),
        ("WIBOR 3M / 6M", f"{f(mm['wibor_3m'])} / {f(mm['wibor_6m'])}", f"POLSTR O/N {f(mm['polstr_on'], 3)}"),
        ("Repo (funding)", f"{f(fund)}%", "special 1W 3.65-3.67"),
        ("POLGB 2Y (OK0129)", f"{f(B['OK0129']['ytm'])}%", f"ASW {sg(B['OK0129']['asw_bp'], 0)}bp"),
        ("POLGB 5Y (PS1031)", f"{f(B['PS1031']['ytm'])}%", f"ASW {sg(B['PS1031']['asw_bp'], 0)}bp"),
        ("POLGB 10Y (DS0436)", f"{f(B['DS0436']['ytm'])}%", f"ASW {sg(B['DS0436']['asw_bp'], 0)}bp"),
        ("IRS 2Y / 5Y / 10Y", f"{f(mi['irs']['pillars']['2'])} / {f(mi['irs']['pillars']['5'])} / {f(mi['irs']['pillars']['10'])}", "LSEG close 6 Nov"),
        ("2s10s / 5s10s", f"{f(s2s10, 0)} / {f(s5s10, 0)}bp", f"2s5s {f(s2s5, 0)}bp"),
        ("CPI Oct (flash)", f"{f(mac['cpi_oct_flash'], 1)}%", "NBP proj. 2027: 4.2%"),
        ("TBSP.Index", f"{A['tbsp_level']:,.2f}", f"BondSpot {E(A['asof'])}"),
    ]
    w('<div class="tiles">' + "".join(
        f'<div class="tile"><div class="l">{E(a)}</div><div class="v">{E(b)}</div><div class="d">{E(c)}</div></div>'
        for a, b, c in tiles) + "</div>")

    t13, t14, tb = IX["GPWB-B1Y3Y"], IX["GPWB-B1Y4Y"], IX["TBSP.Index"]
    w(f"""
<div class="bottomline" id="bottom">
  <h2>Bottom line — {E(A['asof'])}</h2>
  <ol>
    <li><b>Modified duration today:</b> GPWB 1-3Y <b>{f(t13['mod'])}</b>, GPWB 1-4Y <b>{f(t14['mod'])}</b>, TBSP.Index <b>{f(tb['mod'])}</b>
      (GPW Benchmark official at 28 Oct: {f(t13['official']['mod_dur'])} / {f(t14['official']['mod_dur'])} / {f(tb['official']['mod_dur'])}).
      Cash-flow yields {f(t13['irr'])}% / {f(t14['irr'])}% / {f(tb['irr'])}%. Expect a step-up at the end-January rebalance
      (OK0128 drops out; PS0130 joins 1-3Y, PS0131 joins 1-4Y): roughly {f(t13['mod'])} → {f(p13[0])} and {f(t14['mod'])} → {f(p14[0])}.</li>
    <li><b>Best risk-adjusted carry is the 2-3Y sector.</b> The curve jumps {f(front_jump, 0)}bp from OK0128 (1.2Y) to OK0129 (2.2Y),
      so 2-3Y paper earns ~{f(B['OK0129']['h12']['roll_bp'], 0)}bp of roll-down a year on top of its yield: {E(best_front)} returns {f(B[best_front]['h12']['total'])}% over 12M
      on an unchanged curve, {sg(B[best_front]['h12']['net'])}% over repo, with a {f(B[best_front]['h12']['breakeven_bp'], 0)}bp breakeven.
      That steepness prices hikes: 1y1y IRS ≈ {f(fwd_1y1y)}% vs 6M WIBOR {f(mm['wibor_6m'])}%. Owning it is a bet that the MPC does at most a 25bp "insurance" hike.</li>
    <li><b>Asset swaps are at extreme wides:</b> about {f(A['asw_buckets'][4]['avg_asw'], 0)}bp at 5Y and {f(A['asw_buckets'][6]['avg_asw'], 0)}bp at 8-9Y
      (LSEG generic 10Y: {mi['asw_lseg_2026_11_06']['10Y']}bp). This is a fiscal premium: 2026 deficit ~{f(mac['deficit_2026_gdp'], 1)}% of GDP, and S&amp;P moved to a negative outlook on 6 Nov.
      An asset-swapped DS1035/DS0436 earns ~{f(B['DS0436']['asw_carry_bp'], 0)}bp a year in running carry. Size it modestly and add at supply.</li>
    <li><b>Relative value:</b> sell rich DS1029 and buy PS0130, picking up {f(rv_pick, 0)}bp at the same duration ({f(B['DS1029']['mod'])} vs {f(B['PS0130']['mod'])}),
      with PS0130 joining the 1-3Y index in January. The on-the-run supply lines (PS1031, DS0436, OK0129) screen 4bp cheap.
      Avoid sub-1Y paper: it yields below repo.</li>
    <li><b>When to buy:</b> across the last 9 auctions the curve cheapened ~{f(cyc['T-2']['mean'], 1)}bp two days before (the final-offer day)
      and {sg(cyc['T+0']['mean'], 1)}bp on auction day, then rallied {sg(cyc['T+1']['mean'], 1)}bp the day after. So buy at the close of
      <b>18 Nov and 25 Nov</b>, not in the run-up. Scale into the front end around the <b>2 Dec MPC</b>. Hold through the December supply pause
      and the <b>25 Jan</b> OK0127 redemption and coupon reinvestment.</li>""" + (f"""
    <li><b>Versus core:</b> Poland is the steep, high-carry curve in a world of flattening core curves. 10Y carry+roll is {f(kc[('PL', 10)]['total_bp'], 0)}bp/yr vs {f(kc[('DE', 10)]['total_bp'], 0)} (Bund) and {f(kc[('US', 10)]['total_bp'], 0)} (UST).
      PL−Bund 10Y is ~{f((k_last['pl10'] - k_last['de10']) * 100, 0)}bp. Hedged into PLN at market forward points (EUR→PLN hedge pays ~{f(K['pick']['eurpln_1y_market'])}%/yr), Bunds lose to POLGBs from 2Y out
      ({f((kh[('PL', 2)]['PLN'] - kh[('DE', 2)]['PLN']) * 100, 0)}bp at 2Y, ~120bp at 5-10Y matched-maturity), so "buy Bund and swap into PLN" doesn't pay for duration.
      It does pay at the front end: a 1Y Bund hedged into PLN ≈ {f(k_de1)}% vs {f(kh[('PL', 1)]['local'])}% for the 1Y POLGB and {f(k_sub1)}% for sub-1Y POLGBs.
      A EUR investor gets ~{f(K['eurobonds'][-1]['hedged_minus_eurobond'], 0) if K.get('eurobonds') else '–'}bp more from a hedged POLGB than from Poland's own EUR 2036 bond.</li>""" if K else "") + f"""
  </ol>
  <div class="sub">Funding {f(fund)}% · IRS pillars from LSEG via Bank Millennium (6 Nov close), other tenors interpolated · horizon returns assume an unchanged curve and constant rich/cheap.</div>
</div>
""")

    # ------------------------------------------------------------------ indices
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
    <span>Mod. duration — official 28 Oct</span><b>{f(of['mod_dur'])}</b>
    <span>Yield (IRR of cash flows)</span><b>{f(ix['irr'])}%</b>
    <span>Yield (MV-weighted avg)</span><b>{f(ix['ytm'])}% <span class="off">off. 28 Oct {f(of['ytm'])}%</span></b>
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
    scen_rows = "".join(
        f"<tr><td class='l'>{E(s)}</td>" + "".join(
            f"<td>{sg(IX[c]['scenarios'][s]['instant'])}%</td><td>{f(IX[c]['scenarios'][s]['twelve_m'])}%</td>" for c in IX) + "</tr>"
        for s in scen_names)
    w(f"""
<section class="card" id="indices">
  <h2>Index modified duration <span class="tag">GPWB 1-3Y · GPWB 1-4Y · TBSP</span></h2>
  <p class="lede">Computed bond by bond from the official GPW Benchmark portfolios effective 30 Oct 2026 (bond counts from the
  <a href="{E(A['portfolio_meta']['source_url'])}" rel="noopener">28 Oct communiqué</a>). Each portfolio is re-weighted at today's dirty prices.
  Durations are annual-compounding Macaulay/(1+y), the same basis GPW Benchmark publishes. The small gap to the official numbers is
  12 days of time decay plus the ~20-25bp rally since 28 Oct. Next periodic change: {E(A['portfolio_meta']['next_rebalance'])}; the month-end taps of OK0129, PS1031 and DS0436 raise their weights.</p>
  <div class="grid3">{ixcard('GPWB-B1Y3Y')}{ixcard('GPWB-B1Y4Y')}{ixcard('TBSP.Index')}</div>
  <div class="note"><b>What a rebalance does to duration.</b> At the end-January 2027 change, OK0128 falls below one year and leaves both short indices.
  PS0130 enters 1-3Y (MD {f(B['PS0130']['mod'])}) and PS0131 enters 1-4Y (MD {f(B['PS0131']['mod'])}). Holding today's prices, 1-3Y duration goes from {f(t13['mod'])} to ~{f(p13[0])}
  and 1-4Y from {f(t14['mod'])} to ~{f(p14[0])}. Trackers have to buy PS0130/PS0131 into 29 Jan.
  DS0727 is likely to leave TBSP.Index at end-December (~0.57Y to maturity).</div>
  <h3>Contribution to duration, by constituent</h3>
  <div class="tabs" id="ixTabs" role="group" aria-label="Choose index"></div>
  <div class="legend"><span><i style="background:var(--s1)"></i>Weight × modified duration</span></div>
  <div id="ixDetail"></div>
  <h3>Scenario P&amp;L (full repricing)</h3>
  <p class="lede">"Now" is the instantaneous price change; "12M" is the 12-month total return including carry and roll. Yield shifts depend on tenor. All figures in %.</p>
  <div class="tablewrap"><table class="t">
    <thead><tr><th class="l">Scenario</th>{''.join(f"<th>{E(IX[c]['label'].replace('GPWB ', ''))} now</th><th>{E(IX[c]['label'].replace('GPWB ', ''))} 12M</th>" for c in IX)}</tr></thead>
    <tbody>{scen_rows}</tbody></table></div>
</section>
""")

    # ------------------------------------------------------------------ curve & ASW
    asw_rows = "".join(
        f"<tr><td class='l'>{E(b['bucket'])}</td><td class='l'>{E(', '.join(b['bonds']))}</td><td>{f(b['avg_ytm'])}</td>"
        f"<td>{f(b['irs'])}</td><td>{sg(b['avg_asw'], 0)}</td><td>{sg(b['min_asw'], 0)} … {sg(b['max_asw'], 0)}</td><td class='l'>{E(b['widest'])}</td></tr>"
        for b in A["asw_buckets"])
    w(f"""
<section class="card" id="curve">
  <h2>Curve &amp; asset swaps <span class="tag">yield − IRS</span></h2>
  <p class="lede">Dots are the BondSpot fixing yields. The blue line is a Nelson-Siegel-Svensson fit and the orange line is the PLN IRS curve (vs 6M WIBOR).
  The grey verticals show the asset-swap gap for each bond. Swap spreads are near zero inside 2Y, ~{f(A['asw_buckets'][3]['avg_asw'], 0)}bp at 4Y and around
  {f(A['asw_buckets'][6]['avg_asw'], 0)}bp at 8-10Y. The bond curve is far steeper than the swap curve: 2s10s POLGB {f(s2s10, 0)}bp vs IRS {f((mi['irs']['pillars']['10'] - mi['irs']['pillars']['2']) * 100, 0)}bp.
  So the term premium sits in the bonds (fiscal supply), not in rate expectations.</p>
  <div class="legend"><span><i class="dot" style="background:var(--s1)"></i>Bond yield (fixing)</span><span><i class="line" style="background:var(--s1);opacity:.55"></i>Fitted NSS curve</span><span><i class="line" style="background:var(--s2)"></i>PLN IRS</span></div>
  <div class="chart" id="curveChart"></div>
  <h3>ASW by tenor bucket</h3>
  <div class="legend"><span><i style="background:var(--s1)"></i>Average yield − interpolated IRS (bp)</span><span><i class="tick" style="background:var(--ink-2)"></i>LSEG generic ASW, 6 Nov (Bank Millennium)</span></div>
  <div class="chart" id="aswChart"></div>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bucket</th><th class="l">Bonds</th><th>Avg yield %</th><th>IRS %</th><th>Avg ASW bp</th><th>Range bp</th><th class="l">Widest</th></tr></thead><tbody>{asw_rows}</tbody></table></div>
  <div class="note"><b>Reading the ASW.</b> ASW here is the yield-to-swap spread: bond YTM minus the PLN IRS at the same maturity, both annual.
  Positive means the bond pays more than swaps, i.e. cheap sovereign risk. An asset-swap long (buy bond, pay IRS, receive 6M WIBOR, fund at repo) runs at
  ≈ ASW + (6M WIBOR − repo) = ASW + {f((mm['wibor_6m'] - fund) * 100, 0)}bp a year. Its main risk is ASW widening on fiscal or rating news, not the level of rates.
  Past 10Y the IRS is extrapolated, so the 20Y figure (WS0447) is indicative only. The WIBOR→POLSTR switch (no new WIBOR contracts after 31 Dec 2026) will move liquidity
  to POLSTR OIS in 2027. Expect an OIS-vs-WIBOR basis to appear in these spreads.</div>
</section>
""")

    # ------------------------------------------------------------------ rich/cheap
    rc = [b for b in A["bonds"] if b["rc_bp"] is not None]
    cheap = sorted(rc, key=lambda b: -b["rc_bp"])[:5]
    rich = sorted(rc, key=lambda b: b["rc_bp"])[:5]
    sector_best = []
    for name, lo, hi in [("1-2Y", 1.0, 2.0), ("2-3Y", 2.0, 3.0), ("3-4Y", 3.0, 4.0), ("4-6Y", 4.0, 6.0), ("6-8Y", 6.0, 8.0), ("8-11Y", 8.0, 11.0)]:
        mem = [b for b in A["bonds"] if lo <= b["ttm"] < hi]
        if mem:
            top = max(mem, key=lambda b: b["ytm"])
            sector_best.append((name, top, max(mem, key=lambda b: b["rc_bp"] or -99)))
    li = lambda b: f"<li><b>{E(b['ticker'])}</b> ({f(b['coupon'])}% {E(b['maturity'][:7])}): {sg(b['rc_bp'], 1)}bp vs curve, yield {f(b['ytm'], 3)}%, ASW {sg(b['asw_bp'], 0)}bp</li>"
    sec_rows = "".join(f"<tr><td class='l'>{E(n)}</td><td class='l'>{E(t['ticker'])}</td><td>{f(t['ytm'], 3)}</td><td class='l'>{E(c['ticker'])}</td><td>{sg(c['rc_bp'], 1)}</td></tr>" for n, t, c in sector_best)
    w(f"""
<section class="card" id="rv">
  <h2>Single papers that stand out <span class="tag">rich / cheap vs fitted curve</span></h2>
  <p class="lede">Residual = bond yield − yield implied by the fitted zero curve for the same cash flows. Using the zero curve strips out coupon effects that a plain
  yield-vs-maturity line would miss. Positive means cheap (pays more than the curve). Residuals inside ±2bp are noise.</p>
  <div class="legend"><span><i style="background:var(--pos)"></i>Cheap (yield above curve)</span><span><i style="background:var(--neg)"></i>Rich (yield below curve)</span></div>
  <div class="chart" id="rcChart"></div>
  <div class="grid2" style="margin-top:12px">
    <div><h3>Cheapest</h3><ul class="tight">{''.join(li(b) for b in cheap)}</ul>
      <p class="small">The cheap names are mostly the lines MoF is tapping now (OK0129, PS1031, DS0436), which carry a supply concession, plus high-coupon WS0429.
      The October auctions printed PS1031 at 5.91-6.04% and DS0436 at 6.36-6.45%. Both now trade 25-30bp richer, so the concession is the relative 4bp, not the outright level.</p></div>
    <div><h3>Richest</h3><ul class="tight">{''.join(li(b) for b in rich)}</ul>
      <p class="small">Rich: the low-coupon DS series (DS1029, DS1030, DS0432), which trade below par and accrue in price (favoured by held-to-maturity books),
      and the large high-coupon DS1033. WS0447 is rich against an extrapolated curve on a 1-point bid/offer, so ignore it.
      Sub-1Y PS0527/DS0727 yield {f(B['PS0527']['ytm'])}-{f(B['DS0727']['ytm'])}%, below repo, because MoF is buying them back at switch auctions.</p></div>
  </div>
  <h3>Highest yield and cheapest line per sector</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Sector</th><th class="l">Highest yield</th><th>Yield %</th><th class="l">Cheapest vs curve</th><th>R/C bp</th></tr></thead><tbody>{sec_rows}</tbody></table></div>
</section>
""")

    # ------------------------------------------------------------------ carry & roll
    ok29 = B["OK0129"]["h12"]
    w(f"""
<section class="card" id="roll">
  <h2>Roll yield, decomposed <span class="tag">effects that overlap, separated</span></h2>
  <p class="lede">Expected return to a horizon if the curve does not move, per 100 invested (dirty), split into additive pieces. The pieces overlap in everyday
  language ("carry", "roll", "yield"), so here is exactly what each one is:</p>
  <div class="decomp-eq">Total = Coupon income + Pull-to-par + Roll-down &nbsp;&nbsp;|&nbsp;&nbsp; Coupon + Pull-to-par = "yield carry" ≈ YTM × h &nbsp;&nbsp;|&nbsp;&nbsp; Excess = Total − Repo funding</div>
  <ul class="tight">
    <li><b>Coupon income</b>: coupon accrued and paid over the horizon. OK zeros have none; all their yield comes through price.</li>
    <li><b>Pull-to-par</b>: the clean price drift toward 100 at an <i>unchanged own yield</i>. It is positive for discount bonds (DS1030 at 85.6 gets +0.96%/yr) and negative for premiums
      (PS0728 at 104.8 gets −0.66%/yr). Coupon + pull together equal the yield to maturity. Adding YTM and pull-to-par double-counts.</li>
    <li><b>Roll-down</b>: the extra gain from the bond's yield sliding down the fitted curve as it ages, with its rich/cheap residual held constant.
      This is the only piece that depends on curve shape. It is large where the curve is steep: OK0129 rolls ~{f(ok29['roll_bp'], 0)}bp in 12M toward OK0128's level.</li>
    <li><b>Funding</b>: the repo cost of carrying the dirty price at {f(fund)}%. Excess return is the true "carry trade" P&amp;L. <b>Breakeven</b> is the yield rise over the horizon that wipes that excess out.</li>
    <li><b>The overlap with forwards:</b> roll-down is earned only if the curve stays put. A steep 1-3Y curve prices higher future rates
      (1y1y IRS {f(fwd_1y1y)}% vs 6M WIBOR {f(mm['wibor_6m'])}%, +{f(implied_6m_up * 100, 0)}bp). If those forwards are realised, roll is ~0 and you keep only the yield carry.
      Roll-down is therefore a view against hikes, not a free lunch.</li>
  </ul>
  <div class="tabs" id="crTabs" role="group" aria-label="Horizon"></div>
  <div class="legend"><span><i style="background:var(--s1)"></i>Coupon income</span><span><i style="background:var(--s2)"></i>Pull-to-par</span><span><i style="background:var(--s3)"></i>Roll-down</span><span><i class="tick" style="background:var(--ink)"></i>Repo funding cost</span></div>
  <div class="chart" id="crChart"></div>
  <h3>Full decomposition (12M unless noted; % of dirty price)</h3>
  <div id="crTable"></div>
  <div class="note"><b>Takeaway.</b> 12M excess return per unit of duration is highest in 2-3Y (≈{f(ex_md('OK0129'), 0)}bp for OK0129 and {f(ex_md('PS0729'), 0)}bp for PS0729).
  It falls to ≈{f(ex_md('DS0436'), 0)}bp at 10Y. Absolute excess rises with maturity ({sg(B['DS1035']['h12']['net'])}% for DS1035), but the cushion per unit of risk shrinks.
  A DV01-neutral 2s10s flattener wins in both the "MPC hikes" and "fiscal relief" scenarios, but it gives up roughly {f(ex_md('OK0129') - ex_md('DS0436'), 0)}bp a year of carry+roll.
  Use it as a hedge, not as a core position.</div>
</section>
""")

    # ------------------------------------------------------------------ Poland vs core
    if K:
        w(core_section(K, A, B))

    # ------------------------------------------------------------------ auctions & timing
    ev_rows = []
    today = asof.isoformat()
    for e in cal["events"]:
        if e["date"] < today:
            continue
        typ = {"auction": "Auction", "mpc": "MPC", "data": "Data", "flow": "Cash flow", "index": "Index", "supply": "Supply plan", "holiday": "Holiday"}[e["type"]]
        ev_rows.append(f"<tr{' class=\"hl\"' if e['type'] in ('auction', 'mpc') else ''}><td>{E(dt.date.fromisoformat(e['date']).strftime('%a %d %b %Y'))}</td>"
                       f"<td class='l'><span class='pill'>{E(typ)}</span></td><td class='l'>{E(e['title'])}</td><td class='l' style='white-space:normal;min-width:280px'>{E(e['note'])}</td></tr>")
    ra_rows = "".join(f"<tr><td>{E(r['date'])}</td><td>{E(r['offer'])}</td><td>{r['sold'] / 1000:.1f}</td><td>{r['demand'] / 1000:.1f}</td><td>{f(r['btc'])}x</td>"
                      f"<td class='l' style='white-space:normal;min-width:300px'>{E(r['lines'])}</td></tr>" for r in cal["recent_auctions"])
    cy = cyc
    w(f"""
<section class="card" id="auctions">
  <h2>Auctions, flows &amp; when to buy <span class="tag">MoF calendar</span></h2>
  <p class="lede">{E(cal['q4_plan'])} 2026 needs are fully financed (MoF, 30 Oct). Budget cash is ~PLN {mac['budget_cash_bn']}bn and 2027 pre-financing has started (~{mac['prefinancing_2027_pct']}%),
  so MoF can be flexible in December. 2027 gross needs are PLN {f(mac['gross_needs_2027_bn'], 1)}bn (net {f(mac['net_needs_2027_bn'], 1)}bn).</p>
  <div class="grid2">
    <div>
      <h3>Auction-cycle pattern — evidence</h3>
      <p class="small">Average daily change in a 13-bond 2-10Y basket yield, by session relative to the auction day.
      Sample: the {len(cy['_meta']['auctions'])} sale/switch auctions from {E(cy['_meta']['start'])} to {E(cy['_meta']['end'])}. Small sample, taken in a sell-off regime.</p>
      <div class="chart" id="cycleChart"></div>
    </div>
    <div>
      <h3>Benchmark yields and auction days</h3>
      <div class="legend"><span><i class="line" style="background:var(--s1)"></i>OK0129 (2Y)</span><span><i class="line" style="background:var(--s2)"></i>PS0731 (5Y)</span><span><i class="line" style="background:var(--s3)"></i>DS0436 (10Y)</span><span><i class="tick" style="background:var(--axis)"></i>Auction</span></div>
      <div class="chart" id="histChart"></div>
    </div>
  </div>
  <div class="callout"><b>When to buy.</b>
    <ul class="tight">
      <li><b>Buy at the auction-day close or into the auction (18 Nov, 25 Nov, 9 Dec, 16 Dec), not 2-3 days before.</b> The final offer comes out two business days ahead.
        That day ({cy['T-2']['n']} obs) averaged {sg(cy['T-2']['mean'], 1)}bp and rose {cy['T-2']['up_share'] * 100:.0f}% of the time; auction day added {sg(cy['T+0']['mean'], 1)}bp;
        the next day reversed {sg(cy['T+1']['mean'], 1)}bp ({100 - cy['T+1']['up_share'] * 100:.0f}% of the time lower). Non-auction days averaged {sg(cy['other']['mean'], 1)}bp.</li>
      <li><b>25 Nov is the better of the two November auctions.</b> WZ1126 redeems the same day (PLN ~14bn before the switch), plus WZ coupons, so reinvestment cash meets supply.</li>
      <li><b>Front end (2-3Y): scale in around the 2 Dec MPC.</b> Half before, half after. A hold triggers a relief rally (hike risk priced). A 25bp "insurance" hike is mostly priced,
        so a post-hike dip is a buying opportunity rather than a trend change. The real risk is a hiking cycle if the CPN fuel shield is not extended.</li>
      <li><b>December to January is seasonally supportive.</b> There are only two December auctions, after which supply pauses. The 25 Jan OK0127 redemption (PLN ~15bn) plus PS0130/PS0131 coupons
        (~PLN 5bn) and the end-January index extension create January demand. Be positioned before Christmas.</li>
      <li><b>Avoid</b> adding duration on the final-offer days (16 Nov, 23 Nov, ~7 Dec, ~14 Dec). Watch the December supply plan (~27-30 Nov) and the Q1 2027 plan (mid-December).</li>
    </ul>
  </div>
  <h3>Upcoming calendar</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th>Date</th><th class="l">Type</th><th class="l">Event</th><th class="l">Why it matters</th></tr></thead><tbody>{''.join(ev_rows)}</tbody></table></div>
  <h3>Recent auctions</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th>Date</th><th>Offer PLN bn</th><th>Sold bn</th><th>Demand bn</th><th>Bid/cover</th><th class="l">Lines (PLN m @ avg yield)</th></tr></thead><tbody>{ra_rows}</tbody></table></div>
</section>
""")

    # ------------------------------------------------------------------ ideas
    ds35, ds36 = B["DS1035"], B["DS0436"]
    ideas = [
        ("go", "Core: own 2-3Y (OK0129 / PS0729 / PS0130) or the GPWB 1-3Y / 1-4Y index",
         f"Best carry+roll per unit of risk on the curve: {f(ex_md('OK0129'), 0)}-{f(ex_md('PS0130'), 0)}bp of 12M excess per duration year and a 12M breakeven above 100bp. "
         f"The 1-3Y index returns {f(t13['horizons']['h12']['total'])}% over 12M on an unchanged curve, versus repo at {f(fund)}%. PKO's 1Q27 forecast puts the 2Y at 4.00%, against {f(B['OK0129']['ytm'])}% now.",
         f"Risk: an MPC hiking cycle (bear flattener: 1-3Y index {sg(t13['scenarios'][scen_names[2]]['instant'])}% instant). Entry: 18 and 25 Nov auctions, and around the 2 Dec MPC."),
        ("go", "RV switch: sell DS1029, buy PS0130",
         f"+{f(rv_pick, 0)}bp of yield at the same duration ({f(B['DS1029']['mod'])} → {f(B['PS0130']['mod'])}). About {f(rv_rc, 0)}bp of it is pure rich/cheap and the rest is curve. "
         f"PS0130 enters GPWB 1-3Y at end-January, so trackers have to buy it. DS1029 is the richest bond on the curve ({sg(B['DS1029']['rc_bp'], 1)}bp).",
         "Risk: low-coupon richness can persist (held-to-maturity demand). Low DV01 risk."),
        ("wait", "Asset-swap longs in 8-10Y (DS1035 / DS0436 vs paying IRS)",
         f"ASW {sg(ds35['asw_bp'], 0)}/{sg(ds36['asw_bp'], 0)}bp and running carry ~{f(ds36['asw_carry_bp'], 0)}bp a year, with little rate duration. Spreads are at extremes "
         "(the Sep–Oct POLGB-vs-WIBOR spread was a record). December supply is light and 2026 is already financed.",
         "Risk: fiscal and ratings (S&P negative outlook 6 Nov, Fitch negative). A further 20-30bp widening is plausible before any consolidation is credible. Build in 2-3 tranches at auctions, small size."),
        ("wait", "Buy the on-the-run auction lines (PS1031, DS0436) at the auction closes",
         f"They screen {sg(B['PS1031']['rc_bp'], 1)} and {sg(B['DS0436']['rc_bp'], 1)}bp cheap with the best liquidity, and both enter the TBSP month-end extension. "
         "Evidence: the T-2 to T0 cheapening averaged ~7bp over the last 9 auctions.",
         "Risk: outright duration. After the -30bp rally since 28 Oct, the next auction may clear higher. Let the auction concession come to you."),
        ("avoid", "Sub-1Y paper (OK0127, PS0527, DS0727) and WS0447",
         f"Yields of {f(B['OK0127']['ytm'])}-{f(B['DS0727']['ytm'])}% are below repo ({f(fund)}%) and the ASW is about −50bp: negative carry, held up by MoF switch buybacks. "
         "WS0447 has a 1-point bid/offer and no fixing.",
         "For cash, use EUR bills + EUR/PLN FX swap (next card), T-bills or POLSTR deposits instead."),
    ] + ([
        ("go", "PLN cash/short book: EUR bills or Schatz + rolling EUR/PLN FX swap instead of sub-1Y POLGBs",
         f"A 1Y Bund/Schatz hedged into PLN on the 1Y forward yields ≈{f(k_de1)}% vs {f(kh[('PL', 1)]['local'])}% for a 1Y POLGB and {f(k_sub1)}% on PS0527/DS0727, with Bund credit and daily liquidity. "
         "The forward points pay for the NBP hikes the market prices.",
         "Risk: forward points move with NBP pricing, and the quotes used are indicative. Lock the forward at execution. If the NBP hikes more than priced, short POLGBs catch up."),
        ("wait", "Long POLGB 10Y vs short Bund 10Y (DV01-matched, FX-hedged): the fiscal-premium compression trade",
         f"PL−DE 10Y at ~{f((k_last['pl10'] - k_last['de10']) * 100, 0)}bp (peak ~299bp on 28 Oct, ~245bp in early August). It carries ~{f(kc[('PL', 10)]['total_bp'] - kc[('DE', 10)]['total_bp'], 0)}bp/yr more than the Bund leg.",
         "Risk: fiscal or ratings news widens the spread. Needs a catalyst (2027 consolidation, rating stabilisation). Enter on supply-driven widening."),
    ] if K else []) + [
        ("avoid", "Outright 2s10s flattener as a core trade",
         f"It wins in both the hike and fiscal-relief scenarios but gives up about {f(ex_md('OK0129') - ex_md('DS0436'), 0)}bp a year of carry+roll (DV01-neutral).",
         "Use it only as a hedge on the front-end long if the MPC turns hawkish."),
    ]
    lab = {"go": ("go", "Play"), "wait": ("wait", "Play on entry"), "avoid": ("avoid", "Avoid")}
    w('<section class="card" id="ideas"><h2>What is worth playing <span class="tag">assessment</span></h2>'
      '<p class="lede">Ranked by risk-adjusted attractiveness. Sizing is relative: core &gt; tactical &gt; hedge.</p><div class="ideas">' + "".join(
          f'<div class="idea"><div class="hd"><b>{E(t)}</b><span class="status {lab[s][0]}">{lab[s][1]}</span></div><p>{E(b)}</p><p class="risk">{E(r)}</p></div>'
          for s, t, b, r in ideas) + "</div>"
      f'<div class="note"><b>Macro backdrop.</b> NBP held at {f(pol["nbp_reference"])}% on 4 Nov. October CPI fell to {f(mac["cpi_oct_flash"], 1)}% (flash), held down by the CPN fuel programme.'
      ' The NBP November projection has CPI at 4.2% in 2027. MPC hawks (Wnorowski, Zarzecki) flag a December or January hike, while the PAP consensus is a hold to Q3 2027.'
      f' The 2026 deficit is ~{f(mac["deficit_2026_gdp"], 1)}% of GDP; S&amp;P affirmed A- but cut the local-currency rating to A- and moved to a negative outlook (6 Nov).'
      f' Foreign holdings of POLGBs are PLN {f(mac["foreign_holdings_bn"], 1)}bn and banks own {f(mac["banks_share_pct"], 1)}%. Globally, oil near USD 95, the BoE/CNB hikes and a ~75% chance of a December Fed hike keep the long end volatile.</div></section>')

    # ------------------------------------------------------------------ all bonds + method
    w(f"""
<section class="card" id="bonds">
  <h2>All fixed-rate POLGBs <span class="tag">sortable</span></h2>
  <p class="lede">Click a column header to sort. Highlighted rows are the lines discussed above. DV01 is in PLN per 1bp per PLN 1m nominal.</p>
  <div id="bondTable"></div>
</section>
<section class="card" id="method">
  <h2>Method &amp; sources</h2>
  <ul class="tight">
    <li><b>Prices:</b> Treasury BondSpot Poland fixing, {E(A['asof'])} (<a href="{E(A['fixing_url'])}" rel="noopener">source</a>). OK0127, WS0437 and WS0447 have no fixing, so they use the mid of the {E(A['quotes_date'])} session best bid/offer.
      Yields are re-computed from clean prices: annual coupon on the 25th, Act/Act ICMA accrual, settlement T+2 = {E(settle)} (11 Nov is a holiday). They match BondSpot yields within 1bp.</li>
    <li><b>Duration:</b> Macaulay = PV-weighted time; modified = Macaulay/(1+y); convexity is standard annual. Index figures are market-value weighted with GPW Benchmark units effective 30 Oct 2026.
      The cash-flow IRR yield is also shown, because on a curve this steep the MV-weighted YTM understates the portfolio yield.</li>
    <li><b>Curve:</b> {E(mi['curve']['source'])}</li>
    <li><b>IRS / ASW:</b> {E(mi['irs']['source'])} Cross-check (unverified) quotes of 1Y 4.285 / 3Y 4.52 / 7Y 4.853 are within ~5bp of the interpolated curve.</li>
    <li><b>Money market:</b> {E(mm['source'])}</li>
    <li><b>Carry/roll:</b> per-bond horizon repricing. The fitted zero curve is held fixed by time-to-cash-flow and each bond's z-spread residual is held constant. Bonds that mature inside the horizon redeem at par and the cash earns the funding rate.</li>
    <li><b>Poland vs core:</b> Bund curve from the Bundesbank term-structure series (BBSIS, fitted yields by residual maturity); US Treasury daily par yield curve; €STR (ECB data API), SOFR/EFFR (NY Fed), EURIBOR (euribor-rates.eu);
      cross-country benchmark yields from the PAP table republished by wnp.pl; EUR swaps vs 6M EURIBOR, €STR OIS and Fed funds OIS from BlueGamma interdealer mids (6 Nov); EUR/PLN forward points from investing.com (indicative, 9 Nov);
      Poland EUR Eurobond yields from Borsa Italiana MOT (indicative). Carry+roll = (yield − local 3M rate) + duration × 1Y slide on each market's curve. Hedged yields use 1Y FX-implied rates.
      Matched-maturity swaps assume zero cross-currency basis; no published EUR/PLN basis level was found.</li>
    <li><b>Calendar &amp; supply:</b> MoF 2026 auction calendar, Q4 financing plan, November supply plan and the MoF auction database (<a href="{E(cal['_sources']['nov_2026_supply'])}" rel="noopener">Nov plan</a>,
      <a href="{E(cal['_sources']['auction_results_db'])}" rel="noopener">results DB</a>). MPC: NBP 2026 schedule. Macro: NBP projection, GUS flash CPI, MoF, PKO BP and Bank Millennium dailies of 9 Nov 2026.</li>
    <li><b>Refresh:</b> <code>python src/fetch_bondspot.py YYYY-MM-DD &amp;&amp; python src/analytics.py YYYY-MM-DD &amp;&amp; python src/build_dashboard.py YYYY-MM-DD</code>, then <code>python src/deploy.py</code>. Update data/market_inputs.json (IRS, WIBOR) and data/index_portfolios.json each month.</li>
  </ul>
  <p class="small">Not investment advice. Built for internal use; the page is unlinked and marked noindex.</p>
</section>
<footer>Generated {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · data as of {E(A['asof'])}</footer>
""")

    body = "\n".join(o)
    tpl = (ROOT / "src" / "template.html").read_text()
    data_js = json.dumps(js, separators=(",", ":"), default=str).replace("</", "<\\/")
    page = tpl.replace("<!--BODY-->", body).replace("/*DATA*/", data_js)
    out = ROOT / "dist" / "dashboard" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print("wrote", out, f"{len(page) / 1024:.0f} KB")


if __name__ == "__main__":
    main(dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 11, 9))
