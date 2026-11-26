"""Per-day point-in-time narrative for 2-27 Feb 2026 reports -> feb/facts_days.json (merged into the day specs)."""
import json, copy, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user/2b986bc3-1107-5358-8c0f-f544109c09bc/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
F30 = json.load(open(REPO / 'data/snapshots/2026-01-30/facts.json'))
Q30 = json.load(open(REPO / 'data/snapshots/2026-01-30/quasi_inputs.json'))
FX = json.load(open(SP / 'agent_feb_fix/fixings.json'))['by_date']
CV = {**json.load(open(SP / 'agent_feb_curves1/curves.json')), **json.load(open(SP / 'agent_feb_curves2/curves.json'))}
OPS = {}
for h in ('agent_feb_plfacts1', 'agent_feb_plfacts2'):
    for o in json.load(open(SP / h / 'facts.json'))['mof_ops']:
        if isinstance(o, dict) and o.get('type') == 'sale':
            OPS[o['date']] = o
RS = ['02', '03', '04', '05', '06', '09', '10', '11', '12', '13', '16', '17', '18', '19', '20', '23', '24', '25', '26', '27']
DAYS = [f'2026-02-{d}' for d in RS]
CUTS = ['2026-01-30'] + DAYS[:-1]
WINS = ['30 Jan-1 Feb', '2 Feb', '3 Feb', '4 Feb', '5 Feb', '6-8 Feb', '9 Feb', '10 Feb', '11 Feb', '12 Feb', '13-15 Feb', '16 Feb', '17 Feb', '18 Feb', '19 Feb',
        '20-22 Feb', '23 Feb', '24 Feb', '25 Feb', '26 Feb']
CUT, WIN = dict(zip(DAYS, CUTS)), dict(zip(DAYS, WINS))
ge = lambda R, d: R >= '2026-02-' + d if len(d) == 2 else R >= d
def lab(C):
    return f"{int(C[8:])} {'Jan' if C[5:7] == '01' else 'Feb'}"

def y(o, s):
    l = [l for l in o['lines'] if l['series'] == s]
    return l[0]['avg_yield'] if l else None

def res(d):
    o = OPS[d]; a = o.get('additional_sale') or {}
    return o['total_sold_mn'] / 1000, o['total_demand_mn'] / 1000, (a.get('total_mn') or 0) / 1000

WK = {
 '02': "30 Jan-1 Feb: GUS put 2025 GDP at 3.6% (in line); MoF's February plan has sale auctions on 11, 18 and 25 Feb (PLN 7-12bn each) and budget accounts near PLN 180bn; non-residents added PLN 4.6bn of POLGBs in December (11.8% share). Abroad: Trump named Kevin Warsh as Fed chair (30 Jan) - the dollar index rose 0.8%, gold fell 9% and silver 26%; S&P moved Italy to a positive outlook; a partial US shutdown began on 31 Jan.",
 '03': "2 Feb: January manufacturing PMI 48.8 (49.2 expected); the PAP survey has 10 of 18 forecasters expecting a hold on 4 Feb and 8 a cut; MoF mandated banks for a JPY issue. Abroad: US ISM manufacturing jumped to 52.6 (48.5 expected); Brent fell ~5% to ~$66 as the Iran premium faded; a US-India deal cut tariffs to 18%.",
 '04': "3 Feb: POLGBs were flat while IRS fell up to 3bp at 10Y on positioning for a possible cut (PKO); Millennium sees a hold priced. Abroad: the US shutdown ended; gold rebounded 6%; Miran called for ~100bp of cuts in 2026.",
 '05': "4 Feb: the MPC held at 4.00% (14:40) and said CPI may fall in Q1 and stay consistent with the target in coming quarters; FRAs rose 3-5bp. Fitch's analyst said macro-fiscal developments have matched its expectations since the September outlook cut. Abroad: euro-area flash HICP 1.7% (core 2.2%); ADP +22k; March Fed-cut odds ~10%.",
 '06': "5 Feb: Glapiński said a March cut follows 'if the projection shows nothing worrying' and called 3.5% possible; yields fell 3-5bp. Abroad: ECB held at 2.00% (Lagarde: a stronger euro could push inflation below target); BoE held 5-4 and signalled further cuts; CNB held at 3.50% with Czech flash CPI 1.6%; US JOLTS 6.54m, claims 231k; UST 10Y 4.21%.",
 '09': "6-8 Feb: MoF priced JPY 211.6bn (~PLN 4.8bn) in four tranches (3Y 1.88% to 20Y 3.65%); budget accounts reached PLN 183.4bn at end-January; MoF estimates Q4 GDP at ~4.1%; the January minutes show one member calling rates too low; 33-week T-bills sold PLN 2.6bn at 3.53%. Abroad: US payrolls were postponed by the shutdown; US-Iran talks in Oman; Takaichi won a landslide in Japan.",
 '10': "9 Feb: Q4 wages rose 8.5% y/y (above forecasts); Glapiński (AlUla) said inflation will stay within target this year, probably below 2.5%; Kotecki sees a March cut as very likely; MoF offered PLN 8-12bn in eight series for 11 Feb. Abroad: markets priced the first Fed cut in June.",
 '11': "10 Feb: Litwiniuk floated either two 25bp cuts (one in March) or one 50bp cut a bit later (April); POLGBs rallied with global bonds after flat US retail sales (UST 10Y ~4.15%). BGK announced an FPC auction for 12 Feb.",
 '12': "11 Feb: the MoF auction sold PLN 11.9bn against PLN 25.8bn of demand (OK0128 not sold); MoF says 2026 needs are ~33% financed; Zarzecki and Wnorowski see no strong case against a 25bp March cut; POLGBs fell 8-16bp on 10 Feb (10Y 5.03%, PKO). Abroad: US payrolls +130k (65-70k expected) with a -862k benchmark revision; March Fed-cut odds fell to 6%, July fully priced.",
 '13': "12 Feb: Q4 GDP +4.0% y/y (in line); Kotecki called March 'a very good moment' for -25bp and Masłowska also sees a March cut; BGK sold PLN 3.4bn of FPC (demand 6.3bn) plus 0.75bn; Millennium says above-potential growth limits the room for cuts. Abroad: Hungarian CPI 2.1% (2.4% expected); UK Q4 GDP +0.1%; US equities -1.6%, Bund 2.78%.",
 '16': "13-15 Feb: January flash CPI 2.2% y/y (1.9% expected, +0.6% m/m; on 2025 weights, the basket revision comes in mid-March); December current account -EUR 1.7bn (-1.1bn expected); the Sejm passed the SAFE defence-loan law. Abroad: US January CPI 2.4% (2.5% expected), core 2.5%; ~63bp of 2026 Fed cuts priced; CNB minutes show two members leaning towards a cut.",
 '17': "16 Feb: MoF raised the 18 Feb offer to PLN 8-13bn, adding PS0730, DS1034 and IZ0836; the January central-budget deficit was PLN 3.7bn (1.4% of the limit); ING says a 25bp March cut is 'essentially settled'; Fitch's analyst told money.pl the rating could hold if the 7%-of-GDP deficit path is credible. Abroad: US holiday; futures price ~70% for a June Fed cut; Japan Q4 GDP +0.2%.",
 '18': "17 Feb: swaps rose 2-3bp (Millennium); the new Fiscal Council called for debt stabilisation; BGK announced a 19 Feb FPC auction. Abroad: UK unemployment 5.2% put a BoE cut by April almost fully in the price; German ZEW 58.3 (65.2 expected); US-Iran talks in Geneva progressed, Brent -2.3%.",
 '19': "18 Feb: the MoF auction sold PLN 13.0bn (demand 22.1bn) plus 2.1bn additional; ~36% of 2026 needs financed; the 10Y broke below 5% (ING); Dąbrowski called April safer than March (50% odds for March). Abroad: FOMC minutes read hawkish (several open to two-way guidance); UK CPI 3.0%; Brent +4.3% on reports that US-Iran war was close.",
 '20': "19 Feb: January data were weak - wages +6.1% y/y (7.2% expected), industry -1.5% (+2.0%), construction -12.8%, PPI -2.6% - strengthening March-cut pricing (PKO); BGK sold PLN 1.9bn of FPC (demand 2.7bn); the PM urged Poles to leave Iran. Abroad: Trump said an Iran deal may come 'within 10 days'; US claims 206k; ~6% for a March Fed cut.",
 '23': "20-22 Feb: MoF said February is the last month of WIBOR-linked WZ sales - from March only POLSTR NZ floaters; Zarzecki: 25bp justified, 50bp not. Abroad: the US Supreme Court struck down the IEEPA tariffs (6-3) and Trump imposed a 10% global tariff, then announced 15%; US Q4 GDP +1.4% (2.8% expected), core PCE 3.0%; Brent at a six-month high (~$72).",
 '24': "23 Feb: January retail sales +4.4% y/y (3.1% expected); MoF offered PLN 8-12bn for 25 Feb; IRS rose ~8bp last week while bonds held on auction demand (Millennium). Abroad: the European Parliament paused ratification of the EU-US trade deal; Waller called March a 'coin toss'; gold +3%; Bund ~2.72%.",
 '25': "24 Feb: Glapiński said the March projection shows inflation close to target through 2026 and 2027; the 2Y POLGB hit a 4-year low (3.40-3.43%) and the 10Y 4.95% on global risk-off (PKO); the 2025 central-budget deficit was PLN 275.6bn vs 288.8bn planned. Abroad: the MNB cut 25bp to 6.25% (no easing cycle decided); the 10% US tariff took effect; FedWatch ~98% March hold; Bund 2.70%.",
 '26': "25 Feb: the MoF auction sold PLN 11.9bn on only 15.6bn of demand (cover 1.32, the weakest of 2026); ~38% financed; Litwiniuk called a March cut probable, Dąbrowski sees 3.5% as the end-point; GPW Benchmark announced no index changes for 27 Feb; Poland's January HICP 2.5% (new weights). Abroad: euro-area January HICP 1.7%; Greer said the 15% tariff comes 'in coming days'; Bailey sees scope to ease.",
 '27': "26 Feb: PKO flagged the weakest auction demand of 2026 as a sign of fatigue after heavy issuance; Poland's ESI fell to 101.3; the January vote record shows Tyrowicz's 75bp hike motion rejected; EBRD raised 2026 GDP to 3.7%. Abroad: Oman reported 'significant progress' in US-Iran talks; Lagarde said the ECB does not pre-commit; ~96% March Fed hold. Fitch reviews Poland after the close on 27 Feb.",
}

US = {'02': "Warsh named chair (30 Jan); ~15% for March, ~3% end-2026 funds rate priced",
      '03': "~15% for a March cut, ~29% by April (FedWatch, 1 Feb)", '04': "~15% for a March cut (FedWatch, 1 Feb)",
      '05': "~10% for March, ~46% by June (FedWatch, 4 Feb)", '06': "~10% for March, ~46% by June (FedWatch, 4 Feb)", '09': "~10% for March, ~46% by June (FedWatch, 4 Feb)",
      '10': "first 2026 cut priced for June (9 Feb)", '11': "hold until June, at least two cuts by end-2026 (10 Feb)",
      '12': "after payrolls: ~6% for March, ~48% by June (FedWatch, 11 Feb)", '13': "~50bp of 2026 cuts, next fully priced cut pushed later (12 Feb)",
      '16': "after CPI: ~63bp of 2026 cuts, >80% for a cut by June (13 Feb)", '17': "~70% for a June cut (16 Feb)", '18': "~64bp of cuts by end-2026 (17 Feb)",
      '19': "at least two cuts priced for the rest of 2026 (18 Feb)", '20': "after the minutes: ~6% for March, two cuts in 2026 (19 Feb)",
      '23': "~94% March hold (Polymarket, 20 Feb)", '24': "~94% March hold; Waller: March a 'coin toss' (23 Feb)", '25': "98% March hold, ~43% by June (FedWatch, 24 Feb)",
      '26': "98% March hold, ~43% by June (FedWatch, 24 Feb)", '27': "96% March hold, ~43% by June (FedWatch, 26 Feb)"}

GLOB = {'02': " Warsh nomination (30 Jan): dollar up, precious metals crashed; S&P Italy outlook positive.", '03': " US ISM 52.6 (2 Feb); Brent ~$66.",
        '04': " US shutdown ended (3 Feb).", '05': " Euro-area January HICP 1.7% (4 Feb).", '06': " ECB, BoE and CNB all held on 5 Feb; BoE 5-4 with an easing signal.",
        '09': " Poland priced JPY 211.6bn (6 Feb); US payrolls postponed.", '10': " Markets see the next Fed cut in June (9 Feb).", '11': " Global bond rally after flat US retail sales (10 Feb).",
        '12': " Strong US payrolls (+130k, 11 Feb) pushed Fed cuts out.", '13': " Hungary CPI 2.1% (12 Feb) opens MNB cuts.", '16': " US CPI 2.4% (13 Feb) revived Fed-cut pricing.",
        '17': " US holiday on 16 Feb.", '18': " BoE cut by April priced (17 Feb).", '19': " Hawkish FOMC minutes and an Iran-driven oil spike (18 Feb).", '20': " Iran: a deal 'within 10 days' (19 Feb).",
        '23': " IEEPA tariffs struck down; 10-15% global tariff instead (20-21 Feb).", '24': " EU-US trade deal ratification paused (23 Feb).", '25': " MNB cut to 6.25% (24 Feb); Bund 2.70%.",
        '26': " Euro-area HICP 1.7% (25 Feb).", '27': " US-Iran talks progressed (26 Feb)."}

OUT = {}
for R in DAYS:
    d = R[8:]; C = CUT[R]; w = FX[C]['wibor']; v = CV[R]; fra = v['fra']; L = lab(C)
    cuts = round((w['3m'] - fra['9x12']) * 100 / 5) * 5
    fra_s = f"FRAs at the {L} close (1x4 {fra['1x4']:.2f}, 3x6 {fra['3x6']:.2f}, 6x9 {fra['6x9']:.2f}, 9x12 {fra['9x12']:.2f} vs WIBOR 3M {w['3m']:.2f}) price roughly {cuts}bp of NBP cuts within 12 months."
    # ---------------- policy
    V = []
    if R < '2026-02-05':
        V += ["The MPC meets on 3-4 Feb after holding at 4.00% in January; Glapiński (15 Jan) put the terminal rate near 3.5% and excluded neither February nor March."]
        if ge(R, '03'):
            V += ["PAP survey (2 Feb): 10 of 18 expect a hold, 8 a cut; PKO expects a cut, Millennium a hold."]
    else:
        V += ["The MPC held at 4.00% on 4 Feb; the statement says CPI may fall in Q1 and stay consistent with the target in coming quarters."]
        if ge(R, '06'):
            V += ["Glapiński (5 Feb): a March cut if the projection shows nothing worrying; 3.5% possible as the end-point."]
        if ge(R, '10') and R < '2026-02-25':
            V += [{'10': "Kotecki (via PKO, 9 Feb): a March cut very likely.", '11': "Litwiniuk (10 Feb): two 25bp cuts (one in March) or one 50bp cut in April.",
                   '12': "Zarzecki and Wnorowski (11 Feb): no strong case against a 25bp March cut.", '13': "Kotecki (12 Feb): March 'a very good moment' for -25bp, April possibly another; Masłowska also sees March."}.get(d,
                  "Most MPC members now point to a 25bp cut in March (Kotecki, Masłowska, Zarzecki, Wnorowski); Litwiniuk floated 50bp in April instead.")]
        if ge(R, '16'):
            V += ["January flash CPI came in at 2.2% (1.9% expected, 13 Feb); ING (16 Feb) still sees a 25bp March cut as 'essentially settled'." if R < '2026-02-19' else
                  ("Dąbrowski (18 Feb): April safer than March, 50% odds for March" + ("; Zarzecki (20 Feb): 25bp justified, 50bp not." if ge(R, '23') else ".")) if R < '2026-02-25' else
                  "Glapiński (24 Feb): the March projection shows inflation near target through 2026-27; Litwiniuk (25 Feb): a March cut is probable; Dąbrowski (25 Feb): 3.5% is the end-point."]
        if ge(R, '20'):
            V += ["Weak January wages (+6.1%) and industry (-1.5%) on 19 Feb strengthened March pricing (PKO)."]
    pricing = fra_s + " " + " ".join(V)
    if R < '2026-02-05':
        risk = "The 4 Feb decision is a close call (PAP survey 10 hold / 8 cut): a hold lifts short FRAs, a cut extends the front-end rally; if cuts slip beyond March the roll-down does not materialise."
    elif R < '2026-02-16':
        risk = "A March cut is the consensus: the risks are the mid-March CPI basket revision, strong wages (Q4 +8.5%) and fiscal slippage; abroad, Iran/oil and US tariffs move the long end."
    elif R < '2026-02-26':
        risk = "January CPI (2.2%) beat forecasts before the basket revision; if the March projection disappoints, the cut slips to April (Dąbrowski) and the front end backs up; oil spikes on Iran and US tariff changes move the long end."
    else:
        risk = "A March cut is priced and expected; the risks are the mid-March CPI reweighting, auction fatigue (25 Feb cover 1.32) and Fitch on 27 Feb; oil and US tariffs move the long end."
    policy = dict(nbp_reference=4.0, next_mpc_label=("MPC next: 3-4 Feb" if R < '2026-02-05' else "MPC next: 3-4 Mar"), pricing_text=pricing, risk_text=risk)
    # ---------------- macro
    cpi = (dict(v=2.2, m="Jan flash (GUS, 13 Feb; 2025 weights, revision mid-March); Dec 2.4%") if ge(R, '16') else dict(v=2.4, m="Dec final (GUS, 15 Jan); core 2.7%"))
    fiscal = ("2025 general-government deficit ~7.0% of GDP; 2026 budget deficit cap PLN 271.7bn (in force; at the Constitutional Tribunal for follow-up review), gross borrowing needs ~PLN 690bn"
              + ("; the Sejm passed the SAFE defence-loan law (13 Feb), and SAFE loans sit outside the Polish public-debt definition (MoF)" if ge(R, '16') else "")
              + ("; January central-budget deficit PLN 3.7bn (1.4% of the limit)" if ge(R, '17') else "")
              + ("; 2025 central-budget deficit PLN 275.6bn vs 288.8bn planned (MoF, 24 Feb)" if ge(R, '25') else "") + ".")
    fin = ("~30% (29 Jan)" if R < '2026-02-12' else "~33% (11 Feb)" if R < '2026-02-19' else "~36% (18 Feb)" if R < '2026-02-26' else "~38% (25 Feb)")
    frisk = f"2026 needs {fin} financed; budget accounts PLN 183bn at end-January; Fitch reviews Poland on 27 Feb (after the close) and Moody's on 20 Mar, both with negative outlooks."
    gdp = "2025 GDP grew 3.6% (30 Jan)" + ("; Q4 +4.0% y/y (12 Feb)" if ge(R, '13') else "")
    base = (("The NBP held at 4.00% on 14 Jan" + (" and 4 Feb" if ge(R, '05') else "") + "; ")
            + ("January flash CPI 2.2% y/y (13 Feb; 1.9% expected)" if ge(R, '16') else "December CPI 2.4% y/y (final), core 2.7%")
            + "; " + gdp + ". Ratings: Fitch A- negative, Moody's A2 negative, S&P A- stable.")
    macro = dict(cpi=cpi, projection_text="NBP November 2025 projection: CPI 2.9% (2026), 2.5% (2027); the March 2026 projection comes with the 3-4 Mar MPC" + (" - Glapiński (24 Feb): inflation near target through 2026-27." if ge(R, '25') else "."),
                 fiscal_text=fiscal, fiscal_risk_text=frisk, backdrop_text=base + " " + WK[d])
    # ---------------- calendar / supply
    plan = ("MoF February plan (30 Jan): sale auctions on 11, 18 and 25 Feb (PLN 7-12bn each), no switch auction, a 33-week T-bill auction on 6 Feb; January sales were ~PLN 41.6bn incl. additional sales. "
            "BGK placed PLN 1bn of FWA0931 (Armed Forces Support Fund) privately (29-30 Jan).")
    if ge(R, '03') and R < '2026-02-09':
        plan += " MoF mandated Daiwa, Nomura and SMBC for a JPY issue (2 Feb)."
    if ge(R, '09'):
        plan += " JPY 211.6bn priced on 6 Feb (3Y 1.88%, 5Y 2.22%, 10Y 2.90%, 20Y 3.65%); 33-week T-bills PLN 2.6bn at 3.529%."
    if R in ('2026-02-10', '2026-02-11'):
        plan += " 11 Feb offer (9 Feb): PLN 8-12bn in OK0128, WZ0930, PS0131, NZ0331, IZ0831, DS1033, DS1035 and WS0437."
    if ge(R, '12'):
        s, dm, a = res('2026-02-11'); o = OPS['2026-02-11']
        plan += f" 11 Feb: PLN {s:.1f}bn sold vs {dm:.1f}bn demand (cover {dm/s:.2f}) plus {a:.2f}bn additional; OK0128 unsold; stop yields PS0131 {y(o,'PS0131'):.3f}%, DS1033 {y(o,'DS1033'):.3f}%, DS1035 {y(o,'DS1035'):.3f}%, WS0437 {y(o,'WS0437'):.3f}%."
    if R in ('2026-02-17', '2026-02-18'):
        plan += " 18 Feb offer (16 Feb): PLN 8-13bn in OK0128, PS0730, PS0131, NZ0331, DS1034, DS1035 and IZ0836."
    if ge(R, '19'):
        s, dm, a = res('2026-02-18'); o = OPS['2026-02-18']
        plan += f" 18 Feb: PLN {s:.1f}bn vs {dm:.1f}bn (cover {dm/s:.2f}) plus {a:.2f}bn; stop yields OK0128 {y(o,'OK0128'):.3f}%, PS0730 {y(o,'PS0730'):.3f}%, PS0131 {y(o,'PS0131'):.3f}%, DS1034 {y(o,'DS1034'):.3f}%, DS1035 {y(o,'DS1035'):.3f}%."
    if ge(R, '23'):
        plan += " MoF (20 Feb): February is the last month of WIBOR-linked WZ sales; from March floating supply comes only as POLSTR NZ."
    if R in ('2026-02-24', '2026-02-25'):
        plan += " 25 Feb offer (23 Feb): PLN 8-12bn in OK0128, WZ0930, PS0131, NZ0331, DS0432 and DS1035. March supply plan due 27 Feb."
    if ge(R, '26'):
        s, dm, a = res('2026-02-25'); o = OPS['2026-02-25']
        tot = sum(sum(res(x)[i] for i in (0, 2)) for x in ('2026-02-11', '2026-02-18', '2026-02-25'))
        plan += f" 25 Feb: PLN {s:.1f}bn vs {dm:.1f}bn (cover {dm/s:.2f}, the weakest of 2026) plus {a:.2f}bn; stop yields PS0131 {y(o,'PS0131'):.3f}%, DS0432 {y(o,'DS0432'):.3f}%, DS1035 {y(o,'DS1035'):.3f}%. February sales ~PLN {tot:.1f}bn incl. additional sales; March plan due 27 Feb."
    left = "11, 18 and 25 Feb" if R <= '2026-02-11' else "18 and 25 Feb" if R <= '2026-02-18' else "25 Feb" if R <= '2026-02-25' else "the March dates (plan due 27 Feb)"
    timing = ("Within each auction week of the Aug 2025-Feb 2026 sample, yields drifted lower into the auction and the auction-day close was the cheapest point relative to the preceding session, "
              f"so new buying is best executed at the auction-day close ({left}). ")
    covers = [("2026-02-11", '12'), ("2026-02-18", '19'), ("2026-02-25", '26')]
    cv = [f"{res(x)[1]/res(x)[0]:.2f}x ({int(x[8:])} Feb)" for x, k in covers if ge(R, k)]
    timing += ("February covers so far: " + ", ".join(cv) + (" - demand fading after a heavy start (ING, PKO). " if ge(R, '26') else ". ")) if cv else "January auctions were absorbed with 1.4-1.9x cover. "
    timing += ("The 3-4 Feb MPC is the next event (a close call)." if R < '2026-02-05' else "The 3-4 Mar MPC with the new projection is the next event; a 25bp cut is the consensus.")
    ev = [e for e in copy.deepcopy(F30['calendar']['events']) if e['date'] >= '2026-02-01']
    for e in ev:
        if e['date'] == '2026-02-04':
            e['note'] = "PAP survey (2 Feb): 10 of 18 expect a hold." if ge(R, '03') else "Close call after Glapiński's January hints."
        if e['date'] == '2026-03-04':
            e['note'] = "New projection; a 25bp cut is the consensus." if ge(R, '06') else e.get('note', '')
    add = [dict(date='2026-02-11', type='Auction', title='MoF sale auction PLN ' + ('8-12bn' if ge(R, '10') else '7-12bn'), note=('OK0128, WZ0930, PS0131, NZ0331, IZ0831, DS1033, DS1035, WS0437.' if ge(R, '10') else 'Plan: OK0128, WZ0930, PS0131, NZ0331, DS1035 (+IZ/other).'), source_date=('MoF offer 9 Feb' if ge(R, '10') else 'MoF February plan, 30 Jan')),
           dict(date='2026-02-18', type='Auction', title='MoF sale auction PLN ' + ('8-13bn' if ge(R, '17') else '7-12bn'), note=('OK0128, PS0730, PS0131, NZ0331, DS1034, DS1035, IZ0836.' if ge(R, '17') else ''), source_date=('MoF offer 16 Feb' if ge(R, '17') else 'MoF February plan, 30 Jan')),
           dict(date='2026-02-25', type='Auction', title='MoF sale auction PLN ' + ('8-12bn' if ge(R, '24') else '7-12bn'), note=('OK0128, WZ0930, PS0131, NZ0331, DS0432, DS1035.' if ge(R, '24') else ''), source_date=('MoF offer 23 Feb' if ge(R, '24') else 'MoF February plan, 30 Jan')),
           dict(date='2026-02-06', type='Auction', title='MoF 33-week T-bill auction', note='', source_date='MoF February plan, 30 Jan'),
           dict(date='2026-02-12', type='Data', title='GUS Q4 GDP flash', note='', source_date='GUS calendar'),
           dict(date='2026-02-13', type='Data', title='GUS January flash CPI', note='On 2025 weights; basket revision in mid-March.', source_date='GUS calendar'),
           dict(date='2026-02-13', type='Data', title='US January CPI', note='', source_date='BLS calendar'),
           dict(date='2026-02-18', type='CB', title='FOMC minutes', note='', source_date='Fed calendar'),
           dict(date='2026-02-19', type='Data', title='GUS January wages, industry, PPI, construction', note='', source_date='GUS calendar'),
           dict(date='2026-02-23', type='Data', title='GUS January retail sales', note='', source_date='GUS calendar'),
           dict(date='2026-02-24', type='CB', title='MNB decision', note='', source_date='MNB calendar'),
           dict(date='2026-02-27', type='Index', title='GPWB/TBSP periodic portfolio change', note=('Communique (25 Feb): no membership changes; TBSP MD 3.78, 1-3Y 1.74, 1-4Y 2.50.' if ge(R, '26') else 'Maturity-window changes (see Index section).'), source_date=('GPW Benchmark, 25 Feb' if ge(R, '26') else 'GPWB rules')),
           dict(date='2026-02-27', type='Supply', title='MoF March supply plan', note='', source_date='PAP week-ahead, 23 Feb' if ge(R, '24') else 'MoF practice')]
    if R <= '2026-02-06':
        add.append(dict(date='2026-02-06', type='Data', title='US January payrolls', note='', source_date='BLS calendar'))
    elif R <= '2026-02-11':
        add.append(dict(date='2026-02-11', type='Data', title='US January payrolls (postponed by the shutdown)', note='', source_date='BLS, 6-9 Feb'))
    if R in ('2026-02-11', '2026-02-12'):
        add.append(dict(date='2026-02-12', type='Auction', title='BGK FPC auction (FPC0229, FPC0231, FPC0332, FPC0235)', note='Minimum PLN 1.0bn.', source_date='BGK, 10 Feb'))
    if R in ('2026-02-18', '2026-02-19'):
        add.append(dict(date='2026-02-19', type='Auction', title='BGK FPC auction (FPC0229, FPC0231, FPC0332, FPC0235)', note='Minimum PLN 1.0bn.', source_date='BGK, 17 Feb'))
    ev = sorted([e for e in ev if not (e['type'] == 'Index' and e['date'] == '2026-01-30')] + add, key=lambda e: (e['date'], e['type']))
    calendar = dict(plan_text=plan, timing_text=timing, events=ev)
    # ---------------- core
    cp = copy.deepcopy(F30['core_policy'])
    tail = ("; PAP survey split on 4 Feb" if R < '2026-02-05' else "; March 25bp cut is the consensus")
    cp['Poland'].update(pricing=f"FRAs ~{cuts}bp of cuts within 12M ({L} close){tail}")
    if ge(R, '05'):
        cp['Poland'].update(last="held 4 Feb (last cut -25bp 3 Dec 2025)", next="3-4 Mar 2026", stance="Pause; March cut signalled" if ge(R, '06') else "Pause, data-dependent")
    cp['United States'].update(pricing=US[d], last="held 28 Jan (last cut -25bp 10 Dec 2025)", next="17-18 Mar 2026")
    if ge(R, '06'):
        cp['Euro area'].update(last="held 5 Feb (cut -25bp eff. 11 Jun 2025)", next="Mar 2026", pricing=("~20% for a cut by September (5 Feb)" if R < '2026-02-16' else "~30% for a cut by December (13 Feb)" if R < '2026-02-18' else "~40% for a cut by year-end (17 Feb)") + ("; Lagarde (26 Feb): no pre-commitment" if ge(R, '27') else ""))
        cp['United Kingdom'].update(last="held 5 Feb (5-4; cut -25bp 18 Dec 2025)", next="Mar 2026", pricing=("ING: cuts in March and June (5 Feb)" if R < '2026-02-18' else "a cut by April almost fully priced (17 Feb)"))
        cp['Czechia'].update(last="held 5 Feb (3.50%, 7-0)", next="Mar 2026", pricing=("flat PRIBOR curve" if R < '2026-02-16' else "minutes (13 Feb): two members leaning to a cut"))
    if ge(R, '13'):
        cp['Hungary']['pricing'] = "cuts priced in February and March (ING, 12 Feb)"
    if ge(R, '25'):
        cp['Hungary'].update(rate=6.25, rate_disp="6.25", last="-25bp 24 Feb 2026", next="Mar 2026", stance="Easing cautiously", tone="go", pricing="Varga: no easing cycle decided (24 Feb)")
    cc = copy.deepcopy(F30['core_cpi'])
    if ge(R, '05'):
        cc['Euro area'] = dict(v=1.7, m="Jan flash (core 2.2)" if R < '2026-02-26' else "Jan final (core 2.2)")
    if ge(R, '06'):
        cc['Czechia'] = dict(v=1.6, m="Jan flash")
    if ge(R, '13'):
        cc['Hungary'] = dict(v=2.1, m="Jan")
    if ge(R, '16'):
        cc['Poland'] = dict(v=2.2, m="Jan flash"); cc['United States'] = dict(v=2.4, m="Jan (core 2.5)")
    if ge(R, '19'):
        cc['United Kingdom'] = dict(v=3.0, m="Jan")
    note = F30['core_policy_note'].split(' Later releases')[0] + " Later releases used where published by the info cut-off (GUS, Eurostat, BLS, ONS, CZSO, KSH; ECB/BoE/CNB 5 Feb" + (", MNB 24 Feb" if ge(R, '25') else "") + ")."
    good = v.get('cds5y') and v.get('pl_bund_10y') and not v.get('flags')
    spr = (f" Poland's 5Y CDS was {v['cds5y']}bp and the 10Y spread to Bunds {v['pl_bund_10y']}bp on benchmark bonds (Erste, {L} close)." if good else f" (Erste's CDS/spread table for {L} looked stale or inconsistent, so it is not quoted.)")
    regime = (f"Regime: the NBP paused at 4.00% with ~{cuts}bp more priced, the ECB is on hold at 2.00%, the Fed holds into June, the BoE eases gradually, "
              + ("the MNB started cutting (6.25%)" if ge(R, '25') else "the CNB and MNB are on hold") + ".")
    core_text = regime + spr + GLOB[d]
    tk = list(Q30['takeaways_html'])
    if R < '2026-02-11':
        tk[2] = "<b>Supply:</b> BGK placed PLN 1bn of FWA0931 for the Armed Forces Support Fund privately (29-30 Jan); no FPC auction had been announced for February yet. FPC spreads are tight to POLGB, so pickups are thin."
    elif R == '2026-02-11' or R == '2026-02-12':
        tk[2] = "<b>Supply:</b> BGK FPC auction on 12 Feb (FPC0229, FPC0231, FPC0332, FPC0235; minimum PLN 1.0bn, announced 10 Feb); expect prints to cheapen into it."
    else:
        tk[2] = "<b>12 Feb BGK auction:</b> PLN 3.39bn sold vs 6.35bn demand plus 0.75bn additional." + (" <b>19 Feb:</b> PLN 1.88bn vs 2.74bn demand plus 0.33bn - weaker demand for guaranteed paper." if ge(R, '20') else " Another FPC auction is set for 19 Feb." if ge(R, '18') else "")
    au = {"MoF auctions & switch results": dict(as_of=("25 Feb" if ge(R, '26') else "18 Feb" if ge(R, '19') else "11 Feb" if ge(R, '12') else "28 Jan") + " 2026 auction + additional sale",
                                            published="auction days", source="MoF wholesale-bond database (only rows whose same-day release is confirmed by PAP/bank dailies); MoF/PAP communiques", note="No new series, switch or buyback in February."),
          "Index portfolios (GPWB 1-3Y, 1-4Y, TBSP)": dict(as_of="30 Jan 2026 rebalance (holdings 27 Jan)", published="28 Jan 2026 (served PDF carries 2 Feb 2026 metadata)", source="GPW Benchmark 'Portfele obligacji' communique",
                                                          note="Units match MoF settlements to 26 Jan." + (" The 27 Feb communique (published 25 Feb, no membership changes) is quoted in text only." if ge(R, '26') else "")),
          "NBP rates, MPC comments, 2026 MPC schedule": dict(as_of=("4 Feb 2026 decision" if ge(R, '05') else "14 Jan 2026 decision") + "; comments to " + WIN[R], published="<= " + WIN[R].split('-')[-1], source="NBP/MPC, PAP/Bloomberg/press interviews (first dated mention used)", note=""),
          "Bank views": dict(as_of=f"to {WIN[R]}", published=f"<= {WIN[R].split('-')[-1]}", source="PKO, Erste, Millennium, ING, Pekao, Deutsche Bank Polska, Credit Agricole, BPS; PAP", note="Only commentary published by the info cut-off.")}
    nfa = dict(input=f"New facts {WIN[R]} 2026", as_of=WIN[R], published=WIN[R], source="PAP feed (strefainwestorow.pl), MoF, NBP, GUS, BGK, GPW Benchmark, Eurostat, BLS, CME FedWatch, ECB/BoE/CNB/MNB, bank research",
               note="Facts placed in the window they were first published; PAP summary times are upper bounds.")
    od = dict(policy={'nbp_reference': 4.0, 'last_change': "3 Dec 2025 (-25bp); held 14 Jan" + (" and 4 Feb" if ge(R, '05') else "") + " 2026", 'next_mpc': "2026-02-03/04" if R < '2026-02-05' else "2026-03-03/04"},
              facts=dict(policy=policy, macro=macro, calendar=calendar, core_policy={'_replace': True, '_value': cp}, core_cpi={'_replace': True, '_value': cc}, core_policy_note=note, core_text=core_text),
              quasi_takeaways=tk, audit_updates=au, new_facts_audit=nfa)
    adds = []
    for dd, k in covers:
        if ge(R, k):
            o = OPS[dd]
            adds += [dict(date=dd, settle=o.get('settlement'), type='S', op='AS', lines=[dict(series=l['series'], sold=l['sold_mn'], demand=l.get('demand_mn'), avg_yld=l.get('avg_yield'), price=l.get('avg_price')) for l in o['lines'] if l.get('sold_mn')]),
                     dict(date=dd, settle=o.get('settlement'), type='S', op='OB', lines=[dict(series=s, sold=x, demand=None, avg_yld=None, price=None) for s, x in (o.get('additional_sale') or {}).get('lines', {}).items() if x])]
    if adds:
        od['mof_ops_add'] = adds
    OUT[R] = od
json.dump(OUT, open(SP / 'feb/facts_days.json', 'w'), indent=1, ensure_ascii=False)
print('ok', len(OUT))
