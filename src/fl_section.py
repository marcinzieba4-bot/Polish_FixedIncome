"""HTML for the 'Floaters, linkers & quasi-sovereigns' section."""
from __future__ import annotations

import html
import json
import pathlib

E = html.escape
ROOT = pathlib.Path(__file__).resolve().parents[1]


def f(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def sg(x, d=2):
    if x is None:
        return "–"
    r = round(x, d)
    return ("+" if r > 0 else "−" if r < 0 else "") + f"{abs(r):.{d}f}"


def quasi_html(B):
    p = ROOT / "data" / "quasi.json"
    if not p.exists():
        return ""
    Q = json.loads(p.read_text())
    rows = []
    for r in Q.get("bonds", []):
        rows.append(f"<tr><td class='l'>{E(r['ticker'])}</td><td class='l'>{E(r.get('issuer', ''))}</td><td class='l' style='white-space:normal;min-width:110px;max-width:170px'>{E(r.get('coupon_desc', ''))}</td>"
                    f"<td>{E(r.get('maturity', ''))}</td><td>{f(r.get('outstanding_bn'), 1)}</td><td>{f(r.get('yield'))}</td><td>{f(r.get('polgb_same'))}</td>"
                    f"<td><b>{sg(r.get('spread_polgb_bp'), 0)}</b></td><td>{sg(r.get('asw_bp'), 0)}</td><td class='l' style='white-space:normal;min-width:160px;max-width:240px'>{E(r.get('note', ''))}</td></tr>")
    bullets = "".join(f"<li>{x}</li>" for x in Q.get("takeaways_html", []))
    return f"""
  <h3>Quasi-sovereigns (BGK, PFR)</h3>
  <p class="small">{E(Q.get('lede', ''))}</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Series</th><th class="l">Issuer</th><th class="l">Coupon</th><th>Maturity</th><th>Out. PLN bn</th><th>Yield %</th><th>POLGB same mat. %</th><th>Spread vs POLGB bp</th><th>ASW bp</th><th class="l">Price / note</th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table></div>
  <div class="note"><b>Quasi-sovereign takeaways.</b><ul class="tight">{bullets}</ul></div>
  <p class="small">{E(Q.get('sources', ''))}</p>"""


def fl_section(FL, A, B):
    fl = FL["floaters"]
    wz = [x for x in fl if x["ticker"].startswith("WZ")]
    nz = [x for x in fl if x["ticker"].startswith("NZ")]
    by = {x["ticker"]: x for x in fl}
    best = max(wz, key=lambda x: x["dm_per_sdur"])
    sweet = [x for x in wz if 2.5 <= x["ttm"] <= 4.2]
    long_wz = [x for x in wz if x["ttm"] > 4.5]
    rows = "".join(
        f"<tr{' class=\"hl\"' if x in sweet else ''}><td class='l'>{E(x['ticker'])}</td><td class='l'>{E(x['index'])}</td><td>{E(x['maturity'])}</td><td>{f(x['ttm'], 2)}</td>"
        f"<td>{f(x['clean'], 2)}</td><td>{f(x['current_coupon'], 2)}</td><td>{sg(x['dm_bp'], 0)}</td><td><b>{sg(x['dm_wibor_eq_bp'], 0)}</b></td>"
        f"<td>{f(x['spread_dur'], 2)}</td><td>{f(x['rate_dur'], 2)}</td><td>{sg(x['fixed_asw_bp'], 0)}</td><td><b>{sg(x['vs_fixed_bp'], 0)}</b></td>"
        f"<td>{f(x['dm_per_sdur'], 1)}</td><td>{sg(x['carry_12m'], 2)}</td><td>{f(x['outstanding_bn'], 1)}</td><td class='l'>{E(x['src'])}</td></tr>"
        for x in fl)
    lk = FL["linkers"]
    sc_names = list(lk[0]["total_12m"].keys()) if lk else []
    lrows = "".join(
        f"<tr><td class='l'>{E(x['ticker'])}</td><td>{E(x['maturity'])}</td><td>{f(x['real_coupon'], 2)}</td><td>{f(x['clean'], 2)}</td><td><b>{f(x['real_yield'], 2)}</b></td>"
        f"<td>{f(x['nominal_fit'], 2)}</td><td><b>{f(x['breakeven'], 2)}</b></td><td>±{f(x['be_bid_ask_bp'] / 2 if x['be_bid_ask_bp'] else None, 0)}</td><td>{f(x['real_mod'], 2)}</td>"
        + "".join(f"<td>{sg(x['vs_nominal_12m'][k], 2)}</td>" for k in sc_names) + f"<td>{f(x['outstanding_bn'], 1)}</td></tr>"
        for x in lk)
    be_cpi = {x["ticker"]: (list(x["total_12m"].values())[1] - x["vs_nominal_12m"][sc_names[1]]) - x["real_carry_12m"] for x in lk} if lk else {}
    mac = A["market_inputs"]["macro"]
    return f"""
<section class="card" id="floaters">
  <h2>Floaters (WZ, NZ), linkers (IZ) &amp; quasi-sovereigns <span class="tag">spread vs duration</span></h2>
  <p class="lede"><b>WZ</b> pays 6M WIBOR flat (average of three fixings before each period, semi-annual); <b>NZ</b> pays compounded POLSTR flat (Mar/Sep). There is no quoted margin,
  so the value is in the price: the <b>discount margin (DM)</b> is the spread over the projected index that reprices the bond. I bootstrapped a 6M WIBOR forward curve from the full PLN swap curve
  (it humps to ≈{f(FL['fwd_6m'][1]['f'])}% six months ahead, the priced hikes). NZ forwards = WIBOR forwards − {f(FL['polstr_basis'] * 100, 0)}bp (realised WIBOR-POLSTR gap over the last NZ period;
  running period assumed at {f(FL['nz_running'])}%). The <b>WIBOR-equivalent DM</b> is directly comparable with a fixed bond's ASW (yield − PLN IRS): both are spread over WIBOR.</p>
  <div class="legend"><span><i class="line" style="background:var(--s1);opacity:.6"></i>Fixed POLGB ASW (each dot a bond)</span><span><i class="dot" style="background:var(--s2)"></i>WZ discount margin</span><span><i style="background:var(--s3)"></i>NZ discount margin, WIBOR-equivalent</span></div>
  <div class="chart" id="flChart"></div>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bond</th><th class="l">Index</th><th>Maturity</th><th>Yrs</th><th>Price</th><th>Current cpn %</th><th>DM vs index</th><th>DM WIBOR-eq.</th>
  <th>Spread dur.</th><th>Rate dur.</th><th>Fixed ASW same mat.</th><th>Floater − fixed</th><th>DM per spread-dur. yr</th><th>12M carry vs repo %</th><th>Out. bn</th><th class="l">Price</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="note"><b>What's worth it, by tenor (spread vs duration).</b>
    <ul class="tight">
      <li><b>Short end (≤2Y): floaters beat fixed paper.</b> WZ1127 trades at WIBOR {sg(by['WZ1127']['dm_bp'], 0)}bp and WZ0528 at {sg(by['WZ0528']['dm_bp'], 0)}bp, against fixed ASW of {sg(by['WZ1127']['fixed_asw_bp'], 0)} / {sg(by['WZ0528']['fixed_asw_bp'], 0)}bp.
        Short fixed bonds are expensive vs swaps, while short floaters sit near flat. For a liquidity book, WZ beats OK/PS paper by {f(min(by['WZ1127']['vs_fixed_bp'], by['WZ0528']['vs_fixed_bp']), 0)}-{f(max(by['WZ1127']['vs_fixed_bp'], by['WZ0528']['vs_fixed_bp']), 0)}bp with no rate risk.</li>
      <li><b>Sweet spot: 3-4Y WZ ({', '.join(x['ticker'] for x in sweet)}).</b> DM {f(min(x['dm_bp'] for x in sweet), 0)}-{f(max(x['dm_bp'] for x in sweet), 0)}bp, the highest on the WZ curve, with ~{f(sum(x['dm_per_sdur'] for x in sweet) / len(sweet), 0)}bp of DM per year of spread duration
        and rate duration ≈0 (WZ0330/WZ0930 are fixed until March at 3.88%, so ~0.3). They also pay {sg(min(x['vs_fixed_bp'] for x in sweet), 0)} to {sg(max(x['vs_fixed_bp'] for x in sweet), 0)}bp more than the fixed ASW at the same maturity.
        <b>This is the cleanest way to own Polish spread while the MPC hike risk is open:</b> 12M carry over repo ≈{f(max(x['carry_12m'] for x in sweet))}% with zero duration.</li>
      <li><b>Beyond 4.5Y, fixed bonds swapped give more spread.</b> {', '.join(f"{x['ticker']} DM {sg(x['dm_bp'], 0)}bp vs fixed ASW {sg(x['fixed_asw_bp'], 0)}bp" for x in long_wz)}.
        Long WZ flatten out while fixed ASW keeps widening (supply sits in fixed PS/DS). To own 5-10Y spread, asset-swap a fixed line (PS1031, DS0436) rather than buy WZ1131/WZ0533.</li>
      <li><b>NZ (POLSTR) floaters</b> look cheap in their own index ({', '.join(f"{x['ticker']} {sg(x['dm_bp'], 0)}" for x in nz)}bp over POLSTR), but in WIBOR terms they sit
        {f(min(-x['vs_fixed_bp'] for x in nz), 0)}-{f(max(-x['vs_fixed_bp'] for x in nz), 0)}bp below the fixed ASW curve. The verdict hinges on the WIBOR-POLSTR gap: at {f(FL['polstr_basis'] * 100, 0)}bp, NZ is fair to rich.
        If you think POLSTR will run closer to WIBOR (smaller gap, e.g. as WIBOR is phased out), NZ0331/NZ0332 become the better floaters. They are also the lines MoF keeps tapping, which keeps them cheap.</li>
      <li><b>Duration lens:</b> per unit of spread duration, the best floater is {E(best['ticker'])} ({f(best['dm_per_sdur'], 0)}bp/yr). The fixed 2-3Y bonds earn ~80-100bp of carry+roll per duration year (see Carry &amp; roll),
        but that comes with real rate duration. In a hike scenario, the floater wins. In a no-hike scenario, fixed 2-3Y wins through roll-down.</li>
    </ul>
  </div>

  <h3>Inflation-linked IZ: real yields and breakevens</h3>
  <p class="small">IZ bonds pay a real coupon on CPI-indexed principal and are quoted in real (unindexed) prices. Real yields are from the price with annual 25-Aug coupons.
  Breakeven = (1+nominal)/(1+real) − 1 against the fitted nominal curve at the same maturity. The 12M comparison adds real carry plus a CPI-indexation scenario and compares with the nominal neighbour's 12M carry+roll.
  Indexation lag and seasonality are ignored.</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bond</th><th>Maturity</th><th>Real cpn %</th><th>Price</th><th>Real yield %</th><th>Nominal (fit) %</th><th>Breakeven %</th><th>BE bid/ask</th><th>Real MD</th>
  {''.join(f'<th>12M vs nominal @ CPI {E(k)}</th>' for k in sc_names)}<th>Out. bn</th></tr></thead><tbody>{lrows}</tbody></table></div>
  <div class="note"><b>Linkers.</b>
    <ul class="tight">
      <li><b>Breakevens are at the target, not at the projection.</b> {', '.join(f"{x['ticker']} {f(x['breakeven'])}%" for x in lk)}, vs the NBP November projection of CPI 4.2% in 2027 (4.6% in Q1-Q2 2027) and 2.8% in 2028, and the 2.5% target.
        The market prices a fast return to target. Linkers win if inflation stays sticky (CPN fuel shield expiring, energy prices).</li>
      <li><b>Carry is the trade:</b> next year's indexation (~4% on the NBP path) is well above the breakevens, so on 12M carry IZ beat nominals by {', '.join(f"{sg(x['vs_nominal_12m'][sc_names[1]])}% ({x['ticker']})" for x in lk)}.
        12M CPI needed to match the nominal neighbour: ≈{', '.join(f"{f(be_cpi[x['ticker']], 1)}% for {x['ticker']}" for x in lk)}. The nominal side even includes its roll-down.</li>
      <li><b>Prefer IZ0836:</b> higher real yield ({f(lk[-1]['real_yield'])}%), lower breakeven, larger line (PLN {f(lk[-1]['outstanding_bn'], 0)}bn) and a tighter bid/offer in breakeven terms.
        The trade is long IZ0836 vs short DS0436/WS0437 (real-duration weighted), a breakeven widener with positive carry while CPI runs above ~3%.</li>
      <li><b>Risks:</b> a 0.75-0.85 point bid/offer (~±5-8bp of breakeven), thin trading, and a government extending the energy/fuel shields that hold CPI down
        (the NBP projection assumes no extension).</li>
    </ul>
  </div>
  {quasi_html(B)}
</section>
"""
