# Global PIT facts 15-29 Jan 2026: working notes
Windows (CET publication): R0116 = 15 Jan; R0119 = 16-18 Jan; R0120 = 19 Jan; R0121 = 20 Jan; R0122 = 21 Jan; R0123 = 22 Jan; R0126 = 23-25 Jan; R0127 = 26 Jan; R0128 = 27 Jan; R0129 = 28 Jan; R0130 = 29 Jan.
Output: facts.json (116 facts + 12 fed_pricing rows), built by build/make_json.py. The schema matches the H1 file. The window is set from the CET publication date.

## Access
- strefainwestorow listing as of 26 Nov 2026: 15 Jan is p528-531, 23 Jan p517-519, 29 Jan p510-511, 30 Jan p507-509. Index: dl/list/all.tsv (url only). Macro articles (200) are in dl/art; text is in txt/ (scripts/ext.py).
- The PAP yield table ("rentownosci-obligacji-wybranych-panstw-tabela", about 06:35) carries the PREVIOUS day's closes for EU/CEE rows and live 06:3x values for US/JP rows. scripts/tab.py parses it. The 16 Jan and 23 Jan tables have no per-row date stamps.
- Odaily newsflash IDs 464480-466460 cover 15-30 Jan. Titles are in dl/od/titles.tsv (scripts/odt.sh). Timestamps are UTC+8, so CET = -7h. This was the source for FedWatch, Fed chair and gold milestones.

## Key series (dates = close date unless stated)
- Bund 10Y: 14 Jan 2.81, 15 Jan 2.82, 16 Jan 2.84, 19 Jan 2.84, 20 Jan 2.86, 21 Jan 2.88, 22 Jan 2.89, 23 Jan 2.91 (high), 26 Jan 2.87, 27 Jan 2.88, 28 Jan 2.86; 29 Jan ~2.84-2.85 intraday.
- UST 10Y (PAP 06:3x snapshots): 15 Jan 4.14, 16 Jan 4.17, 19 Jan 4.22 (Fri close), 20 Jan 4.26, 21 Jan 4.27, 22 Jan 4.25, 23 Jan 4.24, 26 Jan 4.21, 27 Jan 4.23, 28 Jan 4.23, 29 Jan 4.27. Intraday peak 4.28-4.29 on 20-21 Jan ("Sell America"). UST2: 3.51 (15 Jan), 3.56 (16 Jan), 3.61 intraday on 16 Jan after the Hassett remark, 3.57-3.59 (later).
- Gilt 10Y: 4.34 (14 Jan), 4.46 (20-21 Jan), 4.51 (23 Jan), 4.54 (28 Jan). OAT-Bund narrowed from 68bp to 57bp; BTP-Bund ran 60-65bp; Spain-Bund 36-41bp.
- JGB 10Y: 2.16 (15 Jan), 2.30 (20 Jan, highest since 1999), 2.24-2.28 later. 40Y above 4% on 20 Jan. 2Y 1.245% on 23 Jan (highest since 1996).
- Brent Mar (PAP intraday, ~18:00 CET unless stated): 15 Jan 63.43 (-4.6%), 16 Jan 64.4, 19 Jan 64.12, 20 Jan 64.88, 21 Jan 65.03, 22 Jan 64.26, 23 Jan 65.9, 26 Jan 65.66, 27 Jan 66.90 (67.6 at 22:24), 28 Jan 67.87 (68.61 at 22:07), 29 Jan 70.60 (70.85 at 22:17). No exchange settlements were collected.
- DXY: 99.33 (15 Jan) -> 98.51 (20 Jan) -> 96.97 (26 Jan) -> 96.60 (27 Jan, BBDXY lowest since Mar 2022) -> 96.3-96.4 (28-29 Jan). EUR/USD 1.1607 -> 1.1985 (27 Jan).
- Gold: >4,700 (20 Jan), >4,800 (21 Jan), >5,000 (26 Jan 01:28 CET), ~5,568 record (29 Jan morning), then a -5% intraday drop on 29 Jan. Silver >$100 on 23 Jan.

## Timing judgements (CET)
- Greenland tariff post: Sat 17 Jan (PAP 18 Jan 12:38) -> R0119. The reversal Truth Social post came on 21 Jan US afternoon (~19:30-20:00 CET; PAP 20:59) -> R0122.
- The Trump "armada to Iran" remark (22 Jan, Air Force One) is filed under PAP 23 Jan 21:01 -> R0126. The "another armada" remark (27 Jan) is filed under PAP 28 Jan 07:55 -> R0129. Both are the conservative (later) placement.
- The FOMC statement at 20:00 CET 28 Jan -> R0129. The Trump Fed-chair announcement (30 Jan) and S&P's Italy action (30 Jan) are OUTSIDE all windows and were deliberately excluded. Only the 29 Jan MNI preview is used.
- Vujcic as ECB VP: decided at the Eurogroup on 19 Jan evening, but the earliest stamp found is 20 Jan 00:03 CET. It is filed in R0121 (conservative).
- The US-Taiwan deal (Commerce announced 15 Jan US time) is filed under PAP 16 Jan -> R0119 (conservative).
- Trump's 25% semiconductor tariff proclamation was signed 14 Jan, so it belongs to the earlier run's window. It is not included.
- Approximate clocks: China data 03:00; CNB Frait Reuters interview 27 Jan (12:00 is a placeholder); HL UK CPI article 21 Jan (12:00 is a placeholder); French no-confidence votes 23 Jan (12:00 approx).

## Caveats / conflicts
- EZ final HICP: PAP wrote that flash core was 2.4%, but Eurostat's 7 Jan flash showed 2.3%. Final core is 2.3% either way.
- EZ composite PMI consensus: 51.6 (FXStreet) vs 51.8 (Trading Economics).
- UK CPI consensus: 3.3% (Reuters per HL). An AP snippet mentioned 3.5% "most economists"; the Reuters figure was used.
- FedWatch figures come from Odaily/Jin10 relays, not CME directly. The pre-FOMC 97.2% January-hold figure (Stocktwits/Fox) has no reliable timestamp and is NOT used.
- PAP evening Brent contract labels are sometimes wrong ("lutowe"/Feb vs Mar). Values are taken as front-month Mar.

## Gaps
- No euro-area sovereign rating action found inside the windows (the S&P Italy outlook change came on 30 Jan, out of window).
- ECB speakers: only the MNI sources piece (20 Jan), the Dec accounts (22 Jan), Lagarde in Davos (23 Jan) and Vujcic were found. Lane/Schnabel/Nagel/Villeroy quotes were not found, and no €STR-curve pricing numbers were collected.
- BoE: no speaker content (the Bailey 20 Jan speech was not retrieved). UK flash PMI (23 Jan) is not collected.
- US: PPI (30 Jan), Dec retail sales and Q4 GDP were not released in the windows. US PMI composite is not collected.
- CZ/HU data releases in the windows (CZ PPI 19 Jan, HU PPI/trade 29 Jan) are not collected. MNB vote details beyond "unanimous" are not available.
- The yen "rate check" by the NY Fed on 23 Jan US afternoon is not directly sourced. PAP (26 Jan 08:24) reports the intervention warnings and that the US might join.
- The Powell subpoena follow-ups (Senate/Tillis, DOJ) found no new items in these windows beyond the Cook hearing and Powell's attendance.
