"""Per-day point-in-time narrative for the 1-30 Apr 2026 reports -> apr/facts_days.json (merged into the day specs).
Every statement below sits in the window in which it was first published (research/facts_*.json, notes_*.md)."""
import copy, json, pathlib, sys
SP = pathlib.Path('/tmp/claude-0/-home-user-Polish-FixedIncome/24a3fc3c-8e3f-5cce-b7fb-dcdc0e9e199e/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from wk_apr import WK_PL, AB, US, EZ, UK, GLOB  # noqa: E402
F0 = json.load(open(REPO / 'data/snapshots/2026-03-31/facts.json'))
Q0 = json.load(open(REPO / 'data/snapshots/2026-03-31/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_apr_fix/fixings.json'))['by_date']
CV = {**json.load(open(SP / 'agent_apr_curves1/curves.json')), **json.load(open(SP / 'agent_apr_curves2/curves.json'))}
P2 = json.load(open(SP / 'agent_apr_plfacts2/facts.json'))
OPS = {o['date']: o for o in P2['mof_ops'] if isinstance(o, dict) and o.get('lines')}
RS = ['01', '02', '07', '08', '09', '10', '13', '14', '15', '16', '17', '20', '21', '22', '23', '24', '27', '28', '29', '30']
DAYS = [f'2026-04-{d}' for d in RS]
CUTS = ['2026-03-31'] + [f'2026-04-{d}' for d in ['01', '02', '07', '08', '09', '10', '13', '14', '15', '16', '17', '20', '21', '22', '23', '24', '27', '28', '29']]
WINS = ['31 Mar', '1 Apr', '2-6 Apr', '7 Apr', '8 Apr', '9 Apr', '10-12 Apr', '13 Apr', '14 Apr', '15 Apr', '16 Apr', '17-19 Apr', '20 Apr', '21 Apr',
        '22 Apr', '23 Apr', '24-26 Apr', '27 Apr', '28 Apr', '29 Apr']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
ge = lambda R, d: R >= '2026-04-' + d
lab = lambda C: f"{int(C[8:])} {'Mar' if C[5:7] == '03' else 'Apr'}"
A = lambda dt_, ty, ti, no='', sd='': dict(date=dt_, type=ty, title=ti, note=no, source_date=sd)


def latest(dct, R):
    k = max([kk for kk in dct if ge(R, kk)], default=None)
    return dct[k] if k else None


def ops_add(R):
    out = []
    for d, need in (('2026-04-15', '16'), ('2026-04-23', '24'), ('2026-04-28', '29')):
        if not ge(R, need):
            continue
        o = OPS[d]
        out.append(dict(date=d, settle=o['settlement'], type='S', op='AS',
                        lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]))
        out.append(dict(date=d, settle=o['additional_sale']['settlement'], type='S', op='OB',
                        lines=[dict(series=s, sold=q, demand=None, avg_yld=None, price=None) for s, q in o['additional_sale']['lines'].items() if q]))
    return out


OUT = {}
for R in DAYS:
    d = R[8:]; C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; L = lab(C)
    x = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    pr = f"roughly {abs(x)}bp of NBP {'cuts' if x > 0 else 'hikes'}" if abs(x) >= 5 else "no net NBP move"
    fra_s = f"FRAs at the {L} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price {pr} within 12 months."
    held = ge(R, '10')
    # ---------------- policy
    V = ["The MPC held at 3.75% on 9 Apr; Glapiński sees no near-term change either way - hikes only in a 'black scenario' of renewed war, a question mark over cuts." if held else
         "The MPC cut to 3.75% on 4 Mar (a 'hawkish cut'); the 8-9 Apr meeting is expected to hold" + (" (PAP survey: through H1 2027)." if ge(R, '09') else ".")]
    mpc = latest({'01': "Dąbrowski (26 Mar): the MPC leans to holding rather than hiking; Tyrowicz (24 Mar) sees 4.75% as appropriate.",
                  '07': "Kotecki (2 Apr): the March cut was the last this year; Litwiniuk (2 Apr): no cuts soon, hikes possible if inflation worsens.",
                  '14': "March minutes (13 Apr): most members saw a much lower chance of further cuts; Janczyk: rates flat for the coming quarters.",
                  '15': "Kotecki (14 Apr): unchanged at least until the July projection; Janczyk: hikes only if CPI stays above 3.75% for three months.",
                  '20': "Wnorowski (17 Apr): rates stable for longer, but signal hike risk if inflation does not stay moderate given loose fiscal policy.",
                  '24': "Zarzecki (23 Apr): unchanged for long, any move likely up; Tyrowicz: wages still an inflation risk.",
                  '28': "Zarzecki (23 Apr): any move likely up; the March voting record (27 Apr) shows Wnorowski and Tyrowicz voted against the cut."}, R)
    V.append(mpc)
    V.append(("March CPI 3.0% (final, 15 Apr; flash 31 Mar, 3.3% expected)" if ge(R, '16') else "March flash CPI 3.0% (31 Mar; 3.3% expected)") + ("; core 2.7% (16 Apr)." if ge(R, '17') else "; core 2.5% in February."))
    V.append(latest({'01': "The fuel package (VAT 8%, minimum excise) takes ~0.9pp off April CPI (ING, PKO).",
                     '14': "The fuel VAT and excise cuts run to 30 Apr (13 Apr).", '28': "The fuel VAT and excise cuts were extended to 15 May (27 Apr)."}, R))
    pricing = fra_s + " " + " ".join(V)
    risk = latest({'01': "War and oil set the direction: FRAs price NBP hikes the MPC says it does not plan; escalation would lift the front end further, a ceasefire would unwind hike pricing. Long end: global term premia (Bund ~3%) and the fiscal cost of the fuel shield.",
                   '09': "The ceasefire unwound much of the hike pricing; the risk is a breakdown of the truce (Hormuz still largely shut) re-pricing hikes, while the MPC's bar for a move either way is high. Long end: three April sales plus the USD issue, and a ~7% deficit.",
                   '14': "Two-sided: Hormuz headlines swing oil by up to 10% a day; the MPC holds at least until July (Kotecki), so the front end is anchored near WIBOR while 5-10Y follows Bunds and oil. Supply: April sales of PLN 15-39bn.",
                   '22': "Upside risk to yields: strong March activity and wage data, hawkish MPC voices and ECB/BoE hikes priced keep NBP-hike pricing alive while oil climbs back above $100; a US-Iran deal is the relief valve. Long end: a 2026 deficit of ~6.8% of GDP and weekly supply."}, R)
    policy = dict(nbp_reference=3.75, next_mpc_label=("MPC next: 5-6 May" if held else "MPC next: 8-9 Apr"), pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = dict(v=3.0, m=("Mar (GUS final, 15 Apr; 1.1% m/m)" if ge(R, '16') else "Mar flash (GUS, 31 Mar; 3.3% expected)") + ("; core 2.7%" if ge(R, '17') else "; core 2.5% (Feb)"))
    proj = ("NBP March projection (4 Mar; data to 19 Feb, war excluded): CPI 50% bands 1.6-2.9% (2026), 1.1-3.7% (2027); central path 2.3% / 2.4% / 2.3% (2026-28), GDP 3.9% in 2026 (Inflation Report, 6 Mar)"
            + ("; the NBP forecaster survey (1 Apr) has 2026 CPI at 2.9%" if ge(R, '02') else "") + ("; IMF (14 Apr): 2026 CPI 3.3%" if ge(R, '15') else "") + ". The next projection comes in July.")
    fiscal = ("2025 general-government deficit " + ("7.3% of GDP (GUS EDP, 22 Apr), debt 59.7%" if ge(R, '23') else "7.2% of GDP (GUS preliminary, 1 Apr), debt 59.7%" if ge(R, '02') else "~7.0% of GDP (MoF figures in Fitch)")
              + "; 2026 deficit cap PLN 271.7bn" + ("; S&P (2-6 Apr) sees a 2026 deficit of 7.0% of GDP (8.0% in an oil-shock case)" if ge(R, '07') else "")
              + ("; budget deficit after March PLN 69.6bn (25.6% of the limit)" if ge(R, '15') else "; budget deficit after February PLN 48.5bn")
              + ("; the fiscal notification (22 Apr) has a 2026 deficit of ~6.8% of GDP and debt 65.1%" if ge(R, '23') else "")
              + ("; the government's assumptions (28 Apr): GDP 3.6%, deficit 6.8%" if ge(R, '29') else "")
              + "; fuel package (VAT 8%, minimum excise, price caps) " + ("extended to 15 May (27 Apr)" if ge(R, '28') else "to 30 Apr" if ge(R, '14') else "from 27-31 Mar")
              + ("; the EC sent the SAFE loan agreement (23 Apr)" if ge(R, '24') else "") + ".")
    fin = latest({'01': "~41% (end-Q1)", '27': "~48% (after 23 Apr, Erste)", '29': "~49% (after 28 Apr, MoF)"}, R)
    frisk = (f"2026 needs {fin} financed" + ("; USD 6bn of 5Y/10Y/30Y priced on 7 Apr (UST +65/+105/+130bp)" if ge(R, '08') else "")
             + ("; budget accounts PLN 169.5bn at end-March" if ge(R, '10') else "; budget accounts ~PLN 167bn at end-March (MoF estimate)")
             + ". No rating action in April; S&P reviews Poland on 8 May (A-, stable); Fitch A- and Moody's A2 have negative outlooks.")
    base = (("The NBP cut to 3.75% on 4 Mar and held on 9 Apr" if held else "The NBP cut to 3.75% on 4 Mar (next MPC 8-9 Apr)") + "; March CPI 3.0% y/y"
            + ("; 2025 GDP 3.6%, Q4 revised to 4.1%." if ge(R, '17') else "; 2025 GDP 3.6%, Q4 4.0%.") + " Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable.")
    macro = dict(cpi=cpi, projection_text=proj, fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + WK_PL[d] + " Abroad: " + AB[d])
    # ---------------- calendar
    plan = ("MoF April plan (31 Mar): sale auctions on 15 Apr (PLN 4-12bn; OK0128, NZ0331, PS0731, DS1035, NZ0936), 23 Apr (6-14bn) and 28 Apr (5-13bn; new 10Y DS0436 replaces DS1035 from 23 Apr); "
            "no switch; a 50-week T-bill on 10 Apr (3-6bn). Q2 plan: 7-8 sales for PLN 50-90bn and 1-2 switches. 2026 needs ~41% financed at end-Q1.")
    if ge(R, '08'):
        plan += " 7 Apr: USD 6bn issue (5Y 4.645%, 10Y 5.405%, 30Y 6.233%)."
    if ge(R, '13'):
        plan += " 10 Apr T-bill: PLN 3.0bn at 3.95% (demand 3.6bn) plus 0.39bn."
    if R in ('2026-04-14', '2026-04-15'):
        plan += " 15 Apr offer (13 Apr): PLN 6-12bn, WS0428 added."
    if ge(R, '16'):
        o = OPS['2026-04-15']; ls = {l['series']: l for l in o['lines']}
        plan += (f" 15 Apr sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn demand (cover {o['total_demand_mn']/o['total_sold_mn']:.2f}) plus {o['additional_sale']['total_mn']/1000:.2f}bn; "
                 f"PS0731 {ls['PS0731']['avg_yield']:.3f}%, DS1035 {ls['DS1035']['avg_yield']:.3f}%, WS0428 {ls['WS0428']['avg_yield']:.3f}%.")
    if R in ('2026-04-22', '2026-04-23'):
        plan += " 23 Apr offer (21 Apr): PLN 7-12bn incl. the new DS0436."
    if ge(R, '24'):
        o = OPS['2026-04-23']; ls = {l['series']: l for l in o['lines']}
        plan += (f" 23 Apr sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn (cover {o['total_demand_mn']/o['total_sold_mn']:.2f}) plus {o['additional_sale']['total_mn']/1000:.2f}bn; "
                 f"DS0436 debut {ls['DS0436']['avg_yield']:.3f}%, PS0731 {ls['PS0731']['avg_yield']:.3f}%.")
    if R == '2026-04-28':
        plan += " 28 Apr offer (27 Apr): PLN 5-10bn (OK0128, NZ0331, PS0731, DS1034, DS0436, NZ0936)."
    if ge(R, '29'):
        o = OPS['2026-04-28']; ls = {l['series']: l for l in o['lines']}
        plan += (f" 28 Apr sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn (cover {o['total_demand_mn']/o['total_sold_mn']:.2f}) plus {o['additional_sale']['total_mn']/1000:.2f}bn; "
                 f"DS0436 {ls['DS0436']['avg_yield']:.3f}%, PS0731 {ls['PS0731']['avg_yield']:.3f}%; ~49% of 2026 needs financed.")
    if ge(R, '17'):
        plan += " BGK FPC (16 Apr): PLN 1.06bn sold on 1.89bn demand plus 0.21bn."
    if ge(R, '30'):
        plan += " BGK FPC (29 Apr): PLN 0.69bn on 0.94bn demand."
    left = [s for s, need in (('15 Apr', '15'), ('23 Apr', '23'), ('28 Apr', '28')) if not ge(R, need) or R == f'2026-04-{need}']
    timing = ("The Aug 2025-Feb 2026 pattern (auction-day close the cheapest point of the week) comes from a rally regime; March's sell-off broke it. "
              + (f"April is back to regular supply: remaining sales {', '.join(left)}. " if left else "April supply is done (PLN 28.7bn sold plus 1.65bn additional); the May plan is due at month-end. "))
    timing += ("MPC 8-9 Apr: a hold is expected." if not held else "Next MPC 5-6 May: a hold is expected; the July projection is the next marker.")
    if ge(R, '16'):
        timing += f" Covers so far: 1.13 (15 Apr)" + (", 1.25 (23 Apr)" if ge(R, '24') else "") + (", 1.23 (28 Apr)" if ge(R, '29') else "") + " vs 1.17 on 25 Mar."
    ev = []
    if not held:
        ev.append(A('2026-04-09', 'MPC', 'MPC decision (8-9 Apr) + Glapiński press conference', 'Hold expected (PAP survey, 8 Apr).' if ge(R, '09') else 'Hold expected.', 'NBP schedule'))
    ev += [A('2026-04-10', 'Auction', 'MoF 50-week T-bill (PLN 3-6bn)', '', 'MoF April plan, 31 Mar'), A('2026-04-10', 'Data', 'US March CPI', '', 'BLS calendar'),
           A('2026-04-15', 'Data', 'GUS final March CPI', '', 'GUS calendar'),
           A('2026-04-15', 'Auction', 'MoF sale auction PLN ' + ('6-12bn' if ge(R, '14') else '4-12bn'), 'OK0128, WS0428, NZ0331, PS0731, DS1035, NZ0936.' if ge(R, '14') else '', 'MoF offer, 13 Apr' if ge(R, '14') else 'MoF April plan, 31 Mar'),
           A('2026-04-16', 'Data', 'NBP core inflation (March)', '', 'NBP calendar'),
           A('2026-04-21', 'Data', 'GUS March wages, industry, PPI, construction', '', 'GUS calendar'),
           A('2026-04-23', 'Data', 'GUS March retail sales', '', 'GUS calendar'),
           A('2026-04-23', 'Auction', 'MoF sale auction PLN ' + ('7-12bn' if ge(R, '22') else '6-14bn'), 'Incl. the new 10Y DS0436.' if ge(R, '22') else 'New 10Y DS0436 on offer.', 'MoF offer, 21 Apr' if ge(R, '22') else 'MoF April plan, 31 Mar'),
           A('2026-04-28', 'Auction', 'MoF sale auction PLN ' + ('5-10bn' if ge(R, '28') else '5-13bn'), 'OK0128, NZ0331, PS0731, DS1034, DS0436, NZ0936.' if ge(R, '28') else '', 'MoF offer, 27 Apr' if ge(R, '28') else 'MoF April plan, 31 Mar'),
           A('2026-04-28', 'CB', 'MNB decision', '', 'MNB calendar'),
           A('2026-04-29', 'CB', 'FOMC decision', '', 'Fed calendar'),
           A('2026-04-30', 'CB', 'ECB, BoE decisions', 'Holds expected; hikes priced from June.' if ge(R, '28') else '', 'CB calendars'),
           A('2026-04-30', 'Index', 'GPWB/TBSP periodic portfolio change', 'Communique (28 Apr): PS0731 joins TBSP; WS0429 moves into 1-3Y; WZ1126 leaves BWZ.' if ge(R, '29') else 'Maturity-window changes (see Index section).', 'GPW Benchmark' + (', 28 Apr' if ge(R, '29') else ' rules')),
           A('2026-04-30', 'Data', 'GUS April flash CPI', 'Expected ~3.0% (PAP, 29 Apr).' if ge(R, '30') else '', 'GUS calendar'),
           A('2026-05-08', 'Rating', 'S&P review of Poland (A-, stable)', '', 'Millennium, 23 Mar')]
    if ge(R, '15') and not ge(R, '17'):
        ev.append(A('2026-04-16', 'Auction', 'BGK FPC tender (min PLN 0.5bn)', 'FPC0229, FPC0231, FPC0332, FPC0235.', 'BGK, 14 Apr'))
    if ge(R, '28'):
        ev.append(A('2026-04-29', 'Auction', 'BGK FPC tender (min PLN 0.5bn)', 'FPC0229, FPC0231, FPC0332, FPC0235.', 'BGK, 27 Apr'))
    if held:
        ev.append(A('2026-05-06', 'MPC', 'MPC decision (5-6 May)', 'Hold expected.', 'NBP schedule'))
    ev = sorted(ev, key=lambda e: (e['date'], e['type']))
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core: central banks, CPI
    cp = copy.deepcopy(F0['core_policy'])
    cp['Poland'].update(pricing=f"FRAs ~{abs(x)}bp of {'cuts' if x > 0 else 'hikes'} within 12M ({L} close)" if abs(x) >= 5 else f"FRAs: no net move within 12M ({L} close)")
    if held:
        cp['Poland'].update(last="held 9 Apr 2026 (cut -25bp 4 Mar)", next="5-6 May 2026", stance="Wait-and-see; hikes only in a 'black scenario'", tone="wait")
    else:
        cp['Poland'].update(next="8-9 Apr 2026")
    cp['Euro area'].update(next="29-30 Apr 2026", stance="On hold; hikes priced", tone="wait", pricing=EZ[d])
    cp['United States'].update(pricing=US[d], next="28-29 Apr 2026")
    if ge(R, '30'):
        cp['United States'].update(last="held 29 Apr (8-4)", next="Jun 2026", stance="On hold; easing bias contested", tone="wait")
    cp['United Kingdom'].update(next="30 Apr 2026", stance="On hold; hikes priced", tone="wait", pricing=UK[d])
    cp['Czechia'].update(pricing="CZ March CPI 1.9% (7 Apr flash); no pricing found" if ge(R, '08') else "no pricing found")
    cp['Hungary'].update(pricing=("Tisza two-thirds win (12 Apr): HU10Y ~6.2-6.3%, BUBOR falling to the base rate" if ge(R, '14') else "MNB minutes: the February cut did not start a cycle (11 Mar)"),
                         next="28 Apr 2026")
    if ge(R, '29'):
        cp['Hungary'].update(last="held 28 Apr (6.25%)", next="May 2026")
    cp['Romania'].update(last="held 7 Apr (6.50%)" if ge(R, '08') else "held at 6.50% (next 7 Apr)", next="May 2026" if ge(R, '08') else "7 Apr 2026", pricing="not found")
    cc = copy.deepcopy(F0['core_cpi'])
    cc['Poland'] = dict(v=3.0, m="Mar" + ("" if ge(R, '16') else " flash"))
    cc['Euro area'] = dict(v=2.6, m="Mar (core 2.3)") if ge(R, '17') else dict(v=2.5, m="Mar flash (core 2.3)")
    cc['United States'] = dict(v=3.3, m="Mar (core 2.6)") if ge(R, '13') else dict(v=2.4, m="Feb (core 2.5)")
    cc['United Kingdom'] = dict(v=3.3, m="Mar (core 3.1)") if ge(R, '23') else dict(v=3.0, m="Feb (core 3.2)")
    cc['Czechia'] = dict(v=1.9, m="Mar") if ge(R, '08') else dict(v=1.4, m="Feb")
    cc['Hungary'] = dict(v=1.8, m="Mar (core 1.9)") if ge(R, '09') else dict(v=1.4, m="Feb")
    cc['Romania'] = dict(v=9.9, m="Mar") if ge(R, '15') else dict(v=9.3, m="Feb")
    note = (F0['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off (GUS, Eurostat, BLS, ONS, CZSO, KSH, INS; FOMC 18 Mar"
            + (" and 29 Apr" if ge(R, '30') else "") + ", ECB/BoE/CNB 19 Mar, MNB 24 Mar" + (" and 28 Apr" if ge(R, '29') else "") + (", NBR 7 Apr" if ge(R, '08') else "") + ").")
    good = v.get('cds5y') and v.get('pl_bund_10y') and R not in ('2026-04-14', '2026-04-23')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {L} close)." if good else
           f" (Erste published no table for the {L} close, so CDS and the 10Y spread are not quoted.)")
    regime = latest({'01': "Regime: war shock - oil above $100 and core yields near multi-year highs; ",
                     '09': "Regime: ceasefire relief - oil off its highs and hike pricing cut back everywhere; ",
                     '14': "Regime: fragile truce with a US blockade of Iranian ports - oil swinging between $90 and $105; ",
                     '22': "Regime: the oil shock is back (Brent above $100, Bund near 2011 highs) with hawkish repricing abroad; "}, R)
    regime += (f"the NBP {'held at 3.75% on 9 Apr' if held else 'is at 3.75% after the March cut'} while FRAs price {pr}; the ECB and BoE are priced for hikes, the Fed is on hold"
               + (" (8-4 on 29 Apr)" if ge(R, '30') else "") + ", the CNB and MNB are on hold.")
    core_text = regime + spr + " " + GLOB[d]
    tk = list(Q0['takeaways_html'])
    tk[2] = latest({'01': "<b>Supply:</b> BGK's Q2 FPC calendar (31 Mar) has tenders on 16 and 29 Apr, 14 and 28 May and 18 Jun; on 26 Mar it sold only PLN 0.87bn (demand 1.06bn) plus 0.20bn.",
                    '15': "<b>Supply:</b> BGK offers FPC0229, FPC0231, FPC0332 and FPC0235 on 16 Apr (min PLN 0.5bn); next tender 29 Apr; on 26 Mar it sold only PLN 0.87bn.",
                    '17': "<b>Supply:</b> on 16 Apr BGK sold PLN 1.06bn of FPC bonds on 1.89bn demand plus 0.21bn - a first sign of rebuilding demand (PKO); next tender 29 Apr.",
                    '28': "<b>Supply:</b> BGK sold PLN 1.06bn on 16 Apr (demand 1.89bn); next FPC tender 29 Apr; the FWSZ 2026 bond plan was raised to PLN 76.6bn (27 Apr) - more quasi supply ahead.",
                    '30': "<b>Supply:</b> BGK sold only PLN 0.69bn on 29 Apr (demand 0.94bn) after 1.06bn on 16 Apr; the FWSZ 2026 bond plan was raised to PLN 76.6bn (27 Apr) - more quasi supply ahead."}, R)
    mof_asof = latest({'01': "25 Mar 2026 sale", '13': "10 Apr 2026 T-bill (bonds: 25 Mar sale)", '16': "15 Apr 2026 sale", '24': "23 Apr 2026 sale", '29': "28 Apr 2026 sale"}, R)
    au = {"MoF auctions & switch results": dict(as_of=mof_asof, published="auction days", source="MoF wholesale-bond database (rows whose same-day release PAP confirms); MoF/PAP communiques",
                                                note="April plan (31 Mar): three sales, no switch; USD 6bn issue 7 Apr." + (" New 10Y DS0436 first issued 23 Apr." if ge(R, '24') else "")),
          "Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)": dict(as_of="31 Mar 2026 change (holdings 26 Mar)", published="27 Mar 2026 (served PDF regenerated 30 Mar)", source="GPW Benchmark 'Portfele obligacji' communique",
                                                          note="PS1026 left TBSP (17 bonds); units match MoF settlements to the 25 Mar sale." + (" The 30 Apr communique (28 Apr: PS0731 joins TBSP) is quoted in text only." if ge(R, '29') else "")),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of=("9 Apr 2026 decision (hold)" if held else "4 Mar 2026 decision (-25bp)") + "; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1],
                                                             source="NBP/MPC; PAP/Bloomberg/press interviews (first dated mention)", note=""),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1]}", source="PKO, Erste, Millennium, ING, Pekao, Credit Agricole, DB, BPS, Citi, Goldman; PAP", note="Only commentary published by the info cut-off."),
          "CPI, core CPI, GDP, NBP projection": dict(as_of="Mar 2026 CPI " + ("final" if ge(R, '16') else "flash") + ("; core Mar" if ge(R, '17') else "; core Feb") + "; NBP March projection",
                                                     published="31 Mar (flash)" + (", 15 Apr (final)" if ge(R, '16') else "") + (", 16 Apr (core, Q4 GDP revision)" if ge(R, '17') else ""), source="GUS, NBP", note=""),
          "Ratings & 2026 review calendar": dict(as_of=f"to {WIN[R]}", published="agency releases", source="Fitch, Moody's, S&P; PAP", note="No action on Poland in April; S&P review 8 May."),
          "Central banks (ECB, Fed, BoE, CNB, MNB, BNR), peer CPI": dict(as_of=f"decisions and prints published by {WIN[R].split('-')[-1]}", published="release dates", source="ECB, Fed, BoE, CNB, MNB, NBR; Eurostat, BLS, ONS, CZSO, KSH, INS; pricing via CME FedWatch, PAP/LSEG, Trading Economics",
                                                                         note="Market pricing quoted with its own date.")}
    nfa = dict(input=f"New facts {WIN[R]} 2026", as_of=WIN[R], published=WIN[R],
               source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, Trading Economics, ECB/BoE/CNB/MNB/NBR, rating agencies, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    od = dict(policy={'nbp_reference': 3.75, 'nbp_deposit': 3.25, 'nbp_lombard': 4.25, 'last_change': "4 Mar 2026 (-25bp, eff. 5 Mar)" + ("; held 9 Apr" if held else ""),
                      'next_mpc': "2026-05-05/06" if held else "2026-04-08/09"},
              facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
              quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = ops_add(R)
    if adds:
        od['mof_ops_add'] = adds
    sn = {'2026-04-02': "T+2 = 7 Apr: no settlement on Good Friday (3 Apr, no BondSpot session) or Easter Monday (6 Apr)",
          '2026-04-07': "T+2 = 8 Apr (after the Easter break: no session 3 and 6 Apr)",
          '2026-04-30': "T+2 = 4 May: 1 May is a public holiday"}
    if R in sn:
        od['settlement_note'] = sn[R]
    OUT[R] = od
json.dump(OUT, open(SP / 'apr/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
