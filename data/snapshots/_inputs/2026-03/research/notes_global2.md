# Global PIT facts 16-30 Mar 2026: working notes
Windows (Warsaw publication time): R0317 = 16 Mar; R0318 = 17 Mar; R0319 = 18 Mar; R0320 = 19 Mar; R0323 = 20-22 Mar; R0324 = 23 Mar; R0325 = 24 Mar; R0326 = 25 Mar; R0327 = 26 Mar; R0330 = 27-29 Mar; R0331 = 30 Mar.
Output: facts.json (159 facts + 19 fed_pricing rows), built by build/make_json.py. The schema is identical to 2026-02 facts_global_2.json: facts have published / window_report_date / topic / text / src; fed_pricing rows have published / text / src. The window comes from the publication date. Clocks are Warsaw local time: CET until 29 Mar 02:00, CEST after that (only 30 Mar items are affected). New topic label: "other CB" (RBA, SNB, Riksbank, BoJ, Norges).

## Big picture (as sourced, no hindsight)
A US-Israel war with Iran began on 28 Feb, and Iran is blocking Hormuz. The windows cover an energy shock (Brent $100-115, briefly about $120) and a repricing of every central bank in a hawkish direction. The Fed pivots from cuts to some hike risk, then back to neutral after 30 Mar. ECB hikes get priced and then trimmed. Gold suffers its worst week since 1983. Core yields reach multi-year highs: Bund above 3% (highest since 2011), gilt above 5% (highest since 2008), OAT highest since 2009, JGB highest since 1999. BTP-Bund widens from about 60bp in Feb to 96bp.

## Access
- strefainwestorow listing as of 27 Nov 2026: 16 Mar = p441-443; 19 Mar = p433-436; 23 Mar = p428-431; 26 Mar = p417-423 (heavy day); 30 Mar = p413-415; 31 Mar = p410-413. The index is in dl/list/all.tsv (1,467 urls). 259 macro articles are in dl/art and their text in txt/ (scripts/ext.py). Global digest sections are read with scripts/skr.py, and market-number lines are pulled with scripts/mk2.py.
- No "Skrót wiadomości" digests exist for Fri 20 Mar: the 1700/2100/2110/2115 slugs return 404. Coverage for 20 Mar comes from the DZIEŃ NA RYNKACH pieces plus Odaily.
- PAP yield table columns: current, 1d, 5d, 1m, 3m, 12m. EU/CEE rows are the previous close (date-stamped). US/JP rows are live at 06:3x. The 20 Mar and 27 Mar tables carry no stamps. The 25 Mar table is stamped with 24 Mar ~18:00 times.
- Odaily newsflash IDs 472250-474660 cover 16 Mar 00:00 to 31 Mar ~12:00. Titles are in dl/od/titles.tsv (UTC+8; subtract 7h for CET, 6h for CEST). Macro items with converted times are in dl/od/macro_cet.tsv. Full bodies come from scripts/odfull.py, and "$22" chunked bodies from scripts/odchunk.py. odfull prints +1h, so 30 Mar items were corrected to CEST by hand. 219 IDs return an empty "Odaily" page; these are probably deleted items.
- Official sources: the Fed statement and SEP tables (federalreserve.gov), the ECB press release, the BoE MPS and minutes, the CNB statement, the MNB press release and the ONS CPI bulletin. Trading Economics was used for the EZ flash PMI (news 535935, metaDesc only) and the UK CPI consensus (536259). countryeconomy.com was scanned for 26 sovereigns' rating changes. Irish Times was used for the S&P Ireland upgrade and LaPresse for the Moody's Italy forecasts.

## Key series (dates = close date unless stated)
- Bund 10Y (PAP table): 13 Mar 2.98, 16 Mar 2.95, 17 Mar 2.91, 18 Mar 2.94, 19 Mar 2.96, 20 Mar 3.04, 23 Mar 3.01, 24 Mar 3.03, 25 Mar 2.96, 26 Mar 3.07, 27 Mar 3.09. On 30 Mar PAP had 3.03 at 18:06; the 31 Mar table falls outside the windows. The intraday high was 3.087% on 27 Mar, the highest since 2011.
- Schatz: 2.44, 2.40, 2.38, 2.44, then 2.59 (19 Mar, ECB day), 2.67, 2.58, 2.67, 2.60, 2.72, 2.67.
- Gilt 10Y: 4.82, 4.77, 4.69, 4.74, 4.84, 4.99, 4.92, 4.96, 4.84, 4.97, 4.97; intraday 5.065% on 23 Mar. Gilt 2Y: 4.13, 4.10, 4.04, 4.10, then 4.40 (19 Mar, BoE 9-0), 4.57, 4.42, 4.47, 4.41, 4.53, 4.48.
- Spreads vs Bund: BTP 81 -> 78 -> 75 -> 79 -> 82 -> 92 -> 87 -> 92 -> 88 -> 95 -> 96bp; OAT 69 -> 65 -> 72 -> 70 -> 73 -> 69 -> 73 -> 74bp; Spain 47-54bp.
- UST10, live PAP table at 06:3x: 4.26 (16 Mar), 4.23, 4.18, 4.27 (post-FOMC), 4.25, 4.41 (23 Mar am), 4.38, 4.38, 4.36, 4.43, 4.39. UST10 fell 11bp to 4.33 on 30 Mar after Powell. UST2: 3.71, 3.68, 3.66, 3.80, 3.79, 3.94, 3.90, 3.91, 3.92, 3.99, 3.88; it touched 4.00% on 23 Mar.
- CEE 10Y: CZ 4.96 -> 4.76 -> 4.96; HU 7.33 -> 7.14 -> 7.47 (24 Mar) -> 7.33. JGB10: 2.22-2.38, with 2.38 on 27 Mar the highest since 1999.
- Brent (May contract, PAP ~18:00 / ~21-22:00): 16 Mar 102.7/100.2; 17 Mar 101.6/103.7; 18 Mar 108.4/109.8; 19 Mar about 114 intraday, 107.4 late; 20 Mar 109.8/111.7; 23 Mar 113.5 am, 96.7 low after Trump's postponement, 102.0/99.8; 24 Mar ~104/100.0; 25 Mar 101.1/102.8; 26 Mar 108.9/105.7; 27 Mar 111.5/113.4; 30 Mar 112.4/114.2. Brent gained a record ~48-49% in March. A weekly high above $120 is cited by PAP and the MNB ("close to 120"). No settlement prices were collected.
- DXY: 100.0 (16 Mar) -> 99.6 -> 99.8 / 100.12 post-Powell (18 Mar) -> 100.05, then a >1% drop late NY on 19 Mar -> 99.6-99.7 (20 Mar) -> 99.3 (23 Mar) -> 99.4-99.5 -> 99.6-99.8 (26 Mar) -> 100.1 (27 Mar) -> 100.51-100.56 (30 Mar), the highest since May 2025.
- ECB EUR/USD fixings: 1.1478, 1.1531, (none collected for 18 Mar), 1.1489, 1.1555, 1.1596, 1.1572, 1.1592, 1.1539, 1.1517, 1.1484. USD/JPY rose above 160 on 27 Mar.
- Gold: ~5,010 (16 Mar am) -> 4,982 -> 5,008 -> 4,883 (18 Mar) -> <4,600 (19 Mar) -> 4,491.67 (20 Mar NY close, -10% w/w, worst week since 1983) -> <4,100 (23 Mar Asia, -7.8%) then a rebound -> ~4,400 (24 Mar) -> 4,550-4,600 (25 Mar) -> <4,400 (26 Mar) -> 4,550 (27 Mar) -> 4,540-4,569 (30 Mar).
- TTF: EUR50 (16 Mar) -> 54.9 (18 Mar) -> 63.5 (19 Mar intraday) -> 52.5 (25 Mar) -> 55.4 (26 Mar) -> 54.8 (30 Mar). EU gas storage 28-29% vs 41-42% 5-yr average.

## Timing judgements
- The FOMC decision (18 Mar 19:00) and presser fall in R0319. Post-FOMC FedWatch (19 Mar 00:04) and Timiraos (00:05) fall in R0320.
- ECB, BoE, CNB, SNB, Riksbank and BoJ decided on 19 Mar -> R0320. The BoE minutes were published with the decision at 13:00. The CNB minutes come later and were not used.
- Trump's ultimatum post (Sat 21 Mar evening US time) appears on Odaily at 22 Mar 01:08 -> R0323. The 48h deadline (~01:00 CET 24 Mar) is computed from the post time; PAP gives the same figure in its 23 Mar week-ahead.
- Trump's 5-day postponement: 23 Mar ~12:10 -> R0324. The 10-day postponement to 6 Apr: 26 Mar 23:11 -> R0327.
- The S&P Ireland upgrade (Fri 20 Mar evening; 23:00 is a placeholder) -> R0323.
- Cook's 26 Mar evening speech is filed by the PAP 27 Mar 09:02 report -> R0330 (conservative).
- Schnabel (Fri 27 Mar pm) and the ECB April-hike odds falling to 50% are filed by the PAP 30 Mar 06:34 week-ahead -> R0331 (conservative). The 27 Mar 13:55 LSEG figure of 71% stays in R0330.
- The Moody's Italy/Spain, S&P Czechia and Fitch Denmark/Bulgaria/Switzerland reviews (Fri 27 Mar after close; 22:00 placeholder) -> R0330. Outcomes are unverified; see Gaps.
- Placeholders: Lagarde 25 Mar 12:00; Ireland 20 Mar 23:00; ratings 27 Mar 22:00. Data facts use the official release time and cite the PAP digest or the official page, as the earlier runs did.
- EXCLUDED as out of window: EZ Mar flash HICP, France/Italy CPI and the PL CPI (31 Mar); the 31 Mar PAP yield table; the Iranian parliament's Hormuz transit-fee bill (Odaily 31 Mar 02:12); the "Trump willing to end war with Hormuz closed" report (31 Mar 02:49); the final March PMIs (1 Apr); the ECB account (16 Apr). Later-dated search snippets (the final PMI revision to 50.7, April articles) were ignored.

## Caveats / conflicts
- Brent 20 Mar: the PAP 21:20 piece says Brent "topped $122", but its own quote is May $111.70 (+2.8%), and its 18:17 piece says "briefly above $120 this week". The $122 figure is flagged in the fact text.
- The TTF EUR54.90 (+6.5%) in the PAP 23 Mar 18:06 piece is identical to the 18 Mar 18:20 line and may be stale.
- PAP morning Asia pieces sometimes repeat the previous day's FX/UST/gold lines (e.g. 17 Mar 08:29 repeats 16 Mar). They were not used for numbers.
- The two PAP ECB items disagree on the number of prior holds ("four" vs "five"). The fact text just says "held again".
- PAP 18 Mar 09:17 (Millennium) says the market "prices one Fed hike". This looks like a typo for "cut" and was not used.
- Denmark's Social Democrat share: 19.2% in the exit poll (24 Mar), 21.9% final (25 Mar). Denmark is not in the euro area.
- FedWatch figures come from Jin10/Odaily relays, not CME directly. ECB/BoE pricing comes from PAP citing LSEG/Bloomberg. No €STR or SONIA curve levels were collected.
- Polish items (Moody's Poland review, NBP/RPP, PL fuel-tax package) are mostly left to the Poland file. Only the Moody's Poland no-action note appears, inside the weekend digest fact.

## Gaps
- US retail sales and PCE: no release inside the windows. PKO (PAP 16 Mar) says the CPI and PCE releases came in the week before 16 Mar; the next retail sales is 1 Apr per the PAP calendar. The only Feb PCE figure in-window is Powell's estimate (2.8% headline, 3.0% core). US data that were covered: IP, NAHB, PPI, durable goods, claims (19 and 26 Mar), Philly Fed, new home sales, LEI, flash PMIs and final UMich.
- Fed speakers not captured: Barr (24 and 27 Mar), Jefferson (27 Mar), Daly/Paulson (27 Mar), Williams (30 Mar evening), Miran's 25-26 Mar speeches; Bowman and Waller come only via Jin10 one-liners.
- ECB: Lane, Cipollone, Escriva, Villeroy, Kocher, Rehn and Sleijpen speeches in 23-27 Mar were not retrieved; only Lagarde, Nagel, Makhlouf, Wunsch, Schnabel and de Guindos (via PAP).
- BoE: no Bailey presser quotes and no Greene, Breeden or Taylor content. The only BoE pricing is "25bp hike priced for June" (20 Mar).
- No EZ flash consumer confidence (23 Mar) and no ZEW current-conditions figure. The EZ flash PMI consensus (51.0) comes from TE.
- Euro-area ratings: the S&P Ireland upgrade (20 Mar) is confirmed. For Moody's Italy/Spain (27 Mar), countryeconomy shows no change; no agency press releases were retrieved, so affirmation vs no action is unknown. No France/Belgium/Austria actions were found for 13-30 Mar. Croatia's change (13 Mar) is before the windows.
- US tariffs: only Trump's 16 Mar remark, the FT LNG-leverage report (23 Mar), the EP vote on the EU-US deal and the new US probes (26 Mar). Nothing on Section 122 expiry or new Section 232 actions was found in-window.
- No exchange settlement prices for Brent, gold or TTF (intraday quotes only). No DXY close prints were collected for 24-25 Mar beyond the PAP intraday quotes.
