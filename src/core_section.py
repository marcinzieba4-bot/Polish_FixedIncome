"""HTML for the 'Poland vs core markets' section (consumes data/analytics/core_<date>.json)."""
from __future__ import annotations

import html

E = html.escape


def f(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def sg(x, d=2):
    if x is None:
        return "–"
    r = round(x, d)
    return ("+" if r > 0 else "−" if r < 0 else "") + f"{abs(r):.{d}f}"


def core_section(K, A, B):
    I = K["inputs"]
    pol = I.get("policy", {})
    cpi = I.get("cpi", {})
    snap = {s["country"]: s for s in K["snapshot"]}
    cr = {(c["mkt"], c["T"]): c for c in K["carry_roll"]}
    hed = {(h["asset"], h["T"]): h for h in K["hedged"]}
    hs = K["spread_hist"]
    first, last = hs[0], hs[-1]
    peak = max(hs, key=lambda x: x["pl10"] - x["de10"])
    r3 = K["r3"]
    pick_eur = hed[("DE", 10)]["PLN"] - hed[("DE", 10)]["local"]
    pick_usd = hed[("US", 10)]["PLN"] - hed[("US", 10)]["local"]
    mm = A["market_inputs"]["money_market"]
    pl, de, us = snap["Poland"], snap["Germany"], snap["United States"]
    cm = {k: (cr[(k, 10)]["y"] - cr[(k, 2)]["y"]) * 100 for k in ("PL", "DE", "US")}  # constant-maturity 2s10s
    ch2 = sorted([de["ch2_12m"], us["ch2_12m"]])

    # ---------------- central banks table
    order = ["Poland", "Germany", "United States", "United Kingdom", "Czechia", "Hungary"]
    cb_rows = []
    for c in order:
        p = pol.get(c)
        if not p:
            continue
        infl = cpi.get(c, {})
        real = (p["rate"] - infl["v"]) if (p.get("rate") is not None and infl.get("v") is not None) else None
        cb_rows.append(
            f"<tr><td class='l'><b>{E(p['bank'])}</b> <span class='small'>{E(c)}</span></td><td>{f(p.get('rate'))}%</td>"
            f"<td class='l' style='white-space:normal;min-width:120px'>{E(p.get('last', ''))}</td><td class='l'>{E(p.get('next', ''))}</td>"
            f"<td class='l'><span class='status {E(p.get('tone', ''))}'>{E(p.get('stance', ''))}</span></td>"
            f"<td class='l' style='white-space:normal;min-width:220px'>{E(p.get('pricing', ''))}</td>"
            f"<td>{f(infl.get('v'), 1)}% <span class='small'>{E(infl.get('m', ''))}</span></td><td>{sg(real, 2)}</td></tr>")

    # ---------------- cross-country table
    ctry = ["Poland", "Hungary", "Czechia", "United Kingdom", "United States", "France", "Italy", "Spain", "Germany", "Japan"]
    cc_rows = "".join(
        f"<tr{' class=\"hl\"' if c == 'Poland' else ''}><td class='l'>{E(c)}</td><td>{f(snap[c]['y2'])}{'*' if snap[c]['short_tenor'] == '3Y' else ''}</td>"
        f"<td>{f(snap[c]['y5'])}</td><td>{f(snap[c]['y10'])}</td><td>{sg(snap[c]['s2s10'], 0)}</td><td>{sg(snap[c]['slope_12m_ago'], 0)}</td>"
        f"<td>{sg(snap[c]['sp_de'], 0)}</td><td>{sg(snap[c]['ch10_1m'], 0)}</td><td>{sg(snap[c]['ch10_12m'], 0)}</td><td>{sg(snap[c]['ch2_12m'], 0)}</td></tr>"
        for c in ctry if c in snap)

    # ---------------- hedged matrix
    def cell(T, a, base):
        h = hed[(a, T)]
        best = max(hed[(x, T)][base] for x in ("PL", "DE", "US"))
        v = h[base]
        return f"<td{' style=\"font-weight:600\"' if abs(v - best) < 1e-9 else ''}>{f(v)}</td>"
    lab = {"PL": "POLGB", "DE": "Bund", "US": "UST"}
    hm_rows = "".join(
        f"<tr><td class='l'>{T}Y</td><td class='l'>{lab[a]}</td><td>{f(hed[(a, T)]['local'])}</td>{cell(T, a, 'PLN')}{cell(T, a, 'EUR')}{cell(T, a, 'USD')}</tr>"
        for T in (1, 2, 5, 10) for a in ("PL", "DE", "US"))

    # ---------------- matched-maturity Bund -> PLN
    stp = K.get("swap_to_pln") or []
    if stp:
        stp_rows = "".join(
            f"<tr><td class='l'>{int(s['T'])}Y</td><td>{f(s['bund'])}</td><td>{f(s['eur_irs'])}</td><td>{sg(s['bund_asw'], 0)}</td>"
            f"<td>{f(s['pln_irs'])}</td><td>{f(s['synth_pln'])}</td><td>{f(s['polgb'])}</td><td>{sg(s['pl_asw'], 0)}</td><td><b>{sg(s['adv_pl_bp'], 0)}</b></td></tr>"
            for s in stp)
        src = I.get("eur_irs", {}).get("source", "")
        stp_html = f"""
  <h3>Bund swapped into PLN at matched maturity (asset swap + cross-currency swap)</h3>
  <p class="small">Buy the Bund, pay EUR IRS (now earning EURIBOR + Bund ASW), swap the EURIBOR leg into WIBOR with a EUR/PLN cross-currency basis swap,
  then receive PLN IRS. You end up with a PLN fixed yield of ≈ PLN IRS + Bund ASW + basis. A POLGB gives PLN IRS + POLGB ASW. So the comparison
  reduces to <b>POLGB ASW vs Bund ASW (+ basis)</b>. Basis is set to 0 here; see the sensitivity line. EUR swap source: {E(src)}</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Tenor</th><th>Bund %</th><th>EUR IRS %</th><th>Bund ASW bp</th><th>PLN IRS %</th>
  <th>Synthetic PLN yield %</th><th>POLGB %</th><th>POLGB ASW bp</th><th>POLGB advantage bp</th></tr></thead><tbody>{stp_rows}</tbody></table></div>"""
    else:
        stp_html = """<p class="small">EUR swap quotes were not available from a verifiable free source, so the matched-maturity (asset swap + CCS)
  version is not shown. The rolling-hedge table above is the conservative proxy.</p>"""

    basis_note = I.get("fx", {}).get("basis_note", "")
    lo_pl = min(B["PS0527"]["ytm"], B["DS0727"]["ytm"])
    hi_pl = max(B["PS0527"]["ytm"], B["DS0727"]["ytm"])
    de1_pln = hed[("DE", 1)]["PLN"]
    us1_pln = hed[("US", 1)]["PLN"]
    adv10_de = hed[("PL", 10)]["PLN"] - hed[("DE", 10)]["PLN"]
    adv2_de = hed[("PL", 2)]["PLN"] - hed[("DE", 2)]["PLN"]
    adv10_eur = hed[("PL", 10)]["EUR"] - hed[("DE", 10)]["EUR"]
    pl_e10 = hed[("PL", 10)]["EUR"]

    return f"""
<section class="card" id="core">
  <h2>Poland vs core markets <span class="tag">steepness · carry · central banks · FX-hedged</span></h2>
  <p class="lede">Core-market data: Bund curve (Bundesbank fitted yields, {E(K['bund_date'])}), US Treasury par curve ({E(K['ust_date'])}),
  the PAP cross-country table ({E(K['pap_date'])}), EURIBOR/€STR/SOFR. The Polish curve is the fitted POLGB curve from above.</p>
  <div class="grid3">
    <div class="ixcard"><div class="name">Steepness (2s10s, constant maturity)</div><div class="hero">{sg(cm['PL'], 0)}<small>bp Poland</small></div>
      <div class="kv"><span>Germany / US</span><b>{sg(cm['DE'], 0)} / {sg(cm['US'], 0)}bp</b>
      <span>Benchmarks now PL / DE / US</span><b>{sg(pl['s2s10'], 0)} / {sg(de['s2s10'], 0)} / {sg(us['s2s10'], 0)}</b>
      <span>…12M ago (PAP)</span><b>{sg(pl['slope_12m_ago'], 0)} / {sg(de['slope_12m_ago'], 0)} / {sg(us['slope_12m_ago'], 0)}</b></div>
      <p class="small">Core curves bear-flattened on central-bank hikes, while Poland bear-steepened on fiscal supply. That is the opposite regime.</p></div>
    <div class="ixcard"><div class="name">Carry + roll, 10Y</div><div class="hero">{f(cr[('PL', 10)]['total_bp'], 0)}<small>bp/yr Poland</small></div>
      <div class="kv"><span>Germany / US</span><b>{f(cr[('DE', 10)]['total_bp'], 0)} / {f(cr[('US', 10)]['total_bp'], 0)}bp</b>
      <span>Per duration year PL / DE / US</span><b>{f(cr[('PL', 10)]['per_dur'], 0)} / {f(cr[('DE', 10)]['per_dur'], 0)} / {f(cr[('US', 10)]['per_dur'], 0)}</b>
      <span>2Y per duration PL / DE / US</span><b>{f(cr[('PL', 2)]['per_dur'], 0)} / {f(cr[('DE', 2)]['per_dur'], 0)} / {f(cr[('US', 2)]['per_dur'], 0)}</b></div>
      <p class="small">Excess over local 3M cash, which equals what an FX-hedged investor earns under covered interest parity.</p></div>
    <div class="ixcard"><div class="name">10Y spread over Bunds</div><div class="hero">{sg((last['pl10'] - last['de10']) * 100, 0)}<small>bp</small></div>
      <div class="kv"><span>{E(first['d'])}</span><b>{sg((first['pl10'] - first['de10']) * 100, 0)}bp</b><span>Peak {E(peak['d'])}</span><b>{sg((peak['pl10'] - peak['de10']) * 100, 0)}bp</b>
      <span>vs Hungary / Czechia (PAP)</span><b>{sg((pl['y10'] - snap['Hungary']['y10']) * 100, 0)} / {sg((pl['y10'] - snap['Czechia']['y10']) * 100, 0)}bp</b></div>
      <p class="small">Poland now yields more than Hungary and Czechia at 10Y, a fiscal premium the region does not share.</p></div>
  </div>

  <h3>Central banks</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Bank</th><th>Policy rate</th><th class="l">Last move</th><th class="l">Next meeting</th><th class="l">Stance</th><th class="l">What markets price</th><th>Latest CPI</th><th>Real policy rate</th></tr></thead>
  <tbody>{''.join(cb_rows)}</tbody></table></div>
  <p class="small">{E(I.get('policy_note', ''))}</p>

  <div class="grid2" style="margin-top:6px">
    <div><h3>Yield curves</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>Poland (fitted)</span><span><i class="line" style="background:var(--s2)"></i>US Treasury</span><span><i class="line" style="background:var(--s3)"></i>Germany (Bundesbank)</span></div><div class="chart" id="coreCurves"></div></div>
    <div><h3>Carry + roll by market (bp/yr over local 3M)</h3><div class="legend"><span><i style="background:var(--s1)"></i>Carry (yield − 3M)</span><span><i style="background:var(--s2)"></i>Roll-down return</span><span>label: total (per duration year)</span></div><div class="chart" id="coreCarry"></div></div>
  </div>
  <div class="grid2">
    <div><h3>Poland spreads, Aug–Nov</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>PL−DE 10Y</span><span><i class="line" style="background:var(--s2)"></i>PL−US 10Y</span><span><i class="line" style="background:var(--s3)"></i>PL−DE 2Y</span></div><div class="chart" id="coreSpreads"></div></div>
    <div><h3>2s10s slope, Aug–Nov</h3><div class="legend"><span><i class="line" style="background:var(--s1)"></i>Poland</span><span><i class="line" style="background:var(--s2)"></i>US</span><span><i class="line" style="background:var(--s3)"></i>Germany</span></div><div class="chart" id="coreSlopes"></div></div>
  </div>

  <h3>Cross-country snapshot (PAP, {E(K['pap_date'])})</h3>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Country</th><th>2Y %</th><th>5Y %</th><th>10Y %</th><th>2s10s bp</th><th>2s10s 12M ago</th><th>10Y vs Bund bp</th><th>10Y Δ1M bp</th><th>10Y Δ12M bp</th><th>2Y Δ12M bp</th></tr></thead>
  <tbody>{cc_rows}</tbody></table></div>
  <p class="small">* Hungary short tenor is 3Y. Source: <a href="{E(K['pap_url'])}" rel="noopener">PAP via wnp.pl</a>. The PAP "2Y" for Poland is the OK0129 benchmark (2.2Y), slightly above the fitted 2.0Y point used in the carry figures.</p>

  <h3>FX-hedged yields: who pays most in your own currency? (rolling 3M FX hedge)</h3>
  <p class="small">Hedged yield = local yield + (3M rate of your currency − 3M rate of the bond's currency), using covered-interest-parity forwards from
  WIBOR 3M {f(r3['PLN'])}%, EURIBOR 3M {f(r3['EUR'])}% and USD 3M {f(r3['USD'])}% (3M T-bill as the USD proxy). A PLN investor is paid ≈{sg(pick_eur)}%/yr to hedge EUR assets
  and pays ≈{sg(pick_usd)}%/yr to hedge USD assets. Bold marks the highest hedged yield per tenor and currency.</p>
  <div class="tablewrap"><table class="t"><thead><tr><th class="l">Tenor</th><th class="l">Bond</th><th>Local %</th><th>Hedged into PLN %</th><th>Hedged into EUR %</th><th>Hedged into USD %</th></tr></thead><tbody>{hm_rows}</tbody></table></div>
  {stp_html}
  <div class="note"><b>Does "buy Bund, swap into PLN" make sense?</b>
    <ul class="tight">
      <li><b>From 2Y out, no.</b> POLGBs beat hedged Bunds by {f(adv2_de * 100, 0)}bp at 2Y and {f(adv10_de * 100, 0)}bp at 10Y (rolling hedge). Matched-maturity, the gap is the POLGB-minus-Bund asset-swap spread,
        roughly 100bp at 5-10Y. For the Bund route to win, the EUR/PLN cross-currency basis would have to move by about a full percentage point. That is far outside anything seen for a liquid pair like EUR/PLN.</li>
      <li><b>At the very front end, yes.</b> Sub-1Y POLGBs (PS0527/DS0727) yield {f(lo_pl)}-{f(hi_pl)}%, below repo. A 1Y German bill or Schatz hedged into PLN gives ≈{f(de1_pln)}%, and a 1Y UST
        ≈{f(us1_pln)}%. For a PLN liquidity book, EUR bills plus a rolling EUR/PLN FX swap pick up ~{f((de1_pln - hi_pl) * 100, 0)}-{f((de1_pln - lo_pl) * 100, 0)}bp over short POLGBs, with Bund credit.
        The pickup depends on the FX-swap-implied PLN rate. If FX swaps price PLN below WIBOR (a negative basis for the PLN holder), the gain shrinks one for one.</li>
      <li><b>For EUR-based money, the trade runs the other way.</b> POLGB 10Y hedged into EUR ≈ {f(pl_e10)}%, which is {f(adv10_eur * 100, 0)}bp over Bunds, against ~150bp for French OATs and ~110bp for Italian BTPs unhedged.
        The rolling hedge leaves you exposed to the PLN-EUR short-rate gap: an NBP hike raises your hedge cost.</li>
      <li><b>Basis data caveat.</b> {E(basis_note)}</li>
    </ul>
  </div>
  <div class="note"><b>Takeaways vs core.</b>
    <ul class="tight">
      <li><b>Policy divergence:</b> the ECB, Fed, BoE and CNB are hiking or about to hike into the energy shock, while the NBP is on a hawkish hold. Hence the 12M changes: core 2Y yields are up ~{f(ch2[0], 0)}-{f(ch2[1], 0)}bp versus {f(pl['ch2_12m'], 0)}bp in Poland.
        If the NBP joins with "insurance" hikes, the Polish front end has catching up to do. That is the main risk to the 2-3Y carry trade.</li>
      <li><b>Term premium is Polish-specific:</b> PL 2s10s {sg(cm['PL'], 0)}bp vs DE {sg(cm['DE'], 0)} and US {sg(cm['US'], 0)}bp (constant maturity), with a 10Y spread over Bunds of ~{f((last['pl10'] - last['de10']) * 100, 0)}bp, wider than HU and CZ.
        This is the asset-swap/fiscal premium from the earlier section, not inflation expectations.</li>
      <li><b>Carry is where Poland wins:</b> {f(cr[('PL', 10)]['total_bp'], 0)}bp/yr of carry+roll at 10Y vs ~{f(cr[('DE', 10)]['total_bp'], 0)}-{f(cr[('US', 10)]['total_bp'], 0)}bp in Bunds/USTs, and {f(cr[('PL', 2)]['per_dur'], 0)}bp per duration year at 2Y vs {f(cr[('DE', 2)]['per_dur'], 0)}-{f(cr[('US', 2)]['per_dur'], 0)}bp.
        Hedged, that edge survives intact. Core bonds are the hedge, not the carry trade.</li>
      <li><b>Relative-value angle:</b> if the fiscal premium compresses (credible 2027 consolidation, rating stabilisation), PL−DE 10Y can retrace toward its August level (~{f((first['pl10'] - first['de10']) * 100, 0)}bp).
        A long POLGB 10Y vs short Bund 10Y (DV01-matched, FX-hedged) isolates that view and carries ~{f(cr[('PL', 10)]['total_bp'] - cr[('DE', 10)]['total_bp'], 0)}bp/yr.</li>
    </ul>
  </div>
</section>
"""
