"""Per-day point-in-time narrative for 7-15 Jan 2026 reports -> facts_days.json (merged into the day specs)."""
import json, copy, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user/2b986bc3-1107-5358-8c0f-f544109c09bc/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
F5 = json.load(open(REPO / 'data/snapshots/2026-01-05/facts.json'))
Q5 = json.load(open(REPO / 'data/snapshots/2026-01-05/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_jan_fix/fixings.json'))['by_date']
CV = json.load(open(SP / 'agent_jan_curves/curves.json'))
DAYS = ['2026-01-07', '2026-01-08', '2026-01-09', '2026-01-12', '2026-01-13', '2026-01-14', '2026-01-15']
CUT = dict(zip(DAYS, ['2026-01-05', '2026-01-07', '2026-01-08', '2026-01-09', '2026-01-12', '2026-01-13', '2026-01-14']))
WIN = dict(zip(DAYS, ['5-6 Jan 2026', '7 Jan 2026', '8 Jan 2026', '9-11 Jan 2026', '12 Jan 2026', '13 Jan 2026', '14 Jan 2026']))
LBL = dict(zip(DAYS, ['5 Jan', '7 Jan', '8 Jan', '9 Jan', '12 Jan', '13 Jan', '14 Jan']))
def ge(R, d): return R >= d

def fra_of(R):
    return CV[R]['alt_erste_hdr_0601']['fra'] if R == '2026-01-07' else CV[R]['fra']

OUT = {}
for R in DAYS:
    C = CUT[R]; w = FX[C]['wibor']; fra = fra_of(R); lab = LBL[R]
    cuts = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    fra_s = f"FRAs at the {lab} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price roughly {cuts}bp of NBP cuts within 12 months."
    # ---------- policy
    views = ["The NBP survey of professional forecasters (2 Jan) sees an average reference rate of 3.69% in 2026."]
    if R == '2026-01-07':
        views += ["Credit Agricole (5 Jan): the market prices three incomplete cuts by end-2026; Erste/Santander (5 Jan) expects a hold for a while, then cuts in March and May."]
    if ge(R, '2026-01-08'):
        views += ["PKO (7 Jan): derivatives price a 3.25% reference rate by mid-2026; Deutsche Bank Polska (7 Jan) expects a January hold with core CPI at ~2.8%."]
    if ge(R, '2026-01-09'):
        views += ["MPC member Dąbrowski (Bloomberg, 8 Jan): a 50% chance of a January cut after the low December CPI, though he leans to a pause, and room for another 50bp by mid-2026; Tyrowicz (8 Jan): CPI may stay near target for the first time in this episode."]
    if ge(R, '2026-01-13'):
        views += ["PKO (12 Jan): only about half of a 25bp January cut is priced; Credit Agricole and Santander expect a hold, Goldman Sachs a cut."]
    if ge(R, '2026-01-14'):
        views += ["Parkiet poll (13 Jan): 3 of 19 teams expect a January cut, consensus two 25bp cuts in H1 2026; ING (13 Jan) puts a cut at 35% and sees a 3.25% terminal rate; MNI's survey shows most sell-side expecting a hold."]
    if R == '2026-01-15':
        views = ["The MPC held all rates on 14 Jan (reference 4.00%). The statement keeps decisions data-dependent, drops energy prices from the list of inflation risks and calls the demand recovery 'expected'. Glapiński speaks on 15 Jan at 15:00."] + views[:1] + [
            "Post-decision views (14 Jan): ING sees the next cut in March with the new projection and at least three cuts in 2026 to 3.25%; Erste expects 25bp in March and another in Q2 to 3.50%; PKO expects March and 3.50% in two quick steps with Q1 CPI near 2%."]
    pricing = fra_s + " " + " ".join(views)
    if R == '2026-01-07':
        risk = F5['policy']['risk_text']
    elif R in ('2026-01-08',):
        risk = ("MPC members ruled out a January cut in December (Kotecki 10 Dec; Wnorowski and Kotecki 16 Dec). If cuts are pushed out, front-end roll-down does not materialise; "
                "PKO (7 Jan) notes that 2Y below 3.75% and 10Y near 5.10% are levels it expected only at end-Q1, and Friday's PLN 8-12bn auction limits the room for further falls.")
    elif R != '2026-01-15':
        risk = ("The January decision is a coin-toss for some members (Dąbrowski, 8 Jan) while most economists expect a hold: a hold would lift short FRAs/IRS a few bp (Millennium, 12-13 Jan), "
                "a cut would extend the front-end rally (PKO). If cuts are pushed beyond March, front-end roll-down does not materialise; heavy Q1 supply can widen asset swaps (Millennium, 9 Jan).")
    else:
        risk = ("After the 14 Jan hold the next cut is expected in March with the new projection: a slower path (core CPI ~2.8%, the 'expected' demand recovery) would lift the front end; "
                "a quick move to 3.50% (PKO) would extend the rally. Heavy Q1 supply can widen asset swaps (Millennium, 9 Jan).")
    policy = dict(nbp_reference=4.0, next_mpc_label=("MPC next: 3-4 Feb" if R == '2026-01-15' else "MPC next: 13-14 Jan"), pricing_text=pricing, risk_text=risk)
    # ---------- macro
    fiscal = F5['macro']['fiscal_text']
    if ge(R, '2026-01-12'):
        fiscal = ("2025 general-government deficit ~7.0% of GDP (MoF notified PLN 271bn; 4Q-rolling 7.0% after Q3 per Erste, 12 Jan)" if ge(R, '2026-01-13') else "2025 general-government deficit ~6.9% of GDP (MoF plan)") + \
                 "; the Sejm completed the 2026 budget on 9 Jan (deficit cap PLN 271.7bn, gross borrowing needs ~PLN 690bn); presidential vetoes cost ~PLN 1.8bn in 2026 (Neneman, 9 Jan); budget cash PLN 133.8bn at end-Dec (MoF, 9 Jan)."
        if ge(R, '2026-01-13'):
            fiscal += " The President may send the budget to the Constitutional Tribunal (no veto right); the government would then run on its draft (Domański, 12 Jan)."
    frisk = F5['macro']['fiscal_risk_text']
    if ge(R, '2026-01-12'):
        frisk = ("Q1 2026 supply of PLN 75-100bn over 8 auctions: PLN 13.7bn sold on 9 Jan, next 22 Jan (8-13bn) and 28 Jan (7-12bn); "
                 + ("MoF is considering JPY, CHF and USD issues (14 Jan); " if R == '2026-01-15' else "") + "Fitch (27 Feb) and Moody's (20 Mar) reviews with negative outlooks.")
    base = ("The NBP cut six times in 2025 to 4.00% (last on 3 Dec); CPI fell to 2.4% in December (flash, 31 Dec; final on 15 Jan" + (", consensus 2.4% y/y, core ~2.8%" if ge(R, '2026-01-14') else ", core estimated ~2.8% by Erste") + "), the NBP projects 2.9% for 2026 "
            "(professional forecasters, 2 Jan: 2.6%). Manufacturing PMI fell to 48.5 in December (2 Jan). GDP grew 3.8% y/y in Q3. Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable.")
    if R == '2026-01-15':
        base = base.replace("The NBP cut six times in 2025 to 4.00% (last on 3 Dec)", "The NBP cut six times in 2025 to 4.00% and held on 14 Jan")
    wk = {
        '2026-01-07': ("Since 2 Jan: bank dailies (5 Jan) expect POLGBs to keep their relative strength after the sub-target December CPI (PKO), with IRS 2Y/5Y/10Y down 6-7bp in the week to 2 Jan (Credit Agricole). "
                       "6 Jan was a Polish holiday; abroad, US ISM manufacturing fell to 47.9 (5 Jan; 48.4 expected) and German December CPI surprised lower (1.8% y/y, HICP 2.0%; 6 Jan). "
                       "Venezuela after the 3 Jan US operation was shrugged off by markets; the 6 Jan Paris declaration on Ukraine has the UK and France pledging troops after a ceasefire."),
        '2026-01-08': ("On 7 Jan POLGBs rallied 5-9bp, led by the front end, while swaps barely moved (Erste); MoF announced the 9 Jan offer (PLN 8-12bn incl. the new 5Y POLSTR floater NZ0331). "
                       "Abroad: euro-area flash HICP 2.0% (core 2.3%) and an ECB hold priced through 2026; US JOLTS 7.15m (7.65m expected), ADP +41k, ISM services 54.4; UST 10Y 4.14%, Bund 2.81% (7 Jan). "
                       "FWSZ spent PLN 51.4bn in 2025, ~20bn below plan, possibly shifting the defence impulse into 2026 (Erste, 7 Jan)."),
        '2026-01-09': ("8 Jan: MPC member Dąbrowski put a January cut at 50%; MoF priced EUR 3.25bn (5Y 2.964%, MS+43; 10Y 3.739%, MS+83; books over EUR 12bn); swaps rose 3-5bp (Millennium). "
                       "Poland's December ESI rose to 100.0 but consumer inflation expectations jumped (35.3 from 27.9). Abroad: German factory orders +5.6% m/m (8 Jan), Brent +3.4% to $62 on supply worries; "
                       "the US $200bn MBS purchase order came late on 8 Jan; US December payrolls are due on 9 Jan."),
        '2026-01-12': ("9 Jan: the MoF auction sold PLN 12.0bn (demand 22.3bn) plus 1.69bn in the additional sale, DS1035 at 5.121%; US payrolls +50k (about 70k expected), unemployment 4.4%, January Fed cut odds fell to ~3%; "
                       "no Supreme Court tariff ruling. Prefinancing of 2026 needs at end-2025 was ~21% (final), budget cash PLN 133.8bn. The Sejm finished the 2026 budget. "
                       "Over the weekend: a Russian missile strike near Lviv; EU states approved the Mercosur deal; the French Assembly committee rejected the 2026 budget."),
        '2026-01-13': ("12 Jan: news of DOJ subpoenas to Fed Chair Powell triggered a 'sell America' move (dollar down, gold at a record, UST 10Y 4.20%); Trump announced a 25% tariff on countries trading with Iran; "
                       "ECB's Villeroy called a 2026 hike 'fanciful'. At home: BGK sold PLN 3.7bn of FPC (demand 7.05bn) plus 0.7bn; MoF says 2026 needs are ~26% financed after the 9 Jan auction and the EUR deal; "
                       "POLGB yields rose 1-2bp with late selling (PKO)."),
        '2026-01-14': ("13 Jan: US December core CPI 0.2% m/m (2.6% y/y vs 2.7% expected) left a Fed cut by June almost fully priced; Hungary CPI 3.3% (above the MNB projection), Czech CPI 2.1%; Brent rose ~2.5% on Iran. "
                       "Poland's November current account showed a EUR 460m deficit (EUR 500m surplus expected); POLGB yields fell 3-4bp 'rather unexpectedly' (Erste). "
                       "The 2026 budget reached the President on 13 Jan."),
        '2026-01-15': ("14 Jan: the MPC held (see policy). Abroad: US retail sales +0.6%, PPI 3.0% y/y; China's December exports +6.6% (3.0% expected); Fed's Kashkari said it is 'way too soon' to cut; "
                       "Iran strike fears lifted Brent to $66.5 (a three-month high) before Trump's comments eased them; UST 10Y 4.13%, Bund 2.81%; Greenland talks ended in 'fundamental disagreement'. "
                       "MoF is considering JPY, CHF and USD issues (14 Jan)."),
    }[R]
    street = "Street views (December): PKO 1Q26 forecast 2Y 3.75 / 5Y 4.50 / 10Y 5.10" + (" (reached by 7 Jan, PKO)" if ge(R, '2026-01-08') else "") + "; Santander expects higher yields in Q1 on supply and cut repricing; ING says early-2026 trading follows MoF's Q1 issuance."
    macro = dict(projection_text=F5['macro']['projection_text'], fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + wk + " " + street)
    # ---------- calendar
    plan = ("MoF Q1 2026 financing plan (31 Dec 2025): 8 sale auctions for PLN 75-100bn, one switch auction, possible foreign issuance. January: sale auctions on 9 Jan (PLN 7-12bn), "
            "22 Jan (8-13bn) and 28 Jan (7-12bn); no switch auction in January; 36-week T-bill auction on 16 Jan (PLN 2-4bn). 2026 gross borrowing needs ~PLN 690bn. BGK: FPC to issue domestically in 2026 (up to PLN 18.5bn).")
    if R == '2026-01-07':
        plan += " Series for the 9 Jan auction had not been announced by 6 Jan."
    if ge(R, '2026-01-08') and R < '2026-01-12':
        plan += " 9 Jan offer (MoF, 7 Jan): PLN 8-12bn in OK0128, PS0130, WZ0930, PS0131, NZ0331 (new 5Y compounded-POLSTR floater, 25 Mar 2031), DS1033 and DS1035."
    if ge(R, '2026-01-09'):
        plan += " MoF priced EUR 3.25bn on 8 Jan (EUR 2bn Jan-2031 at 2.964%, MS+43; EUR 1.25bn Jun-2036 at 3.739%, MS+83)."
    if R == '2026-01-09':
        plan += " BGK announced an FPC auction for 12 Jan (FPC0229, FPC0231, FPC0332, FPC0235; min PLN 1.0bn)."
    if ge(R, '2026-01-12'):
        plan += (" 9 Jan result: PLN 12.0bn sold vs 22.3bn demand (cover 1.86) plus 1.69bn additional sale (DS1035 1.17bn); stop yields OK0128 3.678%, PS0130 4.258%, PS0131 4.504%, DS1033 4.851%, DS1035 5.121%; "
                 "new NZ0331 PLN 1.26bn at 95.20. Prefinancing at end-2025 was ~21% (final).")
    if R == '2026-01-12':
        plan += " BGK FPC auction today (12 Jan: FPC0229, FPC0231, FPC0332, FPC0235; min PLN 1.0bn)."
    if ge(R, '2026-01-13'):
        plan += " MoF (12 Jan): 2026 needs ~26% financed. BGK sold PLN 3.73bn of FPC (demand 7.05bn) plus 0.71bn on 12 Jan. The 22 Jan offer had not been published by " + WIN[R].split(' ')[0].split('-')[-1] + " Jan."
    dates = "9, 22, 28 Jan" if R < '2026-01-12' else "22, 28 Jan"
    timing = ("Within each auction week of the Aug 2025-Jan 2026 sample, yields drifted lower into the auction (rally regime) and the auction-day close was the cheapest point relative to the preceding session, "
              f"so new buying is best executed at the auction-day close ({dates}) rather than the day before. ")
    if R < '2026-01-12':
        timing += "January supply is front-loaded (PLN 22-37bn across three auctions) after only ~21-23% pre-financing. "
    else:
        timing += "The 9 Jan auction cleared PLN 13.7bn with 1.86x cover, so supply is being absorbed; 22 and 28 Jan remain (PLN 15-25bn). "
    if R < '2026-01-09':
        timing += "For the front end the 13-14 Jan MPC is the event: members pre-announced no January cut, so a hold is the base case; the December final CPI (15 Jan) and the February/March meetings drive the cut timing."
    elif R < '2026-01-15':
        timing += "For the front end the 13-14 Jan MPC is the event: a hold is the consensus, but Dąbrowski's 50% (8 Jan) means a cut is partly priced" + (" (about half, PKO 12 Jan)" if ge(R, '2026-01-13') else "") + "; the December final CPI (15 Jan) and the March projection drive the timing."
    else:
        timing += "After the 14 Jan hold the front end is driven by the December final CPI (15 Jan, 10:00), Glapiński's press conference (15 Jan, 15:00) and the March projection."
    ev = [e for e in copy.deepcopy(F5['calendar']['events']) if e['date'] != '2026-01-06']
    for e in ev:
        if e['date'] == '2026-01-09' and ge(R, '2026-01-08'):
            e.update(title="MoF sale auction PLN 8-12bn", note="OK0128, PS0130, WZ0930, PS0131, NZ0331 (new), DS1033, DS1035.", source_date="MoF offer 7 Jan (via PAP)")
        if e['date'] == '2026-01-14':
            e['note'] = ("Members ruled out a January cut in December; Dąbrowski (8 Jan): 50% chance." if ge(R, '2026-01-09') else e['note']) + (" Parkiet poll: 3 of 19 expect a cut." if ge(R, '2026-01-14') else "")
        if e['date'] == '2026-01-22':
            e['note'] = "Plan: OK0128, WZ0930, PS0131, NZ0331, DS1035, possibly IZ; offer 2 days before."; e['source_date'] = 'MoF January plan, 31 Dec 2025 (NZ0331 issue letter 22 Dec 2025)'
    add = [dict(date='2026-01-09', type='Data', title='US December payrolls', note='', source_date='BLS calendar'),
           dict(date='2026-01-13', type='Data', title='US December CPI', note='', source_date='BLS calendar'),
           dict(date='2026-01-15', type='Data', title='GUS final December CPI (10:00)', note='Flash 2.4% y/y; consensus 2.4%, core ~2.8% (DB, 13 Jan).' if ge(R, '2026-01-14') else 'Flash 2.4% y/y.', source_date='GUS calendar'),
           dict(date='2026-01-16', type='Auction', title='MoF 36-week T-bill auction PLN 2-4bn', note='', source_date='MoF January plan, 31 Dec 2025')]
    if ge(R, '2026-01-09'):
        add.append(dict(date='2026-01-12', type='Auction', title='BGK FPC auction (FPC0229, FPC0231, FPC0332, FPC0235)', note='Minimum PLN 1.0bn.', source_date='BGK via PAP, 8 Jan'))
    if R == '2026-01-15':
        add.append(dict(date='2026-01-15', type='MPC', title='Glapiński press conference (15:00)', note='After the 14 Jan hold.', source_date='NBP, 14 Jan'))
    ev = sorted(ev + add, key=lambda e: e['date'])
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------- core
    cp = copy.deepcopy(F5['core_policy'])
    cp['Poland']['pricing'] = f"FRAs ~{cuts}bp of cuts within 12M ({lab} close)" + ("; about half a January cut priced (PKO, 12 Jan)" if ge(R, '2026-01-13') and R < '2026-01-15' else "") + ("; banks see the next cut in March" if R == '2026-01-15' else "")
    if R == '2026-01-15':
        cp['Poland'].update(last="held 14 Jan (last cut -25bp 3 Dec 2025)", next="3-4 Feb 2026", stance="Pause, data-dependent")
    us = {'2026-01-07': "FedWatch (5 Jan): 83% hold in January, ~44% chance of a cut by March",
          '2026-01-08': "FedWatch (5 Jan): 83% hold in January, ~44% chance of a cut by March",
          '2026-01-09': "at least two 25bp cuts priced for 2026 (8 Jan); ~88% hold in January",
          '2026-01-12': "after payrolls (9 Jan): ~3% chance of a January cut, ~32% by March; next cut fully priced only by June",
          '2026-01-13': "~3% January / ~32% March (FedWatch, 9 Jan); after the Powell subpoena news JPMorgan sees no cut in 2026 (12 Jan)",
          '2026-01-14': "a cut by June almost fully priced after the soft core CPI (13 Jan); ~5% for January",
          '2026-01-15': "~5% January, ~26% by March, a cut by June almost fully priced (13-14 Jan)"}[R]
    cp['United States']['pricing'] = us
    if ge(R, '2026-01-08'):
        cp['Euro area']['pricing'] = "Hold at 2% priced through 2026 (7 Jan, after the flash HICP)" + ("; Villeroy (12 Jan): a 2026 hike is 'fanciful'" if ge(R, '2026-01-13') else "")
    if ge(R, '2026-01-12'):
        cp['Czechia']['pricing'] = "flat PRIBOR curve; CNB minutes (9 Jan): 6-0 hold, all options open"
    if ge(R, '2026-01-14'):
        cp['Hungary']['pricing'] = "BUBOR curve: mild easing priced; MNB (13 Jan): Dec CPI above projection, no January change"
    if R == '2026-01-15':
        cp['United Kingdom']['pricing'] = "close to two more cuts priced for 2026 (14 Jan)"
    cc = copy.deepcopy(F5['core_cpi'])
    if ge(R, '2026-01-08'):
        cc['Euro area'] = dict(v=2.0, m="Dec flash (core 2.3)"); cc['Czechia'] = dict(v=2.1, m="Dec flash")
    if ge(R, '2026-01-14'):
        cc['United States'] = dict(v=2.7, m="Dec (core 2.6)"); cc['Czechia'] = dict(v=2.1, m="Dec final"); cc['Hungary'] = dict(v=3.3, m="Dec (core 3.8)")
    note = F5['core_policy_note'] + (" Later releases used where published by the info cut-off: Eurostat flash HICP 7 Jan, CZSO 7/13 Jan, KSH 13 Jan, BLS 13 Jan." if ge(R, '2026-01-08') else "")
    v = CV[R]
    spr = "" if R == '2026-01-07' else (f" Poland's 5Y CDS was {v['cds5y']}bp" + (f" and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {lab} close; ~10bp less here on DS1035 vs the Bundesbank fitted 10Y)." if v.get('pl_bund_10y') and not v.get('flags') else f" (Erste, {lab} close; its CDS/spread table looked stale)."))
    regime = ("Regime: the NBP paused at 4.00% " + ("and held again on 14 Jan " if R == '2026-01-15' else "") + f"with ~{cuts}bp more priced, the ECB is done at 2.00%, the Fed and BoE are easing gradually, the CNB and MNB are on hold.")
    glob = {'2026-01-07': " German December inflation surprised lower (6 Jan) and US ISM manufacturing fell to 47.9 (5 Jan).",
            '2026-01-08': " Euro-area December HICP 2.0% (core 2.3%) on 7 Jan; UST 10Y 4.14%, Bund 2.81%.",
            '2026-01-09': " Poland priced EUR 3.25bn on 8 Jan at MS+43/+83bp: in EUR the curve trades well inside the PLN asset-swap levels.",
            '2026-01-12': " US payrolls +50k (9 Jan) pushed the next Fed cut out to June; OAT-Bund 66bp, BTP-Bund 64bp (9 Jan closes).",
            '2026-01-13': " The Powell subpoena news (12 Jan) weakened the dollar and steepened the UST curve; a Fed-independence premium is a new risk for the USD leg.",
            '2026-01-14': " Soft US core CPI (13 Jan); Hungary's December CPI 3.3% came in above the MNB projection.",
            '2026-01-15': " Iran risk lifted Brent to $66.5 on 14 Jan; UST 10Y 4.13%, Bund 2.81%."}[R]
    core_text = regime + spr + glob
    # ---------- quasi takeaways (supply bullet)
    tk = list(Q5['takeaways_html'])
    if R == '2026-01-09' or R == '2026-01-12':
        tk[2] = ("<b>Supply:</b> BGK announced an FPC auction for 12 Jan (FPC0229, FPC0231, FPC0332, FPC0235; minimum PLN 1.0bn, 8 Jan), the first of 2026 under a plan of up to PLN 18.5bn (24 Sep 2025). "
                 "Expect secondary prints to cheapen into the auction; buy there rather than on Catalyst.")
    if ge(R, '2026-01-13'):
        tk[2] = ("<b>12 Jan BGK auction:</b> PLN 3.73bn sold against 7.05bn demand, plus 0.71bn in the additional sale (~PLN 4.4bn, about a quarter of the 2026 FPC plan of up to 18.5bn); per-series levels were not found. "
                 "The 1.9x cover shows real-money demand for guaranteed paper at these spreads.")
    # ---------- audit
    au = {}
    if ge(R, '2026-01-12'):
        au["MoF auctions & switch results"] = dict(as_of="9 Jan 2026 auction + additional sale; EUR deal 8 Jan", published="8-9 Jan 2026",
                                                    source="MoF wholesale-bond database (9 Jan rows only, confirmed by PAP 9 Jan); MoF EUR pricing note 8 Jan", note="No switch or buyback in 5-14 Jan.")
    if R == '2026-01-15':
        au["NBP rates, MPC comments, 2026 MPC schedule"] = dict(as_of="14 Jan 2026 decision", published="14 Jan 2026 (14:37 decision, 16:00 statement)", source="NBP/MPC via PAP", note="Glapiński's 15 Jan press conference is after the report time.")
    au["Bank views"] = dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1] if '-' in WIN[R] else WIN[R]}", source="PKO, Erste/Santander, Millennium, ING, Deutsche Bank Polska, Credit Agricole, BPS dailies/weeklies; PAP", note="Only commentary published by the info cut-off.")
    nfa = dict(input=f"New facts {WIN[R]}", as_of=WIN[R], published=WIN[R],
               source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, Eurostat, BLS, CME FedWatch, CZSO/KSH, bank research", note="Facts placed in the window they were first published; release times from PAP summaries are upper bounds.")
    OUT[R] = dict(policy={'nbp_reference': 4.0, 'last_change': "3 Dec 2025 (-25bp, sixth cut of 2025)" + ("; held 14 Jan 2026" if R == '2026-01-15' else ""),
                          'next_mpc': "2026-02-03/04" if R == '2026-01-15' else "2026-01-13/14"},
                  facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc},
                             core_policy_note=note, core_text=core_text),
                  quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    if ge(R, '2026-01-12'):
        o = json.load(open(SP / 'agent_jan_plfacts/facts.json'))['mof_ops'][0]
        OUT[R]['mof_ops_add'] = [
            dict(date='2026-01-09', settle='2026-01-13', type='S', op='AS', lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l['demand_mn'], avg_yld=l['avg_yield'], price=l['avg_price']) for l in o['lines']]),
            dict(date='2026-01-09', settle='2026-01-13', type='S', op='OB', lines=[dict(series=k, sold=v, demand=None, avg_yld=None, price=None) for k, v in o['additional_sale']['lines'].items() if v])]
json.dump(OUT, open(SP / 'jan/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', {R: len(json.dumps(v)) for R, v in OUT.items()})
