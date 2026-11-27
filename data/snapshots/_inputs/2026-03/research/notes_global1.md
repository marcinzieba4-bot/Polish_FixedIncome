# Global PIT facts 27 Feb - 15 Mar 2026: working notes
Windows (CET publication): R0302 = 27 Feb-1 Mar; R0303 = 2 Mar; R0304 = 3 Mar; R0305 = 4 Mar; R0306 = 5 Mar; R0309 = 6-8 Mar; R0310 = 9 Mar; R0311 = 10 Mar; R0312 = 11 Mar; R0313 = 12 Mar; R0316 = 13-15 Mar.
Output: facts.json (211 facts + 14 fed_pricing rows), built by build/make_json.py. The schema is the same as facts_global_1.json: facts{published, window_report_date, topic, text, src} and fed_pricing{published, text, src}. The script sets the window from the CET publication date, takes PAP times from dl/list/idx.tsv and Odaily times from dl/od/all.tsv, and asserts that each cited article was downloaded.
Europe stayed on CET for the whole period (CEST starts 29 Mar). The US moved to EDT on 8 Mar, so US 08:30 ET releases are at 14:30 CET up to 6 Mar and at 13:30 CET from 9 Mar (CPI 11 Mar, claims 12 Mar, PCE 13 Mar).

## Regime change
On Sat 28 Feb the US and Israel attacked Iran. Khamenei was killed: Trump posted it 28 Feb 22:59 CET and Iran confirmed on 1 Mar. The IRGC declared Hormuz closed, and Gulf oil and LNG flows largely stopped (Qatar LNG force majeure 4 Mar). Brent (front month is May from 2 Mar) rose from $72.5 (27 Feb, Apr contract) to ~$119.5 intraday on 9 Mar. It then fell below $90 on Trump's 'war basically over' (~21:00 CET 9 Mar) and was back above $100 on 12-13 Mar. The IEA announced a record 400m bbl release (11 Mar). Markets moved from pricing Fed, ECB and BoE cuts to pricing fewer Fed cuts and ECB hikes: one July hike fully priced plus 70% odds of a second (13 Mar). Gilts and Bunds sold off. The dollar rallied (DXY 97.6 -> 100).

## Access
- strefainwestorow listing as of 27 Nov 2026: 27 Feb = p469-470, 2 Mar p466-468, 6 Mar p456-458, 9 Mar p453-456, 13 Mar p444-446 (pages shift by ~2 a day as new items are added). The index is dl/list/all.tsv (864 urls). 216 macro and geo articles are in dl/art, with text in txt/ and times in dl/list/idx.tsv. scripts/day.sh YYYYMMDD prints the global digest sections, market lines and policy lines for a day.
- PAP yield table: scripts/tab2.py. The 6 Mar and 13 Mar tables are not date-stamped (EU rows = previous close). For the US rows, '1D' is the table's prior-day value. It is labelled as such and not claimed to be the official close.
- Odaily newsflash IDs 469830-472450 cover 27 Feb 01:08 - 17 Mar 01:32 CET. dl/od/all.tsv holds (id, CET, title, body). 23 IDs returned no page (likely deleted). scripts/odshow.sh prints full items. CET = page UTC dateTime + 1h.
- Trading Economics news pages resolve by ID under any indicator path. The datetime stamp is UTC (+1h applied). Only each article's own body was used, never the sidebar.
- countryeconomy.com/ratings/<country> was scanned for 21 EA sovereigns. Changes dated in the windows: S&P Portugal outlook to Positive (27 Feb), Moody's Slovenia up to A2 (27 Feb), S&P Croatia up to A (13 Mar). Clock times are placeholders (23:00).
- Other sources: Eurostat HICP flash, ECB (Lane FT transcript), RTE/Reuters (ECB trio 5 Mar), eco.sapo (Lagarde 10 Mar), CZSO flash, CNB (CPI comment, Kubicek interview), TE (HU CPI, gilts, Bunds, HICP), MNB minutes PDF (stamped 'published 2 p.m. on 11 March'), Global Trade Mag (15% tariff status).

## Key series (dates = close date unless stated)
- Bund 10Y (PAP table): 26 Feb 2.69, 27 Feb 2.64, 2 Mar 2.71, 3 Mar 2.75, 4 Mar 2.75, 5 Mar 2.84, 6 Mar 2.86, 9 Mar 2.86, 10 Mar 2.84, 11 Mar 2.93, 12 Mar 2.96. 13 Mar intraday 2.95-2.96 (the close is in the 16 Mar table, out of window). Schatz 2.00 -> 2.42.
- Spreads vs Bund: OAT 56 -> 67bp; BTP 61 -> 79bp (peak 79 on 12 Mar); Spain 41 -> 50bp. Obligacje.pl (13 Mar): OAT 10Y at a 15-year high.
- Gilt 10Y: 4.27 (26 Feb) -> 4.23 -> 4.37 (2 Mar) -> 4.47 -> 4.44 -> 4.54 -> 4.63 -> 4.65 -> 4.55 -> 4.69 -> 4.77 (12 Mar). UK2 3.53 -> 4.09. BoE March-cut odds: >80% (27 Feb) -> 60% (2 Mar, Bloomberg) -> ~20% (3 and 5 Mar, TE) -> 'very little chance of any 2026 cut' (11 Mar, TE).
- UST10: PAP evening/European-close quotes are 3.97 (27 Feb), 4.05 (2 Mar), 4.06 (3 Mar), 4.07 (4 Mar), 4.14 (5 Mar), 4.10-4.12 (6 Mar post-NFP), ~4.19-4.21 (9 Mar Asia), 4.11 (10 Mar), 4.21 (11 Mar), 4.22 (12 Mar), 4.25 (13 Mar ~14:00). UST2: 3.39 (2 Mar am) -> 3.53 (post-NFP 6 Mar) -> ~3.70 (12 Mar, a six-month high) -> 3.73 (13 Mar am). 2s10s +52 to +58bp.
- CEE: CZ2 3.41 -> 4.00; CZ10 4.34 -> 4.92; HU10 6.42 -> 7.35 (9 Mar peak) -> 6.94 -> 7.12.
- JGB10: 2.12 -> 2.06 (2 Mar open) -> 2.24 (13 Mar am).
- Brent front month (May from 2 Mar). Settles marked 'implied' come from next-morning PAP % moves and are derived, not exchange data: 27 Feb 72.48 (Apr, CNBC); 2 Mar ~77.7; 3 Mar ~81.4; 4 Mar ~81.4; 5 Mar ~85.4; 6 Mar 92.3-93.3 (conflict: PAP 92.32 at 22:09, Jin10 93.32; +27.5% w/w); 9 Mar intraday 119.50 high, ~99.0 implied settle, then ~89.6-90.6 late after Trump; 10 Mar ~87.8; 11 Mar ~91.4; 12 Mar ~100.5 (101.44 at 21:27); 13 Mar 101.5-102.9 late.
- DXY: 97.62 (27 Feb) -> 98.62 (2 Mar) -> 99.13-99.27 (3 Mar) -> 98.78 (4 Mar) -> 99.30 (5 Mar) -> 99.08-99.14 (6 Mar) -> 98.62 (10 Mar) -> 99.23 (11 Mar) -> 99.65 (12 Mar) -> 100.0-100.06 (13 Mar, first time at 100 since Nov 2025). ECB EUR/USD fixes: 1.1805, 1.1698, 1.1606, 1.1649, 1.1618, 1.1561, 1.1555, 1.1641, 1.1581, 1.1547, 1.1476.
- Gold: ~5,175-5,250 (27 Feb) -> 5,378-5,413 (2 Mar am) -> below 5,000 intraday on 3 Mar (-6%) -> 5,157-5,181 (4 Mar) -> 5,069 (5 Mar) -> 5,080-5,150 (6 Mar) -> 5,075-5,101 (9 Mar) -> 5,242 (10 Mar) -> 5,182 (11 Mar) -> 5,137 (12 Mar) -> ~5,100-5,119 (13 Mar, weekly decline). Silver 93-95 (27 Feb-2 Mar) -> 82-90.

## Timing judgements (CET)
- PPI (27 Feb 14:30) and the CNBC Brent settle (27 Feb) -> R0302. The Fitch Poland affirmation (Fri evening 27 Feb, PAP 28 Feb 13:21) -> R0302. It is a Poland item; keep it out of EA counts if the Poland file already has it.
- The WSJ story on the Fed challenging the Powell subpoenas (27 Feb 01:22) -> R0302 (it was excluded from the February file as out of window).
- Strike start: Odaily 28 Feb 07:16; PAP 13:03-13:20 -> R0302. Hormuz closure: IRGC 28 Feb 20:55 (Odaily) and again Mon 2 Mar evening (PAP 3 Mar 07:19) -> R0302 and R0304.
- PAP 1 Mar 20:31 'Brent +10% to ~$80 on Sunday' predates the 00:00 CET open: it is indicative only. The actual open (+13%) is in R0303.
- Lane FT interview: the ECB transcript is dated 3 Mar (Middle East questions added 2 Mar); PAP cited it at 12:21 -> R0304 (12:00 placeholder for the ECB page).
- HICP flash 3 Mar 11:00 -> R0304. CZ flash CPI 4 Mar (09:00 placeholder) -> R0305. HU CPI 10 Mar (TE 09:12) -> R0311. CNB CPI comment 10 Mar (10:00 placeholder) -> R0311. MNB minutes 11 Mar 14:00 -> R0312. Kubicek (Bloomberg) 11 Mar (12:00 placeholder) -> R0312.
- Warsh: the White House submitted the nomination 4 Mar 17:59 (Odaily) -> R0305. Timiraos on 'acting chair' 12 Mar -> R0313. Boasberg quashed the subpoenas 13 Mar (PAP 21:13) -> R0316. Warren/Tillis follow-up 14 Mar -> R0316.
- Payrolls and retail sales 6 Mar 14:30 -> R0309. Fed blackout from Sat 7 Mar (FOMC 17-18 Mar), so there are no Fed policy speakers in R0310-R0316 (Bowman 12 Mar was on bank capital only).
- Mojtaba Khamenei: Odaily 9 Mar 01:06 -> R0310. The weekend digest (8 Mar 19:28) only said a leader had been chosen. Trump's 'won't last long without my approval' (ABC) was 8 Mar 16:17 -> R0309.
- Oil above $100 at the Sunday-night open: first items 9 Mar 01:03 CET -> R0310, not R0309.
- Trump's 'war basically over': Odaily 9 Mar 20:40-20:57 -> R0310. PAP's 10 Mar 07:04 CBS piece is placed in R0311 for its extra content (threats on power plants); its headline was already public in R0310.
- USTR overcapacity probe of 16 economies: first sighting PAP 12 Mar 17:01 (which says 'Tuesday') -> R0313 (conservative). China's reaction (13 Mar) -> R0316.
- Wright's 172m bbl SPR release ('said Wednesday'): first sighting PAP 12 Mar digest -> R0313. IEA 400m bbl: 11 Mar 15:14 -> R0312.
- Kharg Island strike: Trump post 14 Mar 01:17 CET -> R0316.
- Placeholder clocks: S&P Portugal and Moody's Slovenia 27 Feb 23:00; S&P Croatia 13 Mar 23:00; Lane ECB page 3 Mar 12:00; CZ flash 4 Mar 09:00; Global Trade Mag 5 Mar 12:00; Lagarde 10 Mar 09:00; CNB comment 10 Mar 10:00; Kubicek 11 Mar 12:00.
- EXCLUDED as out of window: the 16 Mar yield table (13 Mar closes), CNB minutes and the 19 Mar decision, the MNB 24 Mar hold, the ECB/Fed/BoE/BoJ March decisions, the Seznam Michl article (26 Mar), later Warsh hearing (21 Apr) news, and later TE gilt/Bund pieces (18-year gilt highs, Bund 15-year highs late March). None were used.

## Caveats / conflicts
- Payrolls consensus: +55k (PAP), +59k (Jin10), ~+50k (one PAP piece), and +60k in the PAP week-ahead.
- US Feb core CPI m/m: +0.2% vs +0.2% expected (PAP 21:15; Jin10/BLS 0.2%), but PAP's 13:55 piece had +0.3% vs +0.3%. The 0.2% figure is used. BLS itself could not be fetched (blocked).
- PPI consensus: +0.3% m/m (Dow Jones/Jin10); y/y 2.6% expected (Jin10). Core +0.8% vs +0.3% comes from PAP only.
- 6 Mar Brent settle: 92.32 (PAP 22:09) vs 93.32 (Jin10 'close'). Unresolved.
- PAP stale lines: the gold/silver line in 3 Mar 18:18 repeats 2 Mar's (silver 88.05 -5.6%). PAP 27 Feb 18:23 has gold '6,054' (typo). PAP 2 Mar 14:32 and 3 Mar 12:21 have USD/JPY '153.x' (typo vs ~157). PAP 6 Mar 11:45 has Bund '2.65%' (typo vs 2.84). None of these values were used. PAP Brent labels alternate 'kwietniowe'/'majowe'; values are front-month May.
- Jin10 names: 'Milan' = Miran; 'Michael Bowman' = Michelle Bowman. Odaily 13 Mar has 'President Ebrahim Raisi' (sic; Pezeshkian); that item is not used.
- CZ flash consensus (1.6%) comes from Trading Economics via search snippet. The CNB's own forecast was 1.6%.
- The 15% global tariff was announced (21 Feb) and Bessent said 4 Mar it was coming 'this week', but no proclamation or CBP guidance was found inside the windows. The 10% Section 122 tariff (from 24 Feb) is the one in force in all windows. The EU was reportedly to be exempted (Jin10, 4 Mar).

## Gaps
- FedWatch prints only for 3, 6 and 11 Mar (none for 4-5 Mar, 9-10 Mar or 12-13 Mar). The rest is swaps or PAP text.
- ECB: no €STR curve numbers. Pricing is from PAP/LSEG/TE text (50% hike odds on 3 Mar -> >50% on 5 Mar -> a hike fully priced by year-end on 6 Mar -> two hikes on 12 Mar -> July hike plus 70% of a second on 13 Mar). Schnabel and Lagarde 2 Mar remarks were not retrieved. Rehn 5 Mar was a speech; only the RTE/Reuters summary was used.
- BoE: no speaker quotes in window (Taylor 2 Mar and Bailey 12 Mar not retrieved). The UK Spring Statement is covered only via TE (OBR 2026 growth cut to 1.1%).
- CZ: no CZ Q4 GDP (3 Mar), Jan IP or retail (12 Mar). HU: no Q4 GDP final (3 Mar) or IP (13 Mar); no MNB speaker remarks in window.
- US: no ISM prices-paid detail, retail control group or ECI. PCE m/m headline not captured. No exchange settlement prices for Brent or gold (intraday/implied only).
- EA sovereign: no auction or syndication results; no DBRS or Scope actions checked. France: only the 15-year-high 10Y comment.
- Ukraine: only headline items (trilateral postponed, Trump-Putin call 9 Mar, EU sanctions extension 14 Mar, Druzhba/Hungary dispute). No peace-talk substance.
