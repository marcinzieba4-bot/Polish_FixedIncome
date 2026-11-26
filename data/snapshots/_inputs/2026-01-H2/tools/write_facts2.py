"""Per-day point-in-time narrative for 16-30 Jan 2026 reports -> jan2/facts_days.json (merged into the day specs)."""
import json, copy, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user/2b986bc3-1107-5358-8c0f-f544109c09bc/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
F15 = json.load(open(REPO / 'data/snapshots/2026-01-15/facts.json'))
Q15 = json.load(open(REPO / 'data/snapshots/2026-01-15/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_jan2_fix/fixings.json'))['by_date']
CV = json.load(open(SP / 'agent_jan2_curves/curves.json'))
PLF = json.load(open(SP / 'agent_jan2_plfacts/facts.json'))
DAYS = ['2026-01-16', '2026-01-19', '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23', '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29', '2026-01-30']
CUTS = ['2026-01-15', '2026-01-16', '2026-01-19', '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23', '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29']
WINS = ['15 Jan 2026', '16-18 Jan 2026', '19 Jan 2026', '20 Jan 2026', '21 Jan 2026', '22 Jan 2026', '23-25 Jan 2026', '26 Jan 2026', '27 Jan 2026', '28 Jan 2026', '29 Jan 2026']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
LBL = {R: f"{int(C[8:])} Jan" for R, C in CUT.items()}
ge = lambda R, d: R >= d
OPS = {o['date']: o for o in PLF['mof_ops'] if isinstance(o, dict) and o.get('type') == 'sale'}

OUT = {}
for R in DAYS:
    C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; lab = LBL[R]
    cuts = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    fra_s = (f"FRAs at the {lab} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) "
             f"price roughly {cuts}bp of NBP cuts within 12 months.")
    # ---------------- policy
    V = ["The MPC held at 4.00% on 14 Jan. Glapiński (15 Jan): a terminal rate of about 3.5% with a real rate of at least 1-1.5%, cuts in 25bp steps; he excluded neither February nor March (or even April)."]
    if R == '2026-01-16':
        V += ["Post-conference (15 Jan): ING sees the next cut in March and 3.25% by end-2026; BNP two cuts to 3.50%; Bank Pocztowy says investors started pricing February. December final CPI confirmed 2.4% y/y (15 Jan)."]
    if ge(R, '2026-01-19'):
        V += ["Kotecki (16 Jan) expects the MPC to resume cuts in February and PKO now sees February as highly probable; Wnorowski (16 Jan) prefers March; core CPI 2.7% in December (16 Jan; 2.8% expected)."]
    if ge(R, '2026-01-20'):
        V += ["Tyrowicz (19 Jan): 'rather no room' to cut; Credit Agricole and Deutsche Bank expect March (DB: March and May, to 3.50%)."]
    if ge(R, '2026-01-22'):
        V += ["New member Zarzecki (21 Jan): resuming cuts before the March projection confirms durable disinflation would be 'premature and risky'."]
    if ge(R, '2026-01-23'):
        V += ["December data beat forecasts (22 Jan): wages +8.6% y/y (6.9% expected), industry +7.3% (2.9%), construction +4.5%; ING (22 Jan) says this lowers the odds of February, with a pause until March the base case."]
    if ge(R, '2026-01-26'):
        V += ["Erste (23 Jan): the data significantly weaken the case for an early-February cut; it expects March and May."]
    if ge(R, '2026-01-26'):
        V += ["Duda (23 Jan): both February and March cuts look likely."]
    if ge(R, '2026-01-29'):
        V += ["NBP board member Sobon (28 Jan): room for further cuts, month by month; Pekao (28 Jan) sees 3.25% possible."]
    V = V[:1] + V[-3:] if len(V) > 4 else V
    pricing = fra_s + " " + " ".join(V)
    if R < '2026-01-23':
        risk = (("February is now debated inside the MPC (" + ("Kotecki for; " + ", ".join(n for n, d in (("Wnorowski", '2026-01-19'), ("Tyrowicz", '2026-01-20'), ("Zarzecki", '2026-01-22')) if ge(R, d)) + " against" if ge(R, '2026-01-19') else "Glapiński excluded neither February nor March") + "): if the cut slips beyond March the front-end roll-down does not materialise, "
                + ("and global long-end sell-offs (UST/JGB, 20 Jan) hit the 10Y through the asset swap." if ge(R, '2026-01-21') else "and global long-end volatility (tariffs, Fed independence) hits the 10Y through the asset swap.")))
    else:
        risk = ("Strong December wages and industry cut the odds of a February move; the March projection is the gate. A hawkish projection (fiscal impulse ~7% of GDP deficit, 8.6% wages) "
                "would lift the front end; global long-end volatility and heavy supply weigh on the 10Y asset swap.")
    policy = dict(nbp_reference=4.0, next_mpc_label="MPC next: 3-4 Feb", pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = dict(v=2.4, m="Dec final (GUS, 15 Jan); Nov 2.5%" + ("; Dec core 2.7% (NBP, 16 Jan)" if ge(R, '2026-01-19') else "; Nov core 2.7%"))
    fiscal = ("2025 general-government deficit ~7.0% of GDP; 2026 budget deficit cap PLN 271.7bn, gross borrowing needs ~PLN 690bn"
              + ("; FinMin Domański (16 Jan): the 2025 central-budget deficit came in a dozen-plus billion below the PLN 288.8bn limit" if ge(R, '2026-01-19') else "")
              + ("; the President signed the 2026 budget on 19 Jan and referred it to the Constitutional Tribunal for follow-up review (the act is in force)" if ge(R, '2026-01-20') else "; the 2026 budget awaited the President's signature")
              + ("; Eurostat (22 Jan): general-government debt 58.1% of GDP at end-Q3 2025" if ge(R, '2026-01-23') else "") + ".")
    fin = {'2026-01-16': "~26% financed (12 Jan)", '2026-01-19': "~26% financed (12 Jan)", '2026-01-20': "~26% financed (12 Jan)", '2026-01-21': "~26% financed (12 Jan)",
           '2026-01-22': "~26% financed (12 Jan)", '2026-01-23': "~26% financed before the 22 Jan sale", '2026-01-26': "~28% financed after 22 Jan (MoF figure published 26 Jan)",
           '2026-01-27': "~28% financed (26 Jan)", '2026-01-28': "~28% financed (26 Jan)", '2026-01-29': "~28% financed before the 28 Jan sale", '2026-01-30': "~30% financed (29 Jan)"}[R]
    if R == '2026-01-26':
        fin = "~26% financed before the 22 Jan sale (MoF, 12 Jan; the post-auction figure was not yet published)"
    frisk = (f"Q1 2026 supply of PLN 75-100bn over 8 auctions; 2026 needs {fin}; "
             + ("a USD 10bn SEC shelf was filed on 20 Jan (published 21 Jan); " if ge(R, '2026-01-22') else "")
             + "Fitch (27 Feb) and Moody's (20 Mar) reviews with negative outlooks; Coface (20 Jan) flagged downgrade risk if the deficit path does not improve." if ge(R, '2026-01-21') else
             f"Q1 2026 supply of PLN 75-100bn over 8 auctions; 2026 needs {fin}; Fitch (27 Feb) and Moody's (20 Mar) reviews with negative outlooks.")
    base = ("The NBP cut six times in 2025 to 4.00% and held on 14 Jan; December CPI 2.4% y/y (final, 15 Jan)" + (", core 2.7%" if ge(R, '2026-01-19') else "")
            + "; the NBP projects 2.9% for 2026 (professional forecasters 2.6%); the March projection is the next policy gate. GDP grew 3.8% y/y in Q3"
            + ("; IMF (19 Jan) raised Poland's 2026 growth forecast to 3.5%" if ge(R, '2026-01-20') else "") + ". Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable.")
    wk = {
        '2026-01-16': "15 Jan: Glapiński's press conference pushed short-end POLGB yields lower in the afternoon and investors started pricing a February cut (Bank Pocztowy, PAP close). Abroad: US jobless claims 198k, Philly Fed 12.6; Brent fell 4.6% to ~$63 as Iran-strike fears eased; Fitch warned of European downgrades if the Greenland dispute splits NATO.",
        '2026-01-19': "16-18 Jan: POLGB yields fell sharply in the week on MPC easing signals and strong auction demand (PKO); the 36-week T-bill sold PLN 3.8bn at 3.645% (demand 5.85bn). Trump signalled Hassett will stay at the NEC, cutting the odds of two Fed cuts; on 17 Jan he announced 10% tariffs from 1 Feb (25% from 1 June) on eight European countries over Greenland.",
        '2026-01-20': "19 Jan: EU weighed EUR 93bn of counter-tariffs over Greenland; euro-area December HICP was revised to 1.9%; China Q4 GDP 4.5%. POLGB yields rose 1-8bp (PKO). The President signed and referred the budget (evening).",
        '2026-01-21': "20 Jan: 'sell America' - UST 10Y 4.27% (+5bp), the dollar -0.9%, gold at a record; Japan's 40Y yield above 4%. The Polish curve bull-steepened: the short end fell on February-cut bets while the 10Y rose back near 5.18% with global long ends (ING, 20 Jan); FRAs price just under three 25bp cuts in 2026 (PKO, 20 Jan). France adopted its budget revenue part via 49.3.",
        '2026-01-22': "21 Jan: Trump said at Davos he would not use force over Greenland and in the evening dropped the 1 Feb tariffs after a 'framework' with NATO; UK CPI 3.4% (3.3% expected). At home the 2Y POLGB fell to 3.57%, its lowest since February 2022, while the 10Y rose 2bp to 5.15% (PKO, 21 Jan); PLN swaps fell 2-3bp (Millennium, 21 Jan).",
        '2026-01-23': "22 Jan: December wages +8.6% y/y, industry +7.3%, construction +4.5%, PPI -2.5% - all stronger than expected; short FRAs rose 3-5bp (BNP TFI). The 22 Jan auction sold PLN 12.0bn (cover 1.43) plus 1.75bn additional. Abroad: US PCE in line, Q3 GDP revised to 4.4%; the ECB account showed no cuts priced and a hike seen beyond 2026.",
        '2026-01-26': "23-25 Jan: risk appetite returned after the tariff U-turn; the short end of the POLGB curve rose (PKO: 2Y 3.57, 5Y 4.49, 10Y 5.12 on 22 Jan). BoJ held at 0.75% (8-1); euro-area PMIs mixed; the French government survived no-confidence votes; US-Ukraine-Russia talks opened in Abu Dhabi. Domański (25 Jan): more arguments to keep the zloty.",
        '2026-01-27': "26 Jan: December retail sales +5.3% y/y (5.6% expected); M3 +10.4%; MoF: 2026 needs ~28% financed; 28 Jan offer published. Abroad: gold above $5,000, the dollar index at 96.97 (-2% in six sessions), Ifo 87.6; markets see the next Fed cut in June.",
        '2026-01-28': "27 Jan: registered unemployment 5.7%; December MPC vote 9-1 with Tyrowicz's 150bp hike motion rejected. MNB held at 6.50% ('careful and patient'); CNB's Frait said a slight cut could be discussed on 5 Feb; US consumer confidence 84.5 (91 expected); the dollar at its lowest since 2022.",
        '2026-01-29': "28 Jan: the last January auction sold PLN 12.0bn on 21.4bn demand (cover 1.78) plus 2.1bn additional; GPW Benchmark announced the 30 Jan index changes. The Fed held at 3.50-3.75% (10-2; Miran and Waller for a cut); Powell: policy near neutral, tariff-driven inflation; March cut odds ~12%; Brent ~$68.6.",
        '2026-01-30': "29 Jan: MoF says 2026 needs are ~30% financed; BGK sold PLN 1bn of FWA0931 (FWSZ); Poland's ESI rose to 103.2. Brent above $70 on US threats to Iran; gold fell over 5% intraday from its record after a tech sell-off. The 2025 GDP flash and the February supply plan are due on 30 Jan.",
    }[R]
    macro = dict(cpi=cpi, projection_text="NBP November 2025 projection: CPI 3.7% (2025), 2.9% (2026), 2.5% (2027); December 2025 CPI 2.4% y/y (final). The March 2026 projection is due with the March MPC meeting.",
                 fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + wk)
    # ---------------- calendar
    plan = ("MoF Q1 2026 financing plan (31 Dec 2025): 8 sale auctions for PLN 75-100bn, one switch auction, possible foreign issuance; January sales 9 Jan (done: PLN 13.7bn incl. additional sale), "
            "22 Jan (plan 8-13bn) and 28 Jan (7-12bn); EUR 3.25bn priced on 8 Jan.")
    if ge(R, '2026-01-19'):
        plan += " 16 Jan: 36-week T-bills PLN 3.8bn at 3.645%."
    if R in ('2026-01-21', '2026-01-22'):
        plan += " 22 Jan offer (MoF, 20 Jan): PLN 8-12bn in OK0128, WZ0930, PS0131, NZ0331, DS0432 (re-opened) and DS1035."
    if ge(R, '2026-01-22'):
        plan += " MoF filed a USD 10bn shelf prospectus with the US SEC (20 Jan)."
    o22, o28 = OPS['2026-01-22'], OPS['2026-01-28']
    y = lambda o, s: [l for l in o['lines'] if l['series'] == s][0]['avg_yield']
    if ge(R, '2026-01-23'):
        plan += (f" 22 Jan result: PLN {o22['total_sold_mn']/1000:.1f}bn sold vs {o22['total_demand_mn']/1000:.1f}bn demand (cover 1.43) plus {o22['additional_sale']['total_mn']/1000:.2f}bn additional (NZ0331 1.04bn, WZ0930 0.59bn); "
                 f"stop yields OK0128 {y(o22,'OK0128'):.3f}%, PS0131 {y(o22,'PS0131'):.3f}%, DS0432 {y(o22,'DS0432'):.3f}%, DS1035 {y(o22,'DS1035'):.3f}%.")
    if ge(R, '2026-01-27'):
        plan += " MoF (26 Jan): ~28% of 2026 needs financed."
    if R in ('2026-01-27', '2026-01-28'):
        plan += " 28 Jan offer (MoF, 26 Jan): PLN 8-12bn in OK0128, WZ0930, PS0131, NZ0331, DS1034 (re-opened) and DS1035."
    if ge(R, '2026-01-29'):
        plan += (f" 28 Jan result: PLN {o28['total_sold_mn']/1000:.1f}bn vs {o28['total_demand_mn']/1000:.1f}bn demand (cover 1.78) plus {o28['additional_sale']['total_mn']/1000:.2f}bn additional (DS1035 1.28bn, NZ0331 0.77bn); "
                 f"stop yields OK0128 {y(o28,'OK0128'):.3f}%, PS0131 {y(o28,'PS0131'):.3f}%, DS1034 {y(o28,'DS1034'):.3f}%, DS1035 {y(o28,'DS1035'):.3f}%. January wholesale sales ~PLN 41.6bn incl. additional sales.")
    if R == '2026-01-30':
        plan += " MoF (29 Jan): ~30% financed; February supply plan due 30 Jan. BGK sold PLN 1bn of FWA0931 for the Armed Forces Support Fund (29 Jan)."
    left = "22 and 28 Jan" if R <= '2026-01-22' else ("28 Jan" if R <= '2026-01-28' else "the February dates (plan due 30 Jan)")
    timing = ("Within each auction week of the Aug 2025-Jan 2026 sample, yields drifted lower into the auction (rally regime) and the auction-day close was the cheapest point relative to the preceding session, "
              f"so new buying is best executed at the auction-day close ({left}) rather than the day before. ")
    timing += ("January auctions have been absorbed with cover of 1.4-1.9x, so supply is not the binding constraint. " if ge(R, '2026-01-23') else "The 9 Jan auction cleared PLN 13.7bn with 1.86x cover. ")
    timing += ("For the front end the 3-4 Feb MPC is the next event: " + ("February is debated after Glapiński's dovish conference; " if R < '2026-01-23' else "strong December data pushed the consensus to a February hold; ")
               + "the March projection decides the cut timing.")
    ev = copy.deepcopy(F15['calendar']['events'])
    for e in ev:
        if e['date'] == '2026-01-22' and e['type'] == 'Auction' and R in ('2026-01-21', '2026-01-22'):
            e.update(title="MoF sale auction PLN 8-12bn", note="OK0128, WZ0930, PS0131, NZ0331, DS0432 (re-opened), DS1035.", source_date="MoF offer 20 Jan (via PAP)")
        if e['date'] == '2026-01-28' and e['type'] == 'Auction' and R in ('2026-01-27', '2026-01-28'):
            e.update(title="MoF sale auction PLN 8-12bn", note="OK0128, WZ0930, PS0131, NZ0331, DS1034 (re-opened), DS1035.", source_date="MoF offer 26 Jan (via PAP)")
        if e['date'] == '2026-01-30' and e['type'] == 'Index' and ge(R, '2026-01-29'):
            e.update(note="Communique (28 Jan): 1-3Y drops OK0127 (5 bonds, MD 1.81); 1-4Y drops OK0127, adds PS0130 (MD 2.56); TBSP keeps its 18 bonds (MD 3.76).", source_date="GPW Benchmark, 28 Jan")
        if e['date'] == '2026-02-04':
            e['note'] = ("February debated after Glapiński (15 Jan); March projection is the gate." if R < '2026-01-23' else "Consensus: hold; March cut base case after strong December data.")
    add = []
    if R <= '2026-01-22':
        add.append(dict(date='2026-01-22', type='Data', title='GUS December wages, industry, PPI, construction', note='', source_date='GUS calendar'))
    if R <= '2026-01-26':
        add.append(dict(date='2026-01-26', type='Data', title='GUS December retail sales', note='', source_date='GUS calendar'))
    add.append(dict(date='2026-01-30', type='Data', title='GUS 2025 GDP flash' + ('; MoF February supply plan' if ge(R, '2026-01-27') else ''), note='', source_date='GUS calendar' + ('; PAP week-ahead 26 Jan' if ge(R, '2026-01-27') else '')))
    ev = sorted([e for e in ev if not (e['type'] == 'Data' and e['date'] == '2026-01-15')] + add, key=lambda e: e['date'])
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core
    cp = copy.deepcopy(F15['core_policy'])
    tail = ("; Glapiński (15 Jan): terminal ~3.5%" if R == '2026-01-16' else "; February cut debated inside the MPC" if R < '2026-01-23' else "; strong December data: March base case")
    cp['Poland'].update(pricing=f"FRAs ~{cuts}bp of cuts within 12M ({lab} close){tail}", next="3-4 Feb 2026")
    us = {'2026-01-16': "investors price at least two cuts by end-2026 (LSEG, 15 Jan)",
          '2026-01-19': "fewer cuts priced after Trump signalled Hassett stays at the NEC (16 Jan); UST 2Y 3.61%"}.get(R)
    if not us:
        us = ("FedWatch (19 Jan): 95% hold in January, ~21% chance of a cut by March" if R <= '2026-01-22' else
              "most economists see a hold through Q1 (Reuters poll, 21 Jan); ~21% for March (FedWatch, 19 Jan)" if R == '2026-01-23' else
              "next cut seen in June (PAP, Goldman, 26 Jan); 99% hold priced for 28 Jan" if R <= '2026-01-28' else
              "held 28 Jan (10-2, Miran and Waller for a cut); March cut odds ~12% (FedWatch, 28 Jan), next cut seen in June")
    cp['United States']['pricing'] = us
    if ge(R, '2026-01-29'):
        cp['United States'].update(last="held 28 Jan (last cut -25bp 10 Dec 2025)", next="17-18 Mar 2026", stance="On hold, easing bias")
    if ge(R, '2026-01-23'):
        cp['Euro area']['pricing'] = "no cuts priced for 2026; next move seen as a hike beyond 2026 (ECB account, 22 Jan)"
    cp['United Kingdom']['pricing'] = ("46bp of cuts priced for 2026 (15 Jan)" if R < '2026-01-22' else "one, possibly two cuts priced for 2026 (21 Jan, after CPI 3.4%)")
    if ge(R, '2026-01-28'):
        cp['Czechia']['pricing'] = "Frait (27 Jan): a slight cut could be discussed on 5 Feb"
        cp['Hungary'].update(last="held 27 Jan (6.50%, unanimous)", next="Feb 2026", pricing="ING (26 Jan): two cuts priced in Q1; MNB: 'careful and patient'")
    cc = copy.deepcopy(F15['core_cpi'])
    cc['Poland'] = dict(v=2.4, m="Dec final")
    if ge(R, '2026-01-20'):
        cc['Euro area'] = dict(v=1.9, m="Dec final (core 2.3)")
    if ge(R, '2026-01-22'):
        cc['United Kingdom'] = dict(v=3.4, m="Dec")
    rel = ["GUS 15 Jan", "Eurostat 7" + ("/19" if ge(R, '2026-01-20') else "") + " Jan"] + (["ONS 21 Jan"] if ge(R, '2026-01-22') else []) + ["CZSO 13 Jan", "KSH 13 Jan", "BLS 13 Jan"] + (["MNB 27 Jan"] if ge(R, '2026-01-28') else []) + (["FOMC 28 Jan"] if ge(R, '2026-01-29') else [])
    note = F15['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off: " + ", ".join(rel) + "."
    good = v.get('cds5y') and v.get('pl_bund_10y') and not v.get('flags')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {lab} close)." if good else
           f" (Erste's CDS/spread table for {lab} looked stale or inconsistent, so it is not quoted.)")
    regime = (f"Regime: the NBP paused at 4.00% with ~{cuts}bp more priced, the ECB is done at 2.00% (a hike is the next move in market pricing), "
              + ("the Fed held on 28 Jan" if ge(R, '2026-01-29') else "the Fed is on hold into June") + ", the BoE eases gradually, the CNB and MNB are on hold.")
    glob = {'2026-01-16': " UST 10Y 4.16%, Bund 2.82% (15 Jan).",
            '2026-01-19': " Greenland tariff threat (17 Jan): 10% on eight European countries from 1 Feb.",
            '2026-01-20': " The EU weighed EUR 93bn of counter-tariffs (19 Jan).",
            '2026-01-21': " 'Sell America' (20 Jan): UST 10Y 4.27%, the dollar -0.9%, Japan's long end above 4%: a global term-premium shock hitting long ends, Poland included.",
            '2026-01-22': " Tariff threat withdrawn on 21 Jan evening (Davos 'framework').",
            '2026-01-23': " Risk-on after the tariff U-turn: UST 10Y 4.26%, Bund 2.88% (22 Jan).",
            '2026-01-26': " OAT-Bund 58bp, BTP-Bund 60bp at the 23 Jan close; France survived no-confidence votes.",
            '2026-01-27': " Dollar index 96.97 (-2% in six sessions) and gold above $5,000 (26 Jan).",
            '2026-01-28': " MNB held at 6.50%; CNB opening to a cut (27 Jan).",
            '2026-01-29': " FOMC held with two dissents for a cut (28 Jan); UST 10Y ~4.25%.",
            '2026-01-30': " Brent above $70 on Iran (29 Jan); risk-off after a tech sell-off lifted Treasuries."}[R]
    core_text = regime + spr + glob
    tk = list(Q15['takeaways_html'])
    if R == '2026-01-30':
        tk[2] += " BGK also sold PLN 1bn of FWA0931 for the Armed Forces Support Fund on 29 Jan."
    au = {"MoF auctions & switch results": dict(as_of=("28 Jan 2026 auction + additional sale" if ge(R, '2026-01-29') else "22 Jan 2026 auction + additional sale" if ge(R, '2026-01-23') else "9 Jan 2026 auction; 16 Jan T-bills" if ge(R, '2026-01-19') else "9 Jan 2026 auction"),
                                            published=("28 Jan 2026" if ge(R, '2026-01-29') else "22 Jan 2026" if ge(R, '2026-01-23') else "9-16 Jan 2026"),
                                            source="MoF wholesale-bond database (only rows whose release on the day is confirmed by PAP); MoF/PAP communiques", note="No new series, switch or buyback in 15-29 Jan."),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of="14 Jan 2026 decision; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1] if '-' in WIN[R] else "<= " + WIN[R], source="NBP/MPC, Bloomberg/PAP interviews", note=""),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1] if '-' in WIN[R] else WIN[R]}", source="PKO, Erste/Santander, Millennium, ING, Pekao, mBank, Deutsche Bank Polska, Credit Agricole, BNP, BPS; PAP", note="Only commentary published by the info cut-off.")}
    if ge(R, '2026-01-29'):
        au["Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)"] = dict(note=("Portfolio in force until the 30 Jan close is the 30 Dec 2025 one. The 30 Jan communique (scheduled for 28 Jan, holdings 27 Jan) is quoted in text only: the PDF now served was regenerated on 2 Feb 2026; "
                                                                   "its unit changes match MoF settlements to 26 Jan."))
    nfa = dict(input=f"New facts {WIN[R]}", as_of=WIN[R], published=WIN[R], source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, MNB/CNB, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    d = dict(policy={'nbp_reference': 4.0, 'last_change': "3 Dec 2025 (-25bp); held 14 Jan 2026", 'next_mpc': "2026-02-03/04"},
             facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
             quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = []
    for dd in ('2026-01-22', '2026-01-28'):
        o = OPS[dd]
        if C >= dd:
            adds += [dict(date=dd, settle=o.get('settlement'), type='S', op='AS', lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l['demand_mn'], avg_yld=l['avg_yield'], price=l['avg_price']) for l in o['lines']]),
                     dict(date=dd, settle=o.get('settlement'), type='S', op='OB', lines=[dict(series=k, sold=x, demand=None, avg_yld=None, price=None) for k, x in o['additional_sale']['lines'].items() if x])]
    if adds:
        d['mof_ops_add'] = adds
    OUT[R] = d
json.dump(OUT, open(SP / 'jan2/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
