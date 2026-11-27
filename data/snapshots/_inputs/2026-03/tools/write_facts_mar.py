"""Per-day point-in-time narrative for 2-31 Mar 2026 reports -> mar/facts_days.json (merged into the day specs)."""
import json, copy, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user/2b986bc3-1107-5358-8c0f-f544109c09bc/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
F27 = json.load(open(REPO / 'data/snapshots/2026-02-27/facts.json'))
Q27 = json.load(open(REPO / 'data/snapshots/2026-02-27/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_mar_fix/fixings.json'))['by_date']
CV = {**json.load(open(SP / 'agent_mar_curves1/curves.json')), **json.load(open(SP / 'agent_mar_curves2/curves.json'))}
P2 = json.load(open(SP / 'agent_mar_plfacts2/facts.json'))
OPS = {o['date']: o for o in P2['mof_ops'] if isinstance(o, dict) and o.get('date') in ('2026-03-18', '2026-03-25')}
RS = ['02', '03', '04', '05', '06', '09', '10', '11', '12', '13', '16', '17', '18', '19', '20', '23', '24', '25', '26', '27', '30', '31']
DAYS = [f'2026-03-{d}' for d in RS]
CUTS = ['2026-02-27'] + DAYS[:-1]
WINS = ['27 Feb-1 Mar', '2 Mar', '3 Mar', '4 Mar', '5 Mar', '6-8 Mar', '9 Mar', '10 Mar', '11 Mar', '12 Mar', '13-15 Mar', '16 Mar', '17 Mar', '18 Mar', '19 Mar',
        '20-22 Mar', '23 Mar', '24 Mar', '25 Mar', '26 Mar', '27-29 Mar', '30 Mar']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
ge = lambda R, d: R >= '2026-03-' + d
lab = lambda C: f"{int(C[8:])} {'Feb' if C[5:7] == '02' else 'Mar'}"

WK = {
 '02': "27 Feb-1 Mar: Fitch affirmed Poland at A- with a negative outlook (27 Feb, late evening); MoF's March plan has sales on 18 and 25 Mar (PLN 7-13bn each, incl. new PS0731 and NZ0936) and an 11 Mar switch; non-residents added PLN 13.7bn of POLGBs in January (12.5% share). On Saturday 28 Feb the US and Israel struck Iran; Iran's Supreme Leader was killed and the Revolutionary Guard declared Hormuz closed. Before the war Brent settled $72.5 and UST 10Y was just under 4.0%.",
 '03': "2 Mar: Brent opened 13% higher (above $80); the pre-war consensus for 4 Mar was a 25bp cut; manufacturing PMI 47.1 (49.4 expected); Q4 GDP confirmed at 4.0%; EUR/PLN 4.24. Abroad: US ISM 52.4; Fed swaps ~59bp of 2026 cuts; UST 10Y 4.05% (+11bp).",
 '04': "3 Mar: POLGBs sold off - 2Y +14bp to 3.79%, 5Y +16bp to 4.56%, 10Y +15bp to 5.22% - and EUR/PLN rose 1.45% to 4.30, the highest since April 2025; IRS +8-10bp, FRA +10-14bp (2 Mar). Abroad: euro-area flash HICP 1.9% (1.7% expected), core 2.4%; markets put 50% on an ECB hike by year-end.",
 '05': "4 Mar: the MPC cut all rates by 25bp (reference 3.75% from 5 Mar), citing geopolitical risk to commodity prices; the March projection (data to 19 Feb, war excluded) has 2026 CPI in a 1.6-2.9% band; ING called it a 'hawkish cut'; 2Y yields fell after the decision. Abroad: US ISM services 56.1, ADP +63k; Warsh's nomination went to the Senate.",
 '06': "5 Mar: Glapiński said the projection excludes the war; if things calm within about two months the old scenario of one more cut returns; the MPC gives no guidance. POLGBs rose 10-17bp (2Y 3.75%, 5Y 4.66%, 10Y 5.35%). Abroad: Nagel, Rehn and de Guindos warned on inflation and an ECB hike is priced above 50%; a US trade court ordered refunds of the voided tariffs.",
 '09': "6-8 Mar: the NBP Inflation Report (6 Mar) has central CPI 2.3% (2026), 2.4% (2027), GDP 3.9% (2026); Wnorowski: forget further cuts while the war lasts; Kotecki: room 'much smaller'; the 10Y POLGB rose ~56bp in the week and the 2Y neared 4.0%. Abroad: US payrolls -92k (+55k expected) but Brent rose ~27% in the week to ~$92-93.",
 '10': "9 Mar: POLGBs fell another ~30bp (2Y 4.22%, 5Y 5.17%, 10Y 5.85%) with Brent near $120 at the open; FRAs now price NBP hikes; MoF cancelled the 11 Mar switch auction on market volatility; ING raised its 2026 CPI forecast to 2.5-3.0%. Late on 9 Mar Brent fell below $90 after Trump said the war was 'basically over'; Mojtaba Khamenei was named leader; Hungary's 10Y hit 7.35%.",
 '11': "10 Mar: POLGB yields fell 23-24bp on the oil pullback (10Y ~5.36% after briefly topping 5.90% on 9 Mar); Pekao cut its 2026 GDP forecast to 3.8%; Moody's said its review next week will incorporate the war. Abroad: Lagarde pledged 'everything necessary' and at least one ECB hike is priced; Hungarian and Czech February CPI 1.4%.",
 '12': "11 Mar: Kotecki said the March cut was 'rather the end' for this year; short POLGB yields jumped up to 21bp; BGK cancelled its 12 Mar FPC auction; Glapiński announced active management of NBP gold. Abroad: US February CPI in line (core 2.5% y/y); the IEA announced a record 400m-barrel release; ECB's Kazimir said a hike may be closer than many think.",
 '13': "12 Mar: Janczyk and Kotecki say the cut discussion is over for now (not April); Fitch's quarterly sees one last NBP cut in 2026; the market prices two NBP hikes within 12 months (ING); in the evening the President vetoed the SAFE defence-loan law. Abroad: Brent back above $100; two ECB hikes priced; only ~24bp of Fed cuts left for 2026; UST 2Y near 3.70%.",
 '16': "13-15 Mar: February CPI 2.1% y/y on the new COICOP 2018 weights (in line; January revised to 2.1%); Domański: MoF will adjust supply to market conditions; Masłowska set a high bar for hikes; the cabinet plans to route the SAFE loan via BGK for the Armed Forces Support Fund. POLGB yields rose 20-50bp in the week and 80-90bp since 2 Mar. Abroad: Brent back above $100; a July ECB hike fully priced; only ~24bp of Fed cuts left for 2026; the US struck Kharg Island.",
 '17': "16 Mar: MoF turned the 18 Mar sale into a switch auction; core CPI fell to 2.5% in February (first at or below target since 2019); January current account +EUR 1.15bn (-0.3bn expected); the budget deficit after February was PLN 48.5bn. Abroad: Brent ~$100-105; allies declined to join Hormuz operations; Trump demanded an emergency Fed cut.",
 '18': "17 Mar: POLGBs rallied 7-17bp on easing oil and the low core print (PKO); Fitch said the SAFE veto underlines political-deadlock risk. Abroad: German ZEW collapsed to -0.5 (39.2 expected); at least one ECB hike priced; one Fed cut priced instead of two.",
 '19': "18 Mar: the switch auction sold PLN 9.48bn (OK0128, NZ0928, NZ0331, new PS0731 at 5.011%, new NZ0936) and bought back 9.17bn of 2026-27 paper; March consumer confidence fell 3.1pt with price expectations jumping. Abroad: the Fed held 11-1 (median still one 2026 cut, 7 of 19 dots none; Powell said a hike was discussed); US PPI +0.7% m/m; Brent ~$110 after strikes on Gulf gas fields.",
 '20': "19 Mar: February wages +6.1% y/y (6.6% expected), industry +1.5%, construction -13.7%, PPI -2.3%; Dąbrowski: the MPC waits for the war to end; the NZ coupon for the period to 25 Mar was set at 3.98% (19 Mar). Abroad: ECB held at 2.00% (2026 inflation projection 2.6%, with war scenarios); BoE held 9-0 with 2Y gilts +30bp; CNB held; no Fed cut is priced for 2026.",
 '23': "20-22 Mar: MoF set the WZ0330/WZ0930 coupon at 3.86% from 25 Mar (20 Mar); Moody's took no action on Poland (A2, negative; 20 Mar evening); GUS business climate deteriorated. Abroad: three ECB hikes priced (~75% for April), a BoE hike by June, ~50% for a Fed hike by October; the Bund rose above 3% (highest since 2011) and gilts above 5%; Trump issued a 48-hour ultimatum on Iranian power plants.",
 '24': "23 Mar: Trump postponed strikes on Iranian energy infrastructure by five days and Brent fell 13% intraday; the 2Y POLGB touched 4.86% intraday before retreating; MoF cut the 25 Mar offer to PLN 3-8bn; February retail sales +5.0% (6.1% expected); Kotecki: wait-and-see, the March cut likely the last even if the war ends; Glapiński (WSJ): no pre-commitment. S&P reviews Poland on 8 May.",
 '25': "24 Mar: POLGBs rallied 3-29bp on Monday's de-escalation signal, then the short end rose again; futures price more than three NBP hikes by year-end (BNP Paribas TFI); Tyrowicz sees 4.75% as the appropriate rate; BGK set an FPC auction for 26 Mar. Abroad: euro-area flash PMI 50.5 with input costs rising fastest since 2023; MNB held at 6.25%.",
 '26': "25 Mar: the MoF sale raised PLN 7.29bn on 8.52bn of demand plus 0.40bn additional (DS1035 at 5.725%, PS0731 at 5.399%); MoF says 2026 needs are ~41% financed; yields fell 8-12bp on the day; FRAs price ~75bp of NBP hikes in 2026 (PKO). Abroad: a US 15-point peace plan was sent via Pakistan; UK CPI 3.0%; Lagarde: ready to act 'decisively and quickly'.",
 '27': "26 Mar: the government adopted a fuel package (VAT on fuel cut to 8%, excise to the EU minimum, price caps; ING: about -0.9pp off CPI); Dąbrowski: the MPC leans to holding rather than hiking; BGK sold PLN 0.87bn of FPC (demand 1.06bn); markets price ~50bp of NBP hikes this year; Polish bonds rallied on peace-talk hopes. Abroad: the Bund rose 11bp to 3.07%; the European Parliament approved the EU-US trade deal with conditions.",
 '30': "27-29 Mar: the fuel laws were passed and signed (27 Mar); PKO and Millennium see April CPI ~0.9pp lower (to ~2%) from ~3% in March; GPW Benchmark announced that PS1026 leaves TBSP at the 31 Mar change; POLGB yields rose 2-9bp on 27 Mar. Abroad: Brent ~$113 (a record ~49% gain in March); OAT yields at the highest since 2009 and JGBs since 1999; ~71% for an April ECB hike.",
 '31': "30 Mar: the 10Y POLGB is ~110bp higher than at the start of March; the long end came under pressure on the fiscal cost of the fuel shield; PKO cut its 2026 GDP forecast to 3.5% and sees NBP rates stable; March flash CPI (31 Mar) is expected slightly above 3%. Abroad: Powell said the Fed can 'wait and see' a supply shock and UST 10Y fell 11bp to 4.33%; April ECB-hike odds eased to ~50%; the dollar index at 100.5.",
}
US = {'02': "~43% for a June cut (FedWatch, 26 Feb)", '03': "~59bp of 2026 cuts priced (2 Mar)", '04': "~97.5% March hold (FedWatch, 3 Mar)", '05': "~97.5% March hold (FedWatch, 3 Mar)",
      '06': "~97.5% March hold; Miran wants a March cut (4 Mar)", '09': "~44bp of 2026 cuts after -92k payrolls (6 Mar)", '10': "~44bp of 2026 cuts (6 Mar)", '11': "~44bp of 2026 cuts (6 Mar)",
      '12': "~44bp of 2026 cuts; February CPI in line (11 Mar)", '13': "only ~24bp of 2026 cuts left (12 Mar)", '16': "~24bp of 2026 cuts (12 Mar)", '17': "Trump demands an emergency cut; ~24bp priced (16 Mar)",
      '18': "one cut priced for 2026 instead of two (17 Mar)", '19': "held 11-1 on 18 Mar; median dot one 2026 cut, 7 of 19 none", '20': "no cut priced for 2026 (19 Mar)",
      '23': "~50% for a hike by October (20-22 Mar)", '24': "~50% for a hike by October (22 Mar)", '25': "~50% for a hike by October (22 Mar)", '26': "~50% for a hike by October (22 Mar)",
      '27': "hike risk priced (22 Mar)", '30': "hike risk priced; UMich 1Y inflation expectations 3.8% (27 Mar)", '31': "Powell (30 Mar): can 'wait and see' a supply shock; hike bets dropped"}
EZ = {'04': "~50% for a hike by year-end (3 Mar)", '06': "a hike by year-end priced above 50% (5 Mar)", '11': "at least one hike priced (10 Mar)", '13': "two hikes priced (12 Mar)",
      '16': "a July hike fully priced (13 Mar)", '23': "three hikes priced, ~75% for April (20-22 Mar)", '30': "~71% for an April hike (27 Mar)", '31': "~50% for April after Schnabel (27-30 Mar)"}
GLOB = {'02': " War began on 28 Feb: Hormuz declared closed.", '03': " Brent +13% at the open (2 Mar).", '04': " Euro-area flash HICP 1.9% (3 Mar).", '05': " NBP cut into the oil shock (4 Mar).",
        '06': " ECB hike priced (5 Mar).", '09': " Brent +27% in the week (6 Mar).", '10': " Brent near $120, then below $90 (9 Mar).", '11': " Lagarde: 'everything necessary' (10 Mar).", '12': " US CPI in line; IEA release (11 Mar).",
        '13': " Brent back above $100 (12 Mar).", '16': " July ECB hike fully priced (13 Mar).", '17': " Brent ~$100-105 (16 Mar).", '18': " German ZEW -0.5 (17 Mar).", '19': " Fed 11-1 hold, hike discussed (18 Mar).",
        '20': " ECB, BoE, CNB on hold with hawkish tilts (19 Mar).", '23': " Bund above 3%, gilts above 5% (20 Mar).", '24': " Strikes postponed; Brent -13% intraday (23 Mar).", '25': " Euro-area PMI 50.5 (24 Mar).",
        '26': " US 15-point plan via Pakistan (25 Mar).", '27': " Bund 3.07% (26 Mar).", '30': " Brent ~$113, +49% in March (27 Mar).", '31': " Powell: wait and see (30 Mar)."}

OUT = {}
for R in DAYS:
    d = R[8:]; C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; L = lab(C)
    x = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    pr = f"roughly {abs(x)}bp of NBP {'cuts' if x > 0 else 'hikes'}" if abs(x) >= 5 else "no net NBP move"
    fra_s = f"FRAs at the {L} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price {pr} within 12 months."
    cut = ge(R, '05')
    # ---------------- policy
    if not cut:
        V = ["The pre-war consensus for the 3-4 Mar MPC was a 25bp cut to 3.75% with the new projection; the US-Israel war on Iran (28 Feb) has since lifted oil and global yields."]
    else:
        V = ["The MPC cut by 25bp to 3.75% on 4 Mar (a 'hawkish cut', ING); the projection excludes the war."]
        if ge(R, '06'):
            V += ["Glapiński (5 Mar): if things calm within about two months, one more cut is back on the table; no forward guidance."]
        if ge(R, '09'):
            V += ["Wnorowski (6 Mar): no further cuts while the war lasts; Kotecki: room 'much smaller'." if R < '2026-03-12' else
                  "Kotecki (11-12 Mar): the March cut was probably the last this year; Janczyk: wait-and-see for months." if R < '2026-03-20' else
                  "Dąbrowski (19 Mar): the MPC waits for the war to end; Kotecki (23 Mar): wait-and-see, neither cuts nor hikes." if R < '2026-03-27' else
                  "Dąbrowski (26 Mar): the MPC leans to holding rather than hiking; Tyrowicz (24 Mar) sees 4.75% as appropriate."]
        if ge(R, '17'):
            V += ["Core CPI fell to 2.5% in February (16 Mar)."]
        if ge(R, '27'):
            V += ["The fuel package (26-27 Mar) takes ~0.9pp off April CPI (ING, PKO)."]
    pricing = fra_s + " " + " ".join(V)
    if not cut:
        risk = "The war shock (oil, PLN, global yields) collides with the 4 Mar decision: a hold would lift short FRAs further; a cut into rising oil risks being read as a policy error."
    elif R < '2026-03-17':
        risk = "Oil and the war set the direction: if Brent stays near $100 the market keeps pricing NBP hikes and the front-end roll-down reverses; a ceasefire would bring cuts back (Glapiński's 'two months'). SAFE politics add a fiscal premium."
    else:
        risk = "The market prices NBP hikes while MPC members lean to holding: if oil and inflation expectations keep rising the front end has further to go; the fuel shield and a ceasefire are the relief valves. Long end: global term premia (Bund >3%) and the fiscal cost of the shield."
    policy = dict(nbp_reference=3.75 if cut else 4.0, next_mpc_label=("MPC next: 8-9 Apr" if cut else "MPC next: 3-4 Mar"), pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = dict(v=2.1, m="Feb (GUS, 13 Mar; COICOP 2018, new weights)" + ("; core 2.5%" if ge(R, '17') else "")) if ge(R, '16') else dict(v=2.2, m="Jan flash (GUS, 13 Feb; old weights)")
    proj = ("NBP November 2025 projection: CPI 2.9% (2026); the March projection comes with the 3-4 Mar MPC." if not cut else
            "NBP March projection (4 Mar; data to 19 Feb, war excluded): CPI 50% bands 1.6-2.9% (2026), 1.1-3.7% (2027)" + ("; central path 2.3% / 2.4% / 2.3% (2026-28), GDP 3.9% in 2026 (Inflation Report, 6 Mar)." if ge(R, '09') else "."))
    fiscal = ("2025 general-government deficit ~7.0% of GDP (MoF figures in Fitch: 7.0% / 6.5% / 6.2% for 2025-27, debt ~70% of GDP by 2027); 2026 deficit cap PLN 271.7bn"
              + ("; the President vetoed the SAFE law (12 Mar)" if ge(R, '13') else "") + ("; the cabinet plans to take the SAFE loan via BGK for the Armed Forces Support Fund (13 Mar)" if ge(R, '16') else "")
              + ("; budget deficit after February PLN 48.5bn (17.8% of the limit)" if ge(R, '17') else "") + ("; fuel package from 27 Mar (VAT 8%, minimum excise, price caps)" if ge(R, '27') else "") + ".")
    fin = "~38% (25 Feb)" if R < '2026-03-26' else "~41% (25 Mar)"
    adj = ("; MoF cancelled the 11 Mar switch" if ge(R, '10') else "") + ("; turned the 18 Mar sale into a switch" if ge(R, '17') else "") + ("; cut the 25 Mar offer to PLN 3-8bn" if ge(R, '24') else "")
    frisk = (f"2026 needs {fin} financed{adj}; budget accounts ~PLN 171.6bn at end-February. "
             + ("Moody's reviews Poland on 20 Mar (A2, negative)." if R < '2026-03-23' else "Moody's took no action (20 Mar); " + ("S&P reviews on 8 May." if ge(R, '24') else "")))
    base = (("The NBP cut to 3.75% on 4 Mar after holding at 4.00% in January and February" if cut else "The NBP held at 4.00% in January and February")
            + ("; February CPI 2.1% y/y on new weights" if ge(R, '16') else "; January flash CPI 2.2%") + "; 2025 GDP 3.6%, Q4 4.0%. Ratings: Fitch A- negative (affirmed 27 Feb), Moody's A2 negative"
            + (" (no action 20 Mar)" if ge(R, '23') else "") + ", S&P A- stable.")
    macro = dict(cpi=cpi, projection_text=proj, fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + WK[d])
    # ---------------- calendar
    plan = ("MoF March plan (27 Feb): sale auctions on 18 and 25 Mar (PLN 7-13bn each; OK0128, NZ0331, PS0731 (new 5Y fixed), DS1035, NZ0936 (new 10Y POLSTR floater)) and a switch on 11 Mar buying back OK0426, DS0726, PS1026, WZ1126 and OK0127; no T-bills; WZ sales ended in February. "
            "February sales were ~PLN 41bn; ~38% of 2026 needs financed.")
    if ge(R, '10'):
        plan += " 9 Mar: MoF cancelled the 11 Mar switch because of market volatility."
    if ge(R, '12'):
        plan += " BGK cancelled its 12 Mar FPC auction (11 Mar)."
    if ge(R, '16'):
        plan += " Domański (13 Mar): supply will be adjusted to market conditions."
    if R in ('2026-03-17', '2026-03-18'):
        plan += " 16 Mar: the 18 Mar sale becomes a switch auction."
    if ge(R, '19'):
        o = OPS['2026-03-18']; ls = {l['series']: l for l in o['lines_sold']}
        plan += f" 18 Mar switch: PLN {o['total_sold_mn']/1000:.2f}bn sold (cover {o['sale_bid_to_cover']:.2f}; OK0128 {ls['OK0128']['avg_yield']:.3f}%, new PS0731 4.00% Jul-2031 at {ls['PS0731']['avg_yield']:.3f}%, new NZ0936) and PLN {o['total_bought_back_mn']/1000:.2f}bn of 2026-27 paper bought back."
    if R in ('2026-03-24', '2026-03-25'):
        plan += " 25 Mar offer (23 Mar) cut to PLN 3-8bn: OK0128, NZ0928, NZ0331, PS0731, DS1035, NZ0936."
    if ge(R, '26'):
        o = OPS['2026-03-25']; ls = {l['series']: l for l in o['lines']}
        plan += (f" 25 Mar sale: PLN {o['total_sold_mn']/1000:.2f}bn vs {o['total_demand_mn']/1000:.2f}bn demand (cover {o['total_demand_mn']/o['total_sold_mn']:.2f}) plus {o['additional_sale']['total_mn']/1000:.2f}bn additional; "
                 f"stop yields OK0128 {ls['OK0128']['avg_yield']:.3f}%, PS0731 {ls['PS0731']['avg_yield']:.3f}%, DS1035 {ls['DS1035']['avg_yield']:.3f}%; ~41% of 2026 needs financed.")
    if ge(R, '27'):
        plan += " BGK FPC (26 Mar): PLN 0.87bn sold vs 1.06bn demand plus 0.20bn."
    left = ("18 and 25 Mar" if R <= '2026-03-18' else "25 Mar" if R <= '2026-03-25' else "the April dates (plan due at month-end)")
    timing = (f"The Aug 2025-Feb 2026 pattern (auction-day close the cheapest point of the week) comes from a rally regime; in March's sell-off MoF is cutting supply (switch instead of sale, a smaller 25 Mar offer), so remaining dates ({left}) are less of a supply event. ")
    timing += ("The 3-4 Mar MPC is the event: the pre-war consensus was a cut." if not cut else "Next MPC 8-9 Apr: a hold is expected while the market prices hikes.")
    if ge(R, '26'):
        timing += " The 25 Mar cover of 1.17 was the weakest of 2026."
    ev = [e for e in copy.deepcopy(F27['calendar']['events']) if e['type'] == 'Rating']
    A = lambda dt_, ty, ti, no='', sd='': dict(date=dt_, type=ty, title=ti, note=no, source_date=sd)
    ev += [A('2026-03-04', 'MPC', 'MPC decision (3-4 Mar) + March projection', 'Pre-war consensus: -25bp.' if ge(R, '03') else '', 'NBP schedule'),
           A('2026-03-05', 'MPC', 'Glapiński press conference', '', 'NBP'), A('2026-03-06', 'MPC', 'NBP March Inflation Report', '', 'NBP practice'),
           A('2026-03-13', 'Data', 'GUS February CPI (new COICOP 2018 weights)', '', 'GUS calendar'), A('2026-03-16', 'Data', 'NBP core inflation (Jan-Feb)', '', 'NBP calendar'),
           A('2026-03-18', 'CB', 'FOMC decision', '', 'Fed calendar'), A('2026-03-19', 'CB', 'ECB, BoE, CNB decisions', '', 'CB calendars'),
           A('2026-03-19', 'Data', 'GUS February wages, industry, PPI, construction', '', 'GUS calendar'), A('2026-03-23', 'Data', 'GUS February retail sales', '', 'GUS calendar'),
           A('2026-03-24', 'CB', 'MNB decision', '', 'MNB calendar'),
           A('2026-03-25', 'Cash flow', 'WZ0330 / WZ0930 coupon reset; NZ coupons', 'New WZ coupon 3.86% (MoF, 20 Mar).' if ge(R, '23') else '', 'bond terms'),
           A('2026-03-31', 'Index', 'GPWB/TBSP periodic portfolio change', 'Communique (27 Mar): PS1026 leaves TBSP; no other changes.' if ge(R, '30') else 'Maturity-window changes (see Index section).', 'GPW Benchmark' + (', 27 Mar' if ge(R, '30') else ' rules')),
           A('2026-03-31', 'Data', 'GUS March flash CPI', 'Expected slightly above 3% (PAP, 30 Mar).' if ge(R, '31') else '', 'GUS calendar')]
    if R <= '2026-03-09':
        ev.append(A('2026-03-11', 'Auction', 'MoF switch auction (buy OK0426, DS0726, PS1026, WZ1126, OK0127)', '', 'MoF March plan, 27 Feb'))
    if R in ('2026-03-10', '2026-03-11'):
        ev.append(A('2026-03-12', 'Auction', 'BGK FPC auction', '', 'PAP week-ahead, 9 Mar'))
    ev.append(A('2026-03-18', 'Auction', 'MoF switch auction (instead of sale)' if ge(R, '17') else 'MoF sale auction PLN 7-13bn', '', 'MoF, 16 Mar' if ge(R, '17') else 'MoF March plan, 27 Feb'))
    ev.append(A('2026-03-25', 'Auction', 'MoF sale auction PLN ' + ('3-8bn' if ge(R, '24') else '7-13bn'), 'OK0128, NZ0928, NZ0331, PS0731, DS1035, NZ0936.' if ge(R, '24') else '', 'MoF offer, 23 Mar' if ge(R, '24') else 'MoF March plan, 27 Feb'))
    if R in ('2026-03-25', '2026-03-26'):
        ev.append(A('2026-03-26', 'Auction', 'BGK FPC auction (min PLN 500m)', '', 'BGK, 24 Mar'))
    if cut:
        ev.append(A('2026-04-09', 'MPC', 'MPC decision (8-9 Apr)', 'Hold expected; market prices hikes.' if ge(R, '13') else '', 'NBP schedule'))
    if ge(R, '24'):
        ev.append(A('2026-05-08', 'Rating', 'S&P review of Poland (A-, stable)', '', 'Millennium, 23 Mar'))
    ev = sorted(ev, key=lambda e: (e['date'], e['type']))
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core
    cp = copy.deepcopy(F27['core_policy'])
    cp['Poland']['pricing'] = f"FRAs ~{abs(x)}bp of {'cuts' if x > 0 else 'hikes'} within 12M ({L} close)"
    if cut:
        cp['Poland'].update(rate=3.75, rate_disp="3.75", last="-25bp 4 Mar 2026 (eff. 5 Mar)", next="8-9 Apr 2026", stance="Wait-and-see after a 'hawkish cut'", tone="wait")
    cp['United States']['pricing'] = US[d]
    if ge(R, '19'):
        cp['United States'].update(last="held 18 Mar (11-1)", next="28-29 Apr 2026")
    k = max([kk for kk in EZ if ge(R, kk)], default=None)
    if k:
        cp['Euro area']['pricing'] = EZ[k]
    if ge(R, '20'):
        cp['Euro area'].update(last="held 19 Mar (2.00%, unanimous)", next="Apr 2026")
        cp['United Kingdom'].update(last="held 19 Mar (9-0)", next="Apr 2026")
        cp['Czechia'].update(last="held 19 Mar (3.50%, 7-0)", next="May 2026")
    cp['United Kingdom']['pricing'] = ("~60% for a March cut (2 Mar)" if R < '2026-03-06' else "~20% for a March cut (5 Mar)" if R < '2026-03-20' else "2Y gilt +30bp after the hold (19 Mar)" if R < '2026-03-23' else "a hike priced by June (20-22 Mar)")
    if ge(R, '12'):
        cp['Hungary']['pricing'] = "MNB minutes: the February cut did not start a cycle (11 Mar)"
    if ge(R, '25'):
        cp['Hungary'].update(last="held 24 Mar (6.25%; cut 24 Feb)", next="Apr 2026", stance="On hold after one cut", tone="wait")
    cc = copy.deepcopy(F27['core_cpi'])
    if ge(R, '04'):
        cc['Euro area'] = dict(v=1.9, m="Feb flash (core 2.4)")
    if ge(R, '11'):
        cc['Czechia'] = dict(v=1.4, m="Feb"); cc['Hungary'] = dict(v=1.4, m="Feb")
    if ge(R, '16'):
        cc['Poland'] = dict(v=2.1, m="Feb (new weights)")
    if ge(R, '26'):
        cc['United Kingdom'] = dict(v=3.0, m="Feb (core 3.2)")
    note = F27['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off (GUS, Eurostat, BLS, ONS, CZSO, KSH; FOMC 18 Mar, ECB/BoE/CNB 19 Mar, MNB 24 Mar where in the window)."
    good = v.get('cds5y') and v.get('pl_bund_10y') and not v.get('flags')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {L} close)." if good else f" (Erste's CDS/spread table for {L} looked stale or inconsistent, so it is not quoted.)")
    regime = (("Regime: war shock - oil and global yields up, PLN weaker; " if C >= '2026-02-27' else "")
              + ("the NBP cut to 3.75% and turned wait-and-see" if cut else "the NBP was expected to cut on 4 Mar") + f" while FRAs price {pr}; the ECB is priced for hikes, the Fed is on hold, the BoE has turned hawkish, the CNB and MNB are on hold.")
    core_text = regime + spr + GLOB[d]
    tk = list(Q27['takeaways_html'])
    tk[2] = ("<b>Supply:</b> no FPC auction announced yet in March; BGK's February auctions raised PLN 6.4bn incl. additional sales." if R < '2026-03-10' else
             "<b>Supply:</b> BGK planned an FPC auction for 12 Mar." if R < '2026-03-12' else
             "<b>Supply:</b> BGK cancelled the 12 Mar FPC auction and says ~60% of its 2026 FPC financing is already raised (11 Mar)" + (" ; a new auction is set for 26 Mar (min PLN 500m)." if R in ('2026-03-25', '2026-03-26') else "." if R < '2026-03-27' else
             "; on 26 Mar it sold only PLN 0.87bn (demand 1.06bn) plus 0.20bn - quasi demand is thin in the sell-off."))
    au = {"MoF auctions & switch results": dict(as_of=("25 Mar 2026 sale" if ge(R, '26') else "18 Mar 2026 switch" if ge(R, '19') else "25 Feb 2026 sale"), published="auction days",
                                            source="MoF wholesale-bond database (rows whose same-day release PAP confirms); MoF/PAP communiques", note="11 Mar switch cancelled; 18 Mar sale replaced by a switch; new PS0731 and NZ0936 first issued 18 Mar." if ge(R, '19') else ""),
          "Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)": dict(as_of="27 Feb 2026 change (holdings 24 Feb)", published="25 Feb 2026", source="GPW Benchmark 'Portfele obligacji' communique",
                                                          note="No membership changes; units match MoF settlements to 20 Feb." + (" The 31 Mar communique (27 Mar; served PDF regenerated 30 Mar) is quoted in text only." if ge(R, '30') else "")),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of=("4 Mar 2026 decision (-25bp)" if cut else "4 Feb 2026 decision") + "; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1], source="NBP/MPC; PAP/Bloomberg/press interviews (first dated mention)", note=""),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1]}", source="PKO, Erste, Millennium, ING, Pekao, Deutsche Bank Polska, BNP TFI, Bank Pocztowy; PAP", note="Only commentary published by the info cut-off.")}
    if ge(R, '23'):
        au["WZ coupons"] = dict(as_of="periods from 25 Mar 2026 (WZ0330, WZ0930: 3.86%)", published="20 Mar 2026", source="MoF rate notices (WIBOR 6M 18-20 Mar: 3.85/3.86/3.87)", note="Applied in the floater engine from the 25 Mar close.")
    if R == '2026-03-09':
        au["PLN IRS curve"] = dict(note="Erste's 9 Mar daily heads its tables 05/03 but the IRS/FRA levels are new and consistent with its change columns and PAP's 6 Mar bond moves: used as the 6 Mar close. Bid side; 7Y not available.")
    nfa = dict(input=f"New facts {WIN[R]} 2026", as_of=WIN[R], published=WIN[R], source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, ECB/BoE/CNB/MNB, rating agencies, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    od = dict(policy=({'nbp_reference': 3.75, 'nbp_deposit': 3.25, 'nbp_lombard': 4.25, 'last_change': "4 Mar 2026 (-25bp, eff. 5 Mar)", 'next_mpc': "2026-04-08/09"} if cut else
                      {'nbp_reference': 4.0, 'last_change': "3 Dec 2025 (-25bp); held 14 Jan and 4 Feb 2026", 'next_mpc': "2026-03-03/04"}),
              facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
              quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = []
    if ge(R, '19'):
        o = OPS['2026-03-18']
        adds.append(dict(date='2026-03-18', settle=o.get('settlement'), type='S', op='AZ', lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines_sold'] if l.get('sold_mn')]))
    if ge(R, '26'):
        o = OPS['2026-03-25']
        adds += [dict(date='2026-03-25', settle=o.get('settlement'), type='S', op='AS', lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]),
                 dict(date='2026-03-25', settle=o.get('settlement'), type='S', op='OB', lines=[dict(series=s, sold=q, demand=None, avg_yld=None, price=None) for s, q in o['additional_sale']['lines'].items() if q])]
    if adds:
        od['mof_ops_add'] = adds
    if ge(R, '26'):
        od['floaters_update'] = {'WZ0330': {'coupon': 3.86, 'period_start': '2026-03-25'}, 'WZ0930': {'coupon': 3.86, 'period_start': '2026-03-25'}}
    OUT[R] = od
json.dump(OUT, open(SP / 'mar/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
