"""Per-day point-in-time narrative for the 1-30 Jun 2026 reports -> jun/facts_days.json (merged into the day specs).
Every statement below sits in the window in which it was first published (research/facts_*.json, notes_*.md).
Strict placement: MoF offers and additional sales only from their first dated mention; the 3 Jun switch result is the MoF
database row (no dated in-window report; the usual same-day MoF release is assumed, so it enters the 5 Jun report)."""
import copy, json, pathlib, sys
SP = pathlib.Path('/tmp/claude-0/-home-user-Polish-FixedIncome/f82df0b1-d4bb-529b-9fb4-ff4ddefccef7/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from wk_jun import WK_PL, AB, US, EZ, UK, GLOB, CZ  # noqa: E402
F0 = json.load(open(REPO / 'data/snapshots/2026-05-29/facts.json'))
Q0 = json.load(open(REPO / 'data/snapshots/2026-05-29/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_jun_fix/fixings.json'))['by_date']
CV = {**json.load(open(SP / 'agent_jun_curves1/curves.json')), **json.load(open(SP / 'agent_jun_curves2/curves.json'))}
P1 = json.load(open(SP / 'agent_jun_plfacts1/facts.json'))
P2 = json.load(open(SP / 'agent_jun_plfacts2/facts.json'))
OPS = {o['date']: o for P in (P1, P2) for o in P['mof_ops'] if isinstance(o, dict) and o.get('lines')}
RS = ['01', '02', '03', '05', '08', '09', '10', '11', '12', '15', '16', '17', '18', '19', '22', '23', '24', '25', '26', '29', '30']
DAYS = [f'2026-06-{d}' for d in RS]
CUTS = ['2026-05-29'] + [f'2026-06-{d}' for d in ['01', '02', '03', '05', '08', '09', '10', '11', '12', '15', '16', '17', '18', '19', '22', '23', '24', '25', '26', '29']]
WINS = ['29-31 May', '1 Jun', '2 Jun', '3-4 Jun', '5-7 Jun', '8 Jun', '9 Jun', '10 Jun', '11 Jun', '12-14 Jun', '15 Jun', '16 Jun', '17 Jun', '18 Jun',
        '19-21 Jun', '22 Jun', '23 Jun', '24 Jun', '25 Jun', '26-28 Jun', '29 Jun']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
ge = lambda R, d: R >= '2026-06-' + d
lab = lambda C: f"{int(C[8:])} {'May' if C[5:7] == '05' else 'Jun'}"
A = lambda dt_, ty, ti, no='', sd='': dict(date=dt_, type=ty, title=ti, note=no, source_date=sd)


def latest(dct, R):
    k = max([kk for kk in dct if ge(R, kk)], default=None)
    return dct[k] if k else None


def ops_add(R):
    out = []
    if ge(R, '05'):  # 3 Jun switch (settles 8 Jun after Corpus Christi)
        o = OPS['2026-06-03']
        out.append(dict(date='2026-06-03', settle=o['settlement'], type='S', op='AZ',
                        lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]))
        out.append(dict(date='2026-06-03', settle=o['settlement'], type='O', op='AZ',
                        lines=[dict(series=l['series'], sold=-l['bought_back_mn'], demand=None, avg_yld=None, price=None) for l in o['lines_bought_back'] if l.get('bought_back_mn')]))
    for d, need, need_add in (('2026-06-17', '18', '19'), ('2026-06-24', '25', '25')):
        if not ge(R, need):
            continue
        o = OPS[d]
        out.append(dict(date=d, settle=o['settlement'], type='S', op='AS',
                        lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]))
        add = [dict(series=s, sold=q, demand=None, avg_yld=None, price=None) for s, q in o['additional_sale']['lines'].items() if q]
        if add and ge(R, need_add):
            out.append(dict(date=d, settle=o['additional_sale']['settlement'], type='S', op='OB', lines=add))
    return out


def sale_txt(d, with_add=True):
    o = OPS[d]; ls = {l['series']: l for l in o['lines']}
    ys = ", ".join(f"{s} {ls[s]['avg_yield']:.3f}%" for s in ('OK0129', 'PS0731', 'DS1030', 'DS1035', 'DS0436') if s in ls and ls[s].get('avg_yield') and ls[s].get('sold_mn'))
    return (f" {int(d[8:])} Jun sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn demand (cover {o['total_demand_mn']/o['total_sold_mn']:.2f})"
            + (f" plus {o['additional_sale']['total_mn']/1000:.2f}bn" if with_add else "") + f"; {ys}.")


SW = OPS['2026-06-03']
SW_TXT = (f" 3 Jun switch (MoF database): PLN {SW['total_sold_mn']/1000:.2f}bn sold (demand {SW['total_demand_mn']/1000:.2f}bn) vs {SW['total_bought_back_mn']/1000:.2f}bn bought back"
          f" (PS0527 7.42bn), net +{SW['net_new_supply_mn']/1000:.2f}bn; OK0129 4.812%, PS0731 5.269%, DS0436 5.703%.")

OUT = {}
for R in DAYS:
    d = R[8:]; C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; L = lab(C)
    x = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    pr = f"roughly {abs(x)}bp of NBP {'cuts' if x > 0 else 'hikes'}" if abs(x) >= 5 else "no net NBP move"
    fra_s = f"FRAs at the {L} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price {pr} within 12 months."
    held = ge(R, '03')
    # ---------------- policy
    V = [("The MPC held at 3.75% on 2 Jun (May CPI eased mainly on food; decisions stay data-dependent)" if held else "The MPC held at 3.75% on 6 May; the 1-2 Jun meeting is expected to hold")
         + ("; Glapiński (3 Jun): lower May CPI cuts the hike odds, rates are high enough and there is no reason to change or even discuss them." if ge(R, '05') else ".")]
    V.append(latest({'01': "Glapiński (18 May): no commitments; the April voting record (22 May) shows Tyrowicz's 100bp hike motion rejected.",
                     '02': "PAP survey (1 Jun): a hold at 3.75% until Q3 2027; Glapiński (18 May): no commitments.",
                     '05': "Goldman, Noble and Erste read the 3 Jun conference as dovish; PAP survey (1 Jun): a hold until Q3 2027.",
                     '08': "May minutes (5 Jun): the CPI outlook is highly uncertain even short term and hinges on fuel prices and the fuel measures; most members backed the hold.",
                     '10': "Masłowska (9 Jun): cuts are now more likely than hikes, conditional on CPI staying below 3.5% and no escalation.",
                     '11': "Dąbrowski (10 Jun): no reason to hike after the CPI fall, room even for cuts if the world calms; Masłowska (9 Jun): cuts more likely than hikes.",
                     '15': "Dąbrowski (12 Jun, Bloomberg): a cut is now more likely than a hike, most members are more optimistic on inflation.",
                     '16': "Kotecki (15 Jun): rate changes unlikely to end-2026, hike appetite lower, too early to signal cuts; Dąbrowski (12 Jun): a cut now more likely than a hike.",
                     '19': "Duda (18 Jun): stable rates the base case, little room for cuts; the May voting record (18 Jun) shows Tyrowicz's +100bp motion rejected again."}, R))
    V.append(("May CPI 3.1% (final, 15 Jun; flash 29 May, 3.7% expected)" if ge(R, '16') else "May flash CPI 3.1% (29 May; 3.7% expected, -0.3% m/m on food)")
             + ("; core 3.1% (16 Jun)." if ge(R, '17') else "; core 3.0% in April.") + (" June flash CPI is due 30 Jun (Goldman, Santander ~2.7%)." if ge(R, '30') else ""))
    V.append(latest({'01': "The fuel VAT and excise cuts run to 15 June (extended 28 May).",
                     '15': "The fuel VAT cut and price caps run to 30 June, but the excise cut ends on 15 June; Tusk: the fuel package ends in summer.",
                     '17': "Standard fuel excise is back from 15 Jun; VAT 8% and price caps run to 30 June, with a VAT decision due 'shortly' (Tusk, 16 Jun).",
                     '30': "VAT 8% and price caps run to 30 June; pump prices are seen rising from July as the package ends (e-petrol, 29 Jun)."}, R))
    pricing = fra_s + " " + " ".join(V)
    risk = latest({'01': "May flash CPI 3.1% (3.7% expected) cut hike pricing sharply; the risks are the US-Iran memorandum failing (oil back above $100) and the end of the fuel package lifting CPI; long end: June supply (switch 3 Jun, sales 17 and 24 Jun) and a 6.5-7% deficit.",
                   '05': "The MPC turned dovish (Glapiński, 3 Jun: no reason to change or even discuss rates), so FRAs trade oil and the Iran talks; risks: renewed Gulf fighting and the fuel package ending (excise from 15 Jun) lifting CPI; long end: the 17 and 24 Jun sales and the deficit.",
                   '12': "MPC members now call cuts more likely than hikes (Masłowska 9 Jun, Dąbrowski 10 Jun) while the ECB hiked on 11 Jun and the Fed is priced for a 2026 hike; risks: the Iran deal failing, the fuel package ending (excise 15 Jun, VAT after 30 Jun) and two PLN 6-12bn sales (17, 24 Jun).",
                   '16': "A preliminary US-Iran deal (14-15 Jun) pushed Brent towards $80 and POLGB yields to three-month lows; risks: the MoU unravelling, the Fed dots (17 Jun), the fuel-package exit (excise back 15 Jun, VAT after 30 Jun) and two PLN 6-12bn sales; the 6.5-7% deficit keeps ASW wide.",
                   '18': "Strong demand at the 17 Jun sale (cover 1.52) and a dovish MPC pulled the 10Y to ~5.40%; risks: the hawkish Fed dots lifted US 2Y yields, CPI may rise as fuel support is withdrawn (VAT after 30 Jun), and the US-Iran MoU is fragile; one more sale on 24 Jun.",
                   '26': "FRAs no longer price NBP hikes (PKO, 25 Jun) and Brent is back at pre-war levels (~$73); risks: a renewed Gulf flare-up, the end of the fuel package in July lifting CPI, the July MPC with its projection, and Q3 supply with a 6.5-7% deficit.",
                   '29': "US strikes on Iran (26-27 Jun), then a halt with Doha talks planned, show the MoU is fragile; FRAs price no NBP move; risks: oil, the fuel package ending in July, the July projection, and Q3 supply (plan due at end-June)."}, R)
    nxt = "MPC next: 7-8 Jul" if ge(R, '30') else ("MPC next: Jul (projection)" if held else "MPC next: 1-2 Jun")
    policy = dict(nbp_reference=3.75, next_mpc_label=nxt, pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = dict(v=3.1, m=("May (GUS final, 15 Jun; -0.3% m/m)" if ge(R, '16') else "May flash (GUS, 29 May; 3.7% expected)") + ("; core 3.1%" if ge(R, '17') else "; core 3.0% (Apr)"))
    proj = ("NBP March projection (4 Mar; data to 19 Feb, war excluded): CPI 50% bands 1.6-2.9% (2026), 1.1-3.7% (2027); central path 2.3% / 2.4% / 2.3% (2026-28), GDP 3.9% in 2026"
            "; IMF (14 Apr): 2026 CPI 3.3%; EC (21 May): GDP 3.5% in 2026" + ("; OECD (June outlook): CPI 3.7% in 2026, no cuts before Q2 2027" if ge(R, '05') else "")
            + ("; Fitch (8 Jun): GDP 3.3%, NBP flat at 3.75% to year-end" if ge(R, '09') else "") + ("; World Bank (11 Jun): GDP 3.1% / 2.6%" if ge(R, '12') else "")
            + ("; NBP survey of economists (24 Jun): CPI 3.0% / 2.9% (2026-27)" if ge(R, '25') else "") + ". The July projection is the next marker.")
    fiscal = ("2025 general-government deficit 7.3% of GDP (GUS EDP, 22 Apr), debt 59.7%; 2026 deficit cap PLN 271.7bn"
              + ("; budget deficit after May PLN 108.2bn (~40% of the limit, 15 Jun)" if ge(R, '16') else "; budget deficit after April PLN 89.3bn (30.1% of the limit)")
              + "; the government's assumptions put the 2026 deficit at ~6.8% of GDP; EC (21 May): 6.5%, debt 64.5%" + ("; EKF consensus (2 Jun): 6.9%" if ge(R, '03') else "")
              + ("; EDP debt 61.6% of GDP at end-Q1 (10 Jun)" if ge(R, '11') else "") + ("; 2027 budget path (9 Jun): GDP 3.1%, CPI 2.5%" if ge(R, '10') else "")
              + latest({'01': "; windfall-tax bill (75% of margins above the 2025 level +20%) in preparation", '12': "; windfall-tax draft cut to a 60% rate, PLN 3.8bn in 2026 (11 Jun)",
                        '17': "; the government adopted the windfall tax (16 Jun)", '22': "; the Sejm passed the windfall tax (60%, ~PLN 3.8bn in 2026)", '26': "; the Senate amended the windfall tax (25 Jun)"}, R)
              + "; fuel package (VAT 8%, price caps" + latest({'01': ", minimum excise) to 15 June (28 May)", '15': ") to 30 June, excise cut ends 15 June", '17': ") to 30 June, standard excise back from 15 June"}, R) + ".")
    fin = latest({'01': "~56% (MoF, 29 May)", '19': "~58-59% (after 17 Jun, banks)", '25': "~62% (MoF, 24 Jun)"}, R)
    acc = "budget accounts PLN 208.3bn at end-May (MoF, 8 Jun)" if ge(R, '09') else "budget accounts >PLN 200bn expected at end-May (Drop, 29 May)"
    rat = latest({'01': "S&P affirmed A-/stable (8 May) and its analyst calls the missing medium-term consolidation the key rating risk (26 May); Scope A negative (15 May); Fitch A- and Moody's A2 have negative outlooks.",
                  '09': "S&P A-/stable (affirmed 8 May); Scope A negative (15 May); Fitch A- and Moody's A2 have negative outlooks; Fitch's June forecast round (8 Jun) was not a rating action.",
                  '25': "S&P A-/stable (8 May); Scope A negative (15 May); Fitch A- negative - its CEO (23 Jun, reported 24 Jun) calls public finances the main rating risk; Moody's A2 negative."}, R)
    frisk = (f"2026 needs {fin} financed; {acc}" + (SW_TXT.replace(" 3 Jun switch", "; 3 Jun switch").rstrip('.') if ge(R, '05') else "")
             + ("; BGK priced EUR 2bn of FPC bonds (2 Jun)" if ge(R, '03') else "") + ". " + rat)
    base = (("The NBP held at 3.75% on 2 Jun" if held else "The NBP has held at 3.75% since the 4 Mar cut (next MPC 1-2 Jun)") + "; May CPI 3.1% y/y"
            + ("; Q1 GDP 3.5% y/y (second estimate)." if ge(R, '02') else "; Q1 GDP 3.4% y/y (flash).") + " Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable.")
    macro = dict(cpi=cpi, projection_text=proj, fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + WK_PL[d] + " Abroad: " + AB[d])
    # ---------------- calendar
    plan = ("MoF June plan (29 May): one switch on 3 Jun (settles 8 Jun; buys back DS0726, PS1026, WZ1126, OK0127, PS0527) and sale auctions on 17 and 24 Jun "
            "(PLN 6-12bn each) in OK0129, NZ0331, PS0731, DS0436 and NZ0936; no T-bills; ~56% of 2026 needs financed.")
    if R in ('2026-06-02', '2026-06-03'):
        plan += " 3 Jun switch offer (1 Jun): sells OK0129, NZ0331, PS0731, DS1034, DS0436 and NZ0936."
    if ge(R, '05'):
        plan += SW_TXT
    if ge(R, '18'):
        plan += sale_txt('2026-06-17', with_add=ge(R, '19'))
    if R == '2026-06-24':
        plan += " 24 Jun offer (first dated 23 Jun): PLN 7-12bn in OK0129, NZ0331, PS0731, DS1035, DS0436 and NZ0936."
    if ge(R, '25'):
        plan += sale_txt('2026-06-24')
    plan += latest({'01': " BGK: FPC switch on 18 Jun (buys back FPC0427).", '03': " BGK priced EUR 2bn of FPC bonds on 2 Jun; FPC switch on 18 Jun (buys back FPC0427).",
                    '19': " BGK switch (18 Jun): PLN 1.35bn of FPC sold (demand 2.11bn) vs 1.44bn of FPC0427 bought back."}, R)
    if ge(R, '30'):
        plan += " The Q3/July supply plans of the MoF and BGK are due 30 Jun."
    left = [s for s, need in (('3 Jun (switch)', '03'), ('17 Jun', '17'), ('24 Jun', '24')) if not ge(R, need) or R == f'2026-06-{need}']
    timing = ("The Aug 2025-Feb 2026 pattern (auction-day close the cheapest point of the week) comes from a rally regime; March's sell-off broke it and April's auction days cheapened on average. "
              + (f"Remaining June operations: {', '.join(left)}. " if left else "June supply is done (PLN 24.0bn sold in two sales plus 2.11bn additional, and the 3 Jun switch); the July/Q3 plan is due at end-June. "))
    timing += ("MPC 1-2 Jun: a hold is expected." if not held else ("Next MPC 7-8 Jul, with the NBP projection: a hold is expected." if ge(R, '30') else "Next MPC in July, with the NBP projection: a hold is expected."))
    if ge(R, '18'):
        timing += " Covers: 1.52 (17 Jun)" + (", 1.28 (24 Jun)" if ge(R, '25') else "") + " vs 1.25-1.33 in May."
    ev = []
    if not held:
        ev.append(A('2026-06-02', 'MPC', 'MPC decision (1-2 Jun)', 'Hold expected.', 'NBP, 6 May'))
    ev += [A('2026-06-01', 'Data', 'GUS Q1 GDP (second estimate); May manufacturing PMI', '', 'GUS/S&P calendars'),
           A('2026-06-03', 'Auction', 'MoF switch auction', ('Sells OK0129, NZ0331, PS0731, DS1034, DS0436, NZ0936; buys back DS0726, PS1026, WZ1126, OK0127, PS0527.' if ge(R, '02')
                                                            else 'Buys back DS0726, PS1026, WZ1126, OK0127, PS0527.'), 'MoF offer, 1 Jun' if ge(R, '02') else 'MoF June plan, 29 May'),
           A('2026-06-03', 'MPC', 'Glapiński press conference', '', 'NBP'),
           A('2026-06-05', 'Data', 'US May payrolls', '', 'BLS calendar'),
           A('2026-06-10', 'Data', 'US May CPI', '', 'BLS calendar'),
           A('2026-06-11', 'CB', 'ECB decision', 'June hike priced.', 'ECB calendar'),
           A('2026-06-12', 'Data', 'NBP April current account', '', 'NBP calendar'),
           A('2026-06-15', 'Data', 'GUS final May CPI', '', 'GUS calendar'),
           A('2026-06-16', 'Data', 'NBP core inflation (May)', '', 'NBP calendar'),
           A('2026-06-17', 'Auction', 'MoF sale auction PLN 6-12bn', 'OK0129, NZ0331, PS0731, DS0436, NZ0936 (plan).', 'MoF June plan, 29 May'),
           A('2026-06-17', 'CB', 'FOMC decision (16-17 Jun)', '', 'Fed calendar'),
           A('2026-06-18', 'Auction', 'BGK FPC switch tender', 'Buys back FPC0427; may sell FPC0229, FPC0231, FPC0332, FPC0235.', 'BGK, 29 May'),
           A('2026-06-18', 'CB', 'BoE and CNB decisions', '', 'BoE/CNB calendars'),
           A('2026-06-19', 'Data', 'GUS May industrial output', '', 'GUS calendar'),
           A('2026-06-22', 'Data', 'GUS May wages, retail sales, PPI, construction', '', 'GUS calendar'),
           A('2026-06-23', 'CB', 'MNB decision', '', 'MNB calendar'),
           A('2026-06-23', 'Data', 'NBP May M3', '', 'NBP calendar'),
           A('2026-06-24', 'Auction', 'MoF sale auction PLN ' + ('7-12bn' if ge(R, '24') else '6-12bn'),
             'OK0129, NZ0331, PS0731, DS1035, DS0436, NZ0936.' if ge(R, '24') else 'OK0129, NZ0331, PS0731, DS0436, NZ0936 (plan).', 'MoF offer (first dated 23 Jun)' if ge(R, '24') else 'MoF June plan, 29 May'),
           A('2026-06-30', 'Index', 'GPWB/TBSP periodic portfolio change', 'Communique (26 Jun): OK0129 joins TBSP, 1-3Y, 1-4Y and 1-5Y; OK0127 leaves TBSP.' if ge(R, '29') else 'Maturity-window changes (see Index section).',
             'GPW Benchmark' + (', 26 Jun' if ge(R, '29') else ' rules')),
           A('2026-06-30', 'Data', 'GUS June flash CPI', 'Goldman, Santander ~2.7% (PAP, 29 Jun).' if ge(R, '30') else '', 'GUS calendar')]
    if ge(R, '30'):
        ev += [A('2026-06-30', 'Auction', 'MoF and BGK Q3/July supply plans', '', 'PAP weekly, 29 Jun'),
               A('2026-07-08', 'MPC', 'MPC decision (7-8 Jul) with the NBP July projection', 'Hold expected.', 'PAP weekly, 29 Jun')]
    if ge(R, '12'):
        ev.append(A('2026-07-23', 'CB', 'ECB decision (22-23 Jul)', '', 'ECB, 11 Jun'))
    if ge(R, '18'):
        ev.append(A('2026-07-29', 'CB', 'FOMC decision (28-29 Jul)', '', 'Fed calendar'))
    ev = sorted(ev, key=lambda e: (e['date'], e['type']))
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core: central banks, CPI
    cp = copy.deepcopy(F0['core_policy'])
    cp['Poland'].update(pricing=f"FRAs ~{abs(x)}bp of {'cuts' if x > 0 else 'hikes'} within 12M ({L} close)" if abs(x) >= 5 else f"FRAs: no net move within 12M ({L} close)")
    if held:
        cp['Poland'].update(last="held 2 Jun 2026 (3.75%)", next="7-8 Jul 2026" if ge(R, '30') else "Jul 2026", tone="wait",
                            stance=latest({'03': "On hold; data-dependent", '05': "On hold; dovish turn (Glapiński, 3 Jun)", '10': "On hold; members see cuts as more likely than hikes",
                                           '19': "On hold; stable rates the base case (Duda, 18 Jun)"}, R))
    else:
        cp['Poland'].update(last="held 6 May 2026 (3.75%)", next="1-2 Jun 2026", stance="On hold; hike odds cut by May CPI 3.1%", tone="wait")
    if ge(R, '12'):
        cp['Euro area'].update(rate=2.25, rate_disp="2.25", last="hiked 11 Jun (+25bp to 2.25%)", next="22-23 Jul 2026", stance="Hiking; meeting-by-meeting", tone="avoid", pricing=EZ[d])
    else:
        cp['Euro area'].update(last="held 30 Apr (2.00%, unanimous)", next="11 Jun 2026", stance="On hold; June hike priced", tone="wait", pricing=EZ[d])
    if ge(R, '18'):
        cp['United States'].update(last="held 17 Jun (12-0); median dot 3.8% for end-2026", next="28-29 Jul 2026", stance="On hold; dots point to a 2026 hike", tone="wait", pricing=US[d])
    else:
        cp['United States'].update(last="held 29 Apr (8-4)", next="16-17 Jun 2026", stance="On hold; Warsh chair from 22 May", tone="wait", pricing=US[d])
    if ge(R, '19'):
        cp['United Kingdom'].update(last="held 18 Jun (7-2, Greene and Pill for +25bp)", next="Jul 2026", stance="On hold; hikes priced", tone="wait", pricing=UK[d])
    else:
        cp['United Kingdom'].update(last="held 30 Apr (8-1, one vote for +25bp)", next="18 Jun 2026", stance="On hold; hikes priced", tone="wait", pricing=UK[d])
    if ge(R, '19'):
        cp['Czechia'].update(rate=3.75, rate_disp="3.75", last="hiked 18 Jun (+25bp to 3.75%, 6-1)", next="Aug 2026", stance="Hiking (first hike since 2022)", tone="avoid", pricing="no pricing found")
    else:
        cp['Czechia'].update(last="held 7 May (3.50%)", next="18 Jun 2026", stance="On hold", tone="wait", pricing="no pricing found" if not ge(R, '16') else "a hike debated for 18 Jun (15 Jun)")
    if ge(R, '24'):
        cp['Hungary'].update(rate=6.0, rate_disp="6.00", last="cut 23 Jun (-25bp to 6.00%)", next="Jul 2026", stance="Easing", tone="go", pricing="HU10Y near four-year lows; BUBOR below the base rate")
    else:
        cp['Hungary'].update(last="held 26 May (6.25%); sees room to ease", next="23 Jun 2026", stance="On hold; room to ease", tone="wait",
                             pricing="HU10Y at a four-year low (16 Jun); BUBOR below the base rate" if ge(R, '17') else "Tisza government; BUBOR below the base rate")
    cp['Romania'].update(last="held 15 May (6.50%)", next="not found", pricing="not found")
    cc = copy.deepcopy(F0['core_cpi'])
    cc['Poland'] = dict(v=3.1, m="May" + ("" if ge(R, '16') else " flash"))
    cc['Euro area'] = dict(v=3.2, m="May (core 2.6)") if ge(R, '18') else (dict(v=3.2, m="May flash (core 2.5)") if ge(R, '03') else dict(v=3.0, m="Apr (core 2.2)"))
    cc['United States'] = dict(v=4.2, m="May (core 2.9)") if ge(R, '11') else dict(v=3.8, m="Apr (core 2.8)")
    cc['United Kingdom'] = dict(v=2.8, m="May (core 2.6)") if ge(R, '18') else dict(v=2.8, m="Apr (core 2.5)")
    cc['Czechia'] = latest(CZ, R)
    cc['Hungary'] = dict(v=1.8, m="May") if ge(R, '10') else dict(v=2.1, m="Apr")
    cc['Romania'] = dict(v=10.9, m="May") if ge(R, '15') else dict(v=10.7, m="Apr")
    note = (F0['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off (GUS, Eurostat, BLS, ONS, CZSO, KSH, INS; FOMC "
            + ("17 Jun" if ge(R, '18') else "29 Apr") + ", ECB " + ("11 Jun" if ge(R, '12') else "30 Apr") + ", BoE " + ("18 Jun" if ge(R, '19') else "30 Apr")
            + ", CNB " + ("18 Jun" if ge(R, '19') else "7 May") + ", NBR 15 May, MNB " + ("23 Jun" if ge(R, '24') else "26 May") + ").")
    good = v.get('cds5y') and v.get('pl_bund_10y')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {L} close)." if good else "")
    regime = latest({'01': "Regime: a 60-day US-Iran memorandum within reach but unsigned - Brent ~$92, Bund ~2.95%; ",
                     '02': "Regime: talks stalled and Gulf clashes resumed - Brent back at ~$95-98; ",
                     '12': "Regime: the ECB has started hiking (11 Jun) while a US-Iran deal takes shape; ",
                     '16': "Regime: a preliminary US-Iran deal - Brent towards $80, core yields at two-month lows; ",
                     '19': "Regime: the US-Iran MoU in force - Brent below $80, hawkish Fed dots, a CNB hike; ",
                     '25': "Regime: oil back to pre-war levels (~$73) as Hormuz traffic normalises; "}, R)
    regime += (f"the NBP {'held at 3.75% on 2 Jun' if held else 'is at 3.75%'} while FRAs price {pr}; "
               + ("the ECB hiked to 2.25% on 11 Jun with one more hike priced" if ge(R, '12') else "the ECB is priced for a June hike")
               + ", the Fed " + ("signals a 2026 hike in its dots" if ge(R, '18') else "is priced for a 2026 hike") + ", the BoE " + ("held 7-2" if ge(R, '19') else "is priced for hikes")
               + ", the CNB " + ("hiked to 3.75%" if ge(R, '19') else "is on hold") + " and the MNB " + ("cut to 6.00%." if ge(R, '24') else "is on hold."))
    core_text = regime + spr + " " + GLOB[d]
    tk = list(Q0['takeaways_html'])
    tk[2] = latest({'01': "<b>Supply:</b> BGK sold PLN 0.94bn of FPC on 28 May (demand 1.62bn) plus 0.05bn; its first FPC switch is set for 18 Jun (buys back FPC0427); a POLSTR-based FPC floater is planned for Q3.",
                    '03': "<b>Supply:</b> BGK priced EUR 2bn of FPC bonds on 2 Jun (8Y EUR 1.25bn, 15Y EUR 0.75bn; demand EUR 4.6bn); FPC switch on 18 Jun (buys back FPC0427).",
                    '15': "<b>Supply:</b> BGK: Q3 issuance will mainly prefund the FPC's 2027 needs (~30% secured, 12 Jun); EUR 2bn priced on 2 Jun; FPC switch on 18 Jun (buys back FPC0427).",
                    '19': "<b>Supply:</b> BGK's first FPC switch (18 Jun): PLN 1.35bn sold (demand 2.11bn) vs 1.44bn of FPC0427 bought back (net about -0.09bn); Q3 issuance to prefund 2027 needs."}, R)
    mof_asof = latest({'01': "27 May 2026 sale", '05': "3 Jun 2026 switch", '18': "17 Jun 2026 sale", '25': "24 Jun 2026 sale"}, R)
    au = {"MoF auctions & switch results": dict(as_of=mof_asof, published="auction days", source="MoF wholesale-bond database (rows whose same-day release PAP confirms); MoF/PAP communiques",
                                                note="June plan (29 May): a switch on 3 Jun and sales on 17 and 24 Jun, no T-bills."
                                                + (" The 3 Jun switch result is the MoF database row (no dated in-window report found; the usual same-day MoF release is assumed)." if ge(R, '05') else "")
                                                + (" The 17 Jun additional sale is used from the 19 Jun report (no same-day source)." if ge(R, '18') else "")
                                                + (" MoF offers are used only from their first dated mention." if ge(R, '16') else "")),
          "Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)": dict(as_of="29 May 2026 change (holdings 26 May)", published="27 May 2026", source="GPW Benchmark 'Portfele obligacji' communique",
                                                          note="DS0436 joined TBSP (19 bonds), PS0527 left 1-3Y/1-4Y; units match MoF settlements to 26 May."
                                                          + (" The 30 Jun communique (26 Jun 19:02: OK0129 joins TBSP, 1-3Y and 1-4Y; OK0127 leaves TBSP) is quoted in text only" + ("; its statistics page appeared in a PDF regenerated on 29 Jun." if ge(R, '30') else ".") if ge(R, '29') else "")),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of=("2 Jun 2026 decision (hold)" if held else "6 May 2026 decision (hold)") + "; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1],
                                                             source="NBP/MPC; PAP/Bloomberg/press interviews (first dated mention)",
                                                             note=("July meeting date (7-8 Jul) first seen in the PAP weekly calendar of 29 Jun." if ge(R, '30') else ("July meeting date not yet stated in dated sources." if held else ""))),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1]}", source="PKO, Erste, Millennium, ING, Pekao, Santander, Citi, BNP, Goldman; PAP", note="Only commentary published by the info cut-off."),
          "CPI, core CPI, GDP, NBP projection": dict(as_of="May 2026 CPI " + ("final" if ge(R, '16') else "flash") + ("; core May" if ge(R, '17') else "; core Apr") + ("; Q1 GDP second estimate" if ge(R, '02') else "; Q1 GDP flash") + "; NBP March projection",
                                                     published="29 May (flash)" + (", 1 Jun (GDP)" if ge(R, '02') else "") + (", 15 Jun (final)" if ge(R, '16') else "") + (", 16 Jun (core)" if ge(R, '17') else ""), source="GUS, NBP", note=""),
          "Ratings & 2026 review calendar": dict(as_of=f"to {WIN[R]}", published="agency releases", source="S&P, Fitch, Moody's, Scope, DBRS; PAP", note=rat),
          "Central banks (ECB, Fed, BoE, CNB, MNB, BNR), peer CPI": dict(as_of=f"decisions and prints published by {WIN[R].split('-')[-1]}", published="release dates", source="ECB, Fed, BoE, CNB, MNB, NBR; Eurostat, BLS, ONS, CZSO, KSH, INS; pricing via CME FedWatch, PAP/LSEG, Trading Economics",
                                                                         note="Market pricing quoted with its own date.")}
    nfa = dict(input=f"New facts {WIN[R]} 2026", as_of=WIN[R], published=WIN[R],
               source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, Trading Economics, Odaily, ECB/Fed/BoE/CNB/MNB/NBR, rating agencies, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    od = dict(policy={'nbp_reference': 3.75, 'nbp_deposit': 3.25, 'nbp_lombard': 4.25, 'last_change': "4 Mar 2026 (-25bp, eff. 5 Mar); held 9 Apr, 6 May" + (" and 2 Jun" if held else ""),
                      'next_mpc': "2026-07-07/08" if ge(R, '30') else ("2026-07" if held else "2026-06-01/02")},
              facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
              quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = ops_add(R)
    if adds:
        od['mof_ops_add'] = adds
    sn = {'2026-06-03': "T+2 = 5 Jun (4 Jun Corpus Christi)", '2026-06-05': "T+2 = 8 Jun (4 Jun Corpus Christi and the weekend)", '2026-06-30': "T+2 = 1 Jul"}
    if R in sn:
        od['settlement_note'] = sn[R]
    OUT[R] = od
json.dump(OUT, open(SP / 'jun/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
