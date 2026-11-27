"""Per-day point-in-time narrative for the 4-29 May 2026 reports -> may/facts_days.json (merged into the day specs).
Every statement below sits in the window in which it was first published (research/facts_*.json, notes_*.md)."""
import copy, json, pathlib, sys
SP = pathlib.Path('/tmp/claude-0/-home-user-Polish-FixedIncome/24a3fc3c-8e3f-5cce-b7fb-dcdc0e9e199e/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from wk_may import WK_PL, AB, US, EZ, UK, GLOB, CZ  # noqa: E402
F0 = json.load(open(REPO / 'data/snapshots/2026-04-30/facts.json'))
Q0 = json.load(open(REPO / 'data/snapshots/2026-04-30/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_may_fix/fixings.json'))['by_date']
CV = {**json.load(open(SP / 'agent_may_curves1/curves.json')), **json.load(open(SP / 'agent_may_curves2/curves.json'))}
P1 = json.load(open(SP / 'agent_may_plfacts1/facts.json'))
P2 = json.load(open(SP / 'agent_may_plfacts2/facts.json'))
OPS = {o['date']: o for P in (P1, P2) for o in P['mof_ops'] if isinstance(o, dict) and o.get('lines')}
RS = ['04', '05', '06', '07', '08', '11', '12', '13', '14', '15', '18', '19', '20', '21', '22', '25', '26', '27', '28', '29']
DAYS = [f'2026-05-{d}' for d in RS]
CUTS = ['2026-04-30'] + [f'2026-05-{d}' for d in ['04', '05', '06', '07', '08', '11', '12', '13', '14', '15', '18', '19', '20', '21', '22', '25', '26', '27', '28']]
WINS = ['30 Apr-3 May', '4 May', '5 May', '6 May', '7 May', '8-10 May', '11 May', '12 May', '13 May', '14 May', '15-17 May', '18 May', '19 May', '20 May',
        '21 May', '22-24 May', '25 May', '26 May', '27 May', '28 May']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
ge = lambda R, d: R >= '2026-05-' + d
lab = lambda C: f"{int(C[8:])} {'Apr' if C[5:7] == '04' else 'May'}"
A = lambda dt_, ty, ti, no='', sd='': dict(date=dt_, type=ty, title=ti, note=no, source_date=sd)
WZ = ['WZ1126', 'WZ1127', 'WZ0528', 'WZ1128', 'WZ1129', 'WZ1131', 'WZ0533']


def latest(dct, R):
    k = max([kk for kk in dct if ge(R, kk)], default=None)
    return dct[k] if k else None


def ops_add(R):
    out = []
    for d, need in (('2026-05-13', '14'), ('2026-05-21', '22'), ('2026-05-27', '28')):
        if not ge(R, need):
            continue
        o = OPS[d]
        out.append(dict(date=d, settle=o['settlement'], type='S', op='AS',
                        lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]))
        add = [dict(series=s, sold=q, demand=None, avg_yld=None, price=None) for s, q in o['additional_sale']['lines'].items() if q]
        if add:
            out.append(dict(date=d, settle=o['additional_sale']['settlement'], type='S', op='OB', lines=add))
    return out


def sale_txt(d):
    o = OPS[d]; ls = {l['series']: l for l in o['lines']}
    ys = ", ".join(f"{s} {ls[s]['avg_yield']:.3f}%" for s in ('OK0129', 'PS0731', 'DS0436', 'PS0130', 'DS1034', 'DS1033') if s in ls and ls[s].get('avg_yield') and ls[s].get('sold_mn'))
    return (f" {int(d[8:])} May sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn demand (cover {o['total_demand_mn']/o['total_sold_mn']:.2f})"
            f" plus {o['additional_sale']['total_mn']/1000:.2f}bn; {ys}.")


OUT = {}
for R in DAYS:
    d = R[8:]; C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; L = lab(C)
    x = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    pr = f"roughly {abs(x)}bp of NBP {'cuts' if x > 0 else 'hikes'}" if abs(x) >= 5 else "no net NBP move"
    fra_s = f"FRAs at the {L} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price {pr} within 12 months."
    held = ge(R, '07')
    # ---------------- policy
    V = [("The MPC held at 3.75% on 6 May (core probably rose in April; wait-and-see)" if held else "The MPC held at 3.75% on 9 Apr; the 5-6 May meeting is expected to hold")
         + ("; Glapiński (7 May): the probability of a hike has risen and a cut is very unlikely - a CPI breach of 3.5% with persistent forecasts would trigger action." if ge(R, '08') else ".")]
    V.append(latest({'04': "Dąbrowski (30 Apr): the chance of cuts fell sharply after the April CPI.",
                     '11': "April minutes (8 May): the war lifts CPI near term but weaker activity may curb medium-term pressure; Kotecki: forecasts keep CPI within target.",
                     '13': "Zarzecki (12 May): no change through 2026 is the base case, hikes need current and projected CPI above 3.5%; Wnorowski: no need to hike now.",
                     '14': "Litwiniuk (13 May): a hike more likely than a cut by end-2026, but no move in July; Kotecki: forget cuts until mid-2027.",
                     '15': "Wnorowski (14 May): on hold at least until July, CPI above 3.5% would not trigger an automatic hike; Litwiniuk (13 May): a hike more likely than a cut.",
                     '19': "Glapiński (18 May): no commitments, CPI within the band; Litwiniuk and Kotecki (13 May): hikes more likely than cuts, not in July.",
                     '21': "Tyrowicz (20 May): 3.75% is too low; Glapiński (18 May): no commitments.",
                     '25': "The April voting record (22 May) shows Tyrowicz's 100bp hike motion rejected with all others against; Glapiński (18 May): no commitments."}, R))
    V.append(("April CPI 3.2% (final, 15 May; flash 30 Apr, 3.0% expected)" if ge(R, '18') else "April flash CPI 3.2% (30 Apr; 3.0% expected)")
             + ("; core 3.0% (18 May)." if ge(R, '19') else "; core 2.7% in March.") + (" May flash CPI is due 29 May (Erste ~3.7%)." if ge(R, '26') else ""))
    V.append(latest({'04': "The fuel VAT and excise cuts run to 15 May.", '14': "The fuel VAT and excise cuts were extended to 31 May (13 May).",
                     '29': "The fuel VAT and excise cuts were extended to 15 June (28 May)."}, R))
    pricing = fra_s + " " + " ".join(V)
    risk = latest({'04': "Hawkish drift: April CPI 3.2% with core rising, FRAs price ~70bp of hikes while the MPC talks hold, and May supply is heavy (PLN 19-37bn) with Brent above $100; a US-Iran deal is the relief valve.",
                   '07': "The hold anchors the front end at WIBOR while FRAs swing with Iran headlines (75bp priced within 10 months before the decision); long end: heavy May supply and a 6.5-6.8% deficit; a deal would unwind hike pricing.",
                   '08': "Glapiński (7 May) moved to hike risk: a CPI breach of 3.5% with persistent forecasts would trigger action - May CPI (29 May) and the July projection are the tests. The front end trades oil and the Iran talks; long end: heavy May supply.",
                   '18': "Global bond rout (UST 10Y ~4.6-4.7%, Bund ~3.2%, gilts ~5.2%) and hike pricing up to ~100bp, while the MPC says hold until July and April activity disappoints (GDP 3.4%, wages, retail) - the long end follows core markets.",
                   '26': "Deal hopes pulled Brent below $100 and trimmed hike pricing; the risks are a collapse of the US-Iran memorandum (US strikes on 26 May) and May CPI (29 May, ~3.7% expected) above 3.5%; long end: June supply and the deficit."}, R)
    policy = dict(nbp_reference=3.75, next_mpc_label=("MPC next: 1-2 Jun" if held else "MPC next: 5-6 May"), pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = dict(v=3.2, m=("Apr (GUS final, 15 May; 0.6% m/m)" if ge(R, '18') else "Apr flash (GUS, 30 Apr; 3.0% expected)") + ("; core 3.0%" if ge(R, '19') else "; core 2.7% (Mar)"))
    proj = ("NBP March projection (4 Mar; data to 19 Feb, war excluded): CPI 50% bands 1.6-2.9% (2026), 1.1-3.7% (2027); central path 2.3% / 2.4% / 2.3% (2026-28), GDP 3.9% in 2026"
            "; IMF (14 Apr): 2026 CPI 3.3%" + ("; EC (21 May): GDP 3.5% in 2026" if ge(R, '22') else "") + ". The July projection is the next marker.")
    fiscal = ("2025 general-government deficit 7.3% of GDP (GUS EDP, 22 Apr), debt 59.7%; 2026 deficit cap PLN 271.7bn"
              + ("; budget deficit after April PLN 89.3bn (30.1% of the limit)" if ge(R, '18') else "; budget deficit after March PLN 69.6bn (25.6% of the limit)")
              + "; the fiscal notification and the government's assumptions put the 2026 deficit at ~6.8% of GDP" + ("; EC (21 May): 6.5%, debt 64.5%" if ge(R, '22') else "")
              + ("; the SAFE loan was signed on 8 May" if ge(R, '11') else "") + ("; windfall-tax bill due in Q2 (75% of margins above the 2025 level +20%)" if ge(R, '20') else "")
              + "; fuel package (VAT 8%, minimum excise, price caps) " + latest({'04': "to 15 May", '14': "extended to 31 May (13 May)", '29': "extended to 15 June (28 May)"}, R) + ".")
    fin = latest({'04': "~49% (after 28 Apr, MoF)", '15': "~51% (after 13 May, Millennium)", '26': "~54% (MoF, 25 May)"}, R)
    rat = latest({'04': "S&P reviews Poland on 8 May (A-, stable; Erste sees a sizeable risk of a negative outlook); Fitch A- and Moody's A2 have negative outlooks.",
                  '11': "S&P affirmed A-/stable (8 May); Fitch A- and Moody's A2 have negative outlooks.",
                  '12': "S&P affirmed A-/stable (8 May), DBRS A with a negative trend; Fitch A- and Moody's A2 have negative outlooks.",
                  '18': "S&P affirmed A-/stable (8 May); Scope moved its A outlook to negative (15 May); Fitch A- and Moody's A2 have negative outlooks.",
                  '27': "S&P affirmed A-/stable (8 May) and its analyst calls the missing medium-term consolidation the key rating risk (26 May); Scope A negative (15 May); Fitch and Moody's negative outlooks."}, R)
    frisk = (f"2026 needs {fin} financed" + "; budget accounts ~PLN 184bn at end-April (MoF estimate)"
             + ("; 8 May T-bill PLN 3.66bn at 4.151%" if ge(R, '12') else "") + ("; CHF 885m priced on 21 May (first CHF deal since 2015)" if ge(R, '22') else "") + ". " + rat)
    base = (("The NBP held at 3.75% on 6 May" if held else "The NBP has held at 3.75% since the 4 Mar cut (next MPC 5-6 May)") + "; April CPI 3.2% y/y"
            + ("; Q1 GDP 3.4% y/y (flash)." if ge(R, '15') else "; 2025 GDP 3.6%, Q4 4.1%.") + " Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable" + (" (affirmed 8 May)." if ge(R, '11') else "."))
    macro = dict(cpi=cpi, projection_text=proj, fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + WK_PL[d] + " Abroad: " + AB[d])
    # ---------------- calendar
    plan = ("MoF May plan (30 Apr): sale auctions on 13 May (PLN 6-12bn), 21 May (7-13bn) and 27 May (6-12bn) in OK0129 (new 2Y, replaces OK0128), NZ0331, PS0731, DS0436 and NZ0936; "
            "a 46-week T-bill on 8 May (3-6bn); no switch. ~49% of 2026 needs financed after the April sales.")
    if ge(R, '12'):
        plan += " 8 May T-bill: PLN 3.66bn at 4.151% plus 0.55bn."
    if R in ('2026-05-13', '2026-05-14'):
        plan += " 13 May offer (12 May): PLN 6-11bn, PS0130 added."
    if ge(R, '14'):
        plan += sale_txt('2026-05-13')
    if R in ('2026-05-20', '2026-05-21', '2026-05-22'):
        plan += " 21 May offer (19 May): PLN 6-10bn, cut from 7-13bn in the plan (DS1034 added)."
    if ge(R, '22'):
        plan += sale_txt('2026-05-21') + " CHF 885m priced (3Y/7Y/10Y green)."
    if R in ('2026-05-26', '2026-05-27', '2026-05-28'):
        plan += " 27 May offer (25 May): PLN 7-11bn (DS1033 added)."
    if ge(R, '28'):
        plan += sale_txt('2026-05-27')
    if ge(R, '15'):
        plan += " BGK FPC (14 May): PLN 0.84bn on 1.10bn demand plus 0.15bn."
    if ge(R, '29'):
        plan += " BGK FPC (28 May): PLN 0.94bn on 1.62bn plus 0.05bn. The June plan is due 29 May."
    left = [s for s, need in (('13 May', '13'), ('21 May', '21'), ('27 May', '27')) if not ge(R, need) or R == f'2026-05-{need}']
    timing = ("The Aug 2025-Feb 2026 pattern (auction-day close the cheapest point of the week) comes from a rally regime; March's sell-off broke it and April's auction days cheapened on average. "
              + (f"Remaining May sales: {', '.join(left)}. " if left else "May supply is done (PLN 31.1bn sold plus 1.03bn additional); the June plan is due 29 May. "))
    timing += ("MPC 5-6 May: a hold is expected." if not held else "Next MPC 1-2 Jun: a hold is expected; the July projection is the next marker.")
    if ge(R, '14'):
        timing += " Covers: 1.25 (13 May)" + (", 1.33 (21 May)" if ge(R, '22') else "") + (", 1.25 (27 May)" if ge(R, '28') else "") + " vs 1.13-1.25 in April."
    ev = []
    if not held:
        ev.append(A('2026-05-06', 'MPC', 'MPC decision (5-6 May)', 'Hold expected.', 'NBP schedule'))
    ev += [A('2026-05-07', 'MPC', 'Glapiński press conference', '', 'NBP'),
           A('2026-05-08', 'Auction', 'MoF 46-week T-bill (PLN 3-6bn)', '', 'MoF May plan, 30 Apr'),
           A('2026-05-08', 'Rating', 'S&P and DBRS reviews of Poland', 'After 22:00.', 'PAP week-ahead, 4 May' if ge(R, '05') else 'Millennium, 23 Mar'),
           A('2026-05-12', 'Data', 'US April CPI', '', 'BLS calendar'),
           A('2026-05-13', 'Auction', 'MoF sale auction PLN ' + ('6-11bn' if ge(R, '13') else '6-12bn'), 'OK0129 (new 2Y), PS0130, NZ0331, PS0731, DS0436, NZ0936.' if ge(R, '13') else 'New 2Y OK0129.', 'MoF offer, 12 May' if ge(R, '13') else 'MoF May plan, 30 Apr'),
           A('2026-05-14', 'Data', 'GUS Q1 GDP flash', '', 'GUS calendar'),
           A('2026-05-15', 'Data', 'GUS final April CPI; NBP March current account', '', 'GUS/NBP calendars'),
           A('2026-05-18', 'Data', 'NBP core inflation (April)', '', 'NBP calendar'),
           A('2026-05-21', 'Data', 'GUS April wages, industry, PPI, construction', '', 'GUS calendar'),
           A('2026-05-21', 'Auction', 'MoF sale auction PLN ' + ('6-10bn' if ge(R, '20') else '7-13bn'), 'Offer cut from 7-13bn; DS1034 added.' if ge(R, '20') else '', 'MoF offer, 19 May' if ge(R, '20') else 'MoF May plan, 30 Apr'),
           A('2026-05-25', 'Data', 'GUS April retail sales; NBP M3', '', 'GUS/NBP calendars'),
           A('2026-05-25', 'Cash flow', 'WZ coupon reset (WZ1126-WZ0533, May/Nov lines)', 'New coupon 3.96% (MoF, 20 May).' if ge(R, '21') else 'Set from WIBOR 6M fixings before the MoF notice.', 'bond terms'),
           A('2026-05-26', 'CB', 'MNB decision', '', 'MNB calendar'),
           A('2026-05-27', 'Auction', 'MoF sale auction PLN ' + ('7-11bn' if ge(R, '26') else '6-12bn'), 'DS1033 added.' if ge(R, '26') else '', 'MoF offer, 25 May' if ge(R, '26') else 'MoF May plan, 30 Apr'),
           A('2026-05-29', 'Index', 'GPWB/TBSP periodic portfolio change', 'Communique (27 May): DS0436 joins TBSP (19 bonds); PS0527 leaves 1-3Y/1-4Y; NZ0331/NZ0928 join BWZ.' if ge(R, '28') else 'Maturity-window changes (see Index section).', 'GPW Benchmark' + (', 27 May' if ge(R, '28') else ' rules')),
           A('2026-05-29', 'Data', 'GUS May flash CPI', 'Erste ~3.7% (25 May).' if ge(R, '26') else '', 'GUS calendar'),
           A('2026-06-11', 'CB', 'ECB decision', 'June hike priced.' if ge(R, '15') else '', 'ECB calendar'),
           A('2026-06-17', 'CB', 'FOMC decision (16-17 Jun)', '', 'Fed calendar')]
    if R in ('2026-05-13', '2026-05-14'):
        ev.append(A('2026-05-14', 'Auction', 'BGK FPC tender (min PLN 0.5bn)', 'FPC0229, FPC0231, FPC0332, FPC0235.', 'BGK, 12 May'))
    if R in ('2026-05-27', '2026-05-28'):
        ev.append(A('2026-05-28', 'Auction', 'BGK FPC tender (min PLN 0.5bn)', '', 'BGK, 26 May'))
    if held:
        ev.append(A('2026-06-02', 'MPC', 'MPC decision (1-2 Jun)', 'Hold expected.', 'NBP, 6 May'))
    ev = sorted(ev, key=lambda e: (e['date'], e['type']))
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core: central banks, CPI
    cp = copy.deepcopy(F0['core_policy'])
    cp['Poland'].update(pricing=f"FRAs ~{abs(x)}bp of {'cuts' if x > 0 else 'hikes'} within 12M ({L} close)" if abs(x) >= 5 else f"FRAs: no net move within 12M ({L} close)")
    if held:
        cp['Poland'].update(last="held 6 May 2026 (3.75%)", next="1-2 Jun 2026",
                            stance="On hold; hike risk up (Glapiński, 7 May)" if ge(R, '08') else "Wait-and-see", tone="wait")
    else:
        cp['Poland'].update(last="held 9 Apr 2026 (cut -25bp 4 Mar)", next="5-6 May 2026")
    cp['Euro area'].update(last="held 30 Apr (2.00%, unanimous)", next="11 Jun 2026", stance="On hold; June hike priced", tone="wait", pricing=EZ[d])
    cp['United States'].update(last="held 29 Apr (8-4)", next="16-17 Jun 2026", stance=("On hold; Warsh chair from 22 May" if ge(R, '25') else "On hold; easing bias contested"), tone="wait", pricing=US[d])
    cp['United Kingdom'].update(last="held 30 Apr (8-1, one vote for +25bp)", next="Jun 2026", stance="On hold; hikes priced", tone="wait", pricing=UK[d])
    cp['Czechia'].update(last="held 7 May (3.50%)" if ge(R, '08') else "held 19 Mar (3.50%)", next="Jun 2026" if ge(R, '08') else "7 May 2026", pricing="no pricing found")
    cp['Hungary'].update(last="held 26 May (6.25%); sees room to ease" if ge(R, '27') else "held 28 Apr (6.25%)", next="Jun 2026" if ge(R, '27') else "26 May 2026",
                         pricing="Tisza government; HU10Y ~6%, BUBOR at the base rate")
    cp['Romania'].update(last="held 15 May (6.50%)" if ge(R, '18') else "held 7 Apr (6.50%)", next="not found" if ge(R, '18') else "15 May 2026", pricing="not found")
    cc = copy.deepcopy(F0['core_cpi'])
    cc['Poland'] = dict(v=3.2, m="Apr" + ("" if ge(R, '18') else " flash"))
    cc['Euro area'] = dict(v=3.0, m="Apr (core 2.2)" if ge(R, '21') else "Apr flash (core 2.2)")
    cc['United States'] = dict(v=3.8, m="Apr (core 2.8)") if ge(R, '13') else dict(v=3.3, m="Mar (core 2.6)")
    cc['United Kingdom'] = dict(v=2.8, m="Apr (core 2.5)") if ge(R, '21') else dict(v=3.3, m="Mar (core 3.1)")
    cc['Czechia'] = latest(CZ, R)
    cc['Hungary'] = dict(v=2.1, m="Apr") if ge(R, '11') else dict(v=1.8, m="Mar (core 1.9)")
    cc['Romania'] = dict(v=10.7, m="Apr") if ge(R, '14') else dict(v=9.9, m="Mar")
    note = (F0['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off (GUS, Eurostat, BLS, ONS, CZSO, KSH, INS; FOMC 29 Apr, ECB/BoE 30 Apr"
            + (", CNB 7 May" if ge(R, '08') else "") + (", NBR 15 May" if ge(R, '18') else "") + (", MNB 26 May" if ge(R, '27') else ", MNB 28 Apr") + ").")
    good = v.get('cds5y') and v.get('pl_bund_10y')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {L} close"
           + ("; Erste switched its 10Y from DS1035 to DS0436 at the 18 May print" if R in ('2026-05-19', '2026-05-20') else "") + ")." if good else "")
    regime = latest({'04': "Regime: oil shock with a stalled US-Iran truce (Brent above $100, Bund near 2011 highs) and hawkish repricing abroad; ",
                     '07': "Regime: deal hopes versus stalemate - oil swinging around $100-110; ",
                     '18': "Regime: global bond rout (UST 10Y ~4.7%, Bund ~3.2%, gilts ~5.2%) as hike pricing spreads; ",
                     '21': "Regime: talks in a 'final stage' - oil off its highs, core yields retreating; ",
                     '26': "Regime: a 60-day US-Iran memorandum within reach - Brent below $100, Bund back under 3%; "}, R)
    regime += (f"the NBP {'held at 3.75% on 6 May' if held else 'is at 3.75%'} while FRAs price {pr}; the ECB is priced for a June hike, the BoE for hikes, the Fed has turned to hike risk"
               + (" under Warsh" if ge(R, '25') else "") + ", the CNB and MNB are on hold.")
    core_text = regime + spr + " " + GLOB[d]
    tk = list(Q0['takeaways_html'])
    tk[2] = latest({'04': "<b>Supply:</b> BGK sold PLN 0.69bn on 29 Apr plus 0.13bn additional (demand 0.94bn); next FPC tenders 14 and 28 May; the FWSZ 2026 bond plan was raised to PLN 76.6bn.",
                    '13': "<b>Supply:</b> BGK offers FPC0229, FPC0231, FPC0332 and FPC0235 on 14 May (min PLN 0.5bn); next tender 28 May; the FWSZ 2026 bond plan is PLN 76.6bn.",
                    '15': "<b>Supply:</b> BGK sold PLN 0.84bn on 14 May (demand 1.10bn) plus 0.15bn; next FPC tender 28 May.",
                    '20': "<b>Supply:</b> BGK sold PLN 0.84bn on 14 May plus 0.15bn; it filed a EUR 35bn MTN prospectus (19 May); next FPC tender 28 May.",
                    '26': "<b>Supply:</b> BGK plans FPC switch tenders from June and a POLSTR floater in Q3 (25 May); FPC tender on 28 May.",
                    '29': "<b>Supply:</b> BGK sold PLN 0.94bn on 28 May (demand 1.62bn) plus 0.05bn; FPC switches from June and a POLSTR-based FPC floater in Q3."}, R)
    mof_asof = latest({'04': "28 Apr 2026 sale", '12': "8 May 2026 T-bill (bonds: 28 Apr sale)", '14': "13 May 2026 sale", '22': "21 May 2026 sale", '28': "27 May 2026 sale"}, R)
    au = {"MoF auctions & switch results": dict(as_of=mof_asof, published="auction days", source="MoF wholesale-bond database (rows whose same-day release PAP confirms); MoF/PAP communiques",
                                                note="May plan (30 Apr): three sales, no switch." + (" New 2Y OK0129 first issued 13 May." if ge(R, '14') else "") + (" CHF 885m on 21 May." if ge(R, '22') else "")),
          "Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)": dict(as_of="30 Apr 2026 change (holdings 27 Apr)", published="28 Apr 2026", source="GPW Benchmark 'Portfele obligacji' communique",
                                                          note="PS0731 joined TBSP (18 bonds), WS0429 moved into 1-3Y; units match MoF settlements to 27 Apr." + (" The 29 May communique (27 May: DS0436 joins TBSP) is quoted in text only." if ge(R, '28') else "")),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of=("6 May 2026 decision (hold)" if held else "9 Apr 2026 decision (hold)") + "; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1],
                                                             source="NBP/MPC; PAP/Bloomberg/press interviews (first dated mention)", note="June meeting moved to 1-2 June (6 May)." if held else ""),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1]}", source="PKO, Erste, Millennium, ING, Pekao, DB, BNP, XTB, mBank; PAP", note="Only commentary published by the info cut-off."),
          "CPI, core CPI, GDP, NBP projection": dict(as_of="Apr 2026 CPI " + ("final" if ge(R, '18') else "flash") + ("; core Apr" if ge(R, '19') else "; core Mar") + ("; Q1 GDP flash" if ge(R, '15') else "") + "; NBP March projection",
                                                     published="30 Apr (flash)" + (", 14 May (GDP)" if ge(R, '15') else "") + (", 15 May (final)" if ge(R, '18') else "") + (", 18 May (core)" if ge(R, '19') else ""), source="GUS, NBP", note=""),
          "Ratings & 2026 review calendar": dict(as_of=f"to {WIN[R]}", published="agency releases", source="S&P, DBRS, Scope, Fitch, Moody's; PAP", note=rat),
          "Central banks (ECB, Fed, BoE, CNB, MNB, BNR), peer CPI": dict(as_of=f"decisions and prints published by {WIN[R].split('-')[-1]}", published="release dates", source="ECB, Fed, BoE, CNB, MNB, NBR; Eurostat, BLS, ONS, CZSO, KSH, INS; pricing via CME FedWatch, PAP/LSEG, Trading Economics",
                                                                         note="Market pricing quoted with its own date.")}
    if ge(R, '21'):
        au["WZ coupons"] = dict(as_of="periods from 25 May 2026 (WZ1126-WZ0533: 3.96%); WZ0330/WZ0930 3.86% from 25 Mar", published="20 May 2026 (PDF 11:23)", source="MoF rate notice (WIBOR 6M 18-20 May: 3.97/3.96/3.96)",
                                note="Applied in the floater engine from the 25 May close." if ge(R, '26') else "Applied from the 25 May close.")
    nfa = dict(input=f"New facts {WIN[R]} 2026", as_of=WIN[R], published=WIN[R],
               source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, Trading Economics, ECB/BoE/CNB/MNB/NBR, rating agencies, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    od = dict(policy={'nbp_reference': 3.75, 'nbp_deposit': 3.25, 'nbp_lombard': 4.25, 'last_change': "4 Mar 2026 (-25bp, eff. 5 Mar); held 9 Apr" + (" and 6 May" if held else ""),
                      'next_mpc': "2026-06-01/02" if held else "2026-05-05/06"},
              facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
              quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = ops_add(R)
    if adds:
        od['mof_ops_add'] = adds
    if ge(R, '26'):
        od['floaters_update'] = {t: {'coupon': 3.96, 'period_start': '2026-05-25'} for t in WZ}
    sn = {'2026-05-04': "T+2 = 5 May (1 May holiday and the weekend)", '2026-05-29': "T+2 = 1 Jun"}
    if R in sn:
        od['settlement_note'] = sn[R]
    OUT[R] = od
json.dump(OUT, open(SP / 'may/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
