# Working notes: June 2026 fixings (C = 29 May; 1, 2, 3, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29 Jun 2026)
All pages fetched 2026-11-27. Later-published pages were used only to read the rows dated C.
Output: fixings.json (same folder). It has the same schema as 2026-05/research/fixings.json, checked by scripts/verify_schema.py and scripts/schema_paths.py:
- Every record kind (top, by_date[C], wibor, wibor/wibid, euribor, pribor, bubor, nbp_fx, fpc, fpc[traded], fpc[notraded], polstr[d], polstr/*_comp) has exactly the May key set, in the May key order.
- Value types are the same and there are no nulls (59 coarse paths = 59).
- Per-bond normalised paths: 116, identical to the April file. Against May, the only extra paths are the 6 FPC0332[notraded] paths (FPC0332 had no trade on 9, 15 and 23 Jun; it traded on every May C). This is a data state, not a schema change.
- 21 by_date records, 22 POLSTR index dates (28 May-29 Jun), 19 notes.
Builder: scripts/build.py (-> core.json + checks.txt, all cross-checks) + scripts/finalize.py (adds notes from scripts/notes_jun.py) + scripts/verify_schema.py.
Parsers: scripts/parse_gpwb.py (-> gpwb_parsed.json), erste_list.py (archive -> erste_list.json), parse_erste.py (-> erste_parsed.json), erste_chain.py (-> erste_chain.txt), cat_official.py (-> cat_parsed.json), parse_br.py (-> br_parsed.json), parse_bubor.py (-> bubor_parsed.json).
xlrd 2.0.1 was installed into pylib/ (pip --target) for the .xls files; scripts add it to sys.path and run under python3 -I. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip `<!-- -->` comments). HTTP 200 on the first try. The rolling table runs 2026-01-02..2026-11-25.
  Column order on the page is WIBID ON/1M/3M/6M/SW, then WIBOR ON/1M/3M/6M/1Y/SW (SW is the shaded last column of each block); post-window rows have "-" for ON/SW. Post-window page text (ON discontinued 1 Oct 2026, SW publication ended) was ignored.
  Cross-check: Erste Codziennik issued C+1, "Stawki WIBOR" (no 1Y). C -> id:
  29.05->169472 (issue 1 Jun), 01.06->169480, 02->169482, 03->169489 (issue Fri 5 Jun), 05->169491, 08->169494, 09->169495, 10->169498, 11->169499, 12->169503,
  15->169515, 16->169517, 17->169523, 18->169525, 19->169527, 22->169531, 23->169534, 24->169536, 25->169539, 26->169541, 29->169544. (169465 = 29 May issue, C=28 May, used as the chain base.)
  URL: https://www.erste.pl/regulation_file_server/download?id=<id>&lang=pl_PL (-L). Archive: SP/dl/erste_archiwum.html (downloaded today by the coordinator; regex `<div class="item-box" data-item-group-id="06-2026" data-item-id="(\d+)">`; 21 June items, the href carries the file-server stamp `time20260601090344`).
  ON/SW/1M/3M/6M match GPWB on all 21 C. On every issue, value minus change = the previous GPWB fixing (5 Jun issue: vs 3 Jun). The fixing column = NBP(C) on all 21 C. Both headers ("Poprzednia sesja na rynku FX", "Rynek stopy procentowej") = C on all 21.
  Archive: one issue per Polish business day 1-30 Jun and none on 4 Jun. Nothing is missing and no WIBOR table is stale.
  File-server stamps are 07:55-09:21 Warsaw on the issue date (latest 3 Jun 09:21, 5 Jun 09:16, 2 Jun 09:06, 1 Jun 09:03). HTTP Last-Modified matches the stamp. PDF CreationDate is 05:50-07:01 UTC.
  Formats: dd/mm/yyyy with points on 169472, 169480, 169482, 169491, 169494, 169495, 169498, 169499, 169541, 169544; dd.mm.yyyy with commas on the rest. All issues use the 4-page Erste Bank Polska layout. pdftotext -layout; the NBP fixing is the 5th number on the EURPLN/USDPLN rows (some print 3 decimals, e.g. 4.253 = 4.2530).
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione (latest complete index date 2026-11-19; the 20 Nov row has no POLSTR/WIRON yet). All 22 index dates 2026-05-28..2026-06-29 are present; there is no 4 Jun. The index dates equal the WIBOR fixing dates. 28 May is identical to the May file.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.M01+M03+M06+M12.BID._Z?format=csv&startPeriod=2026-05-20&endPeriod=2026-07-05 ("Stand vom 27.11.2026 14:32"). 4 Jun and 19 Jun have values (TARGET open). Weekends = "Kein Wert".
- PRIBOR: CNB year.txt?year=2026 (split on `|`; idx 12/14/18 = 3M/6M/1Y PRIBOR). Every June weekday has a row; last row 20 Nov.
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (cols 6/9/15; Excel serial dates). Every June weekday has a row; latest row 27 Nov.
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-05-25/2026-07-01/?format=json. Tables 103..123/A cover the C dates; there is no 4 Jun table (106/A = 3 Jun, 107/A = 5 Jun).
- Catalyst PRIMARY: gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls. Month list: POST year=2026&month=06 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL.
  It lists 21 sessions, 1-30 Jun; catalyst_20260604.xls returns 302 -> page-404. June files are still .xls with an unchanged layout (sheet "instrumenty": col 2 accrued, 11 close, 12 reference, 14-16 open/low/high, 19 #trades, 20 volume, 21 value thous., 22-23 block) and one GPW RR row per FPC bond. There are no block or off-session FPC trades. Header date (sheet "statystyka" cell K5) = C in all files.
  HTTP Last-Modified is on C for 20 of 21 C files (16:44-17:48 UTC). EXCEPTION: catalyst_20260616.xls Last-Modified = Wed 17 Jun 16:50:48 UTC, 17 s before the 17 Jun file (16:51:05), i.e. (re)posted after the R=17 Jun pre-open. Its internal last-saved is Tue 16 Jun 16:26:04, header 2026.06.16, and its FPC rows match biznesradar, so the content is the 16 Jun session (GPW Catalyst also shows session results live). Flagged, values kept.
  Internal last-saved (`file` command, OLE summary) is on C 16:25-16:27 UTC for all C files. The 30 Jun file (not a C) reads "Sun May 31 16:25:52", the month-end artefact seen on 30 Apr.
  All May files and 28-30 Apr were re-downloaded for lookback. They reproduce the May output (0 mismatches on 114 bond-days).
- Catalyst cross-check: biznesradar notowania-historyczne/<BOND>[,<page>] (50 rows per page; pages 1-3, page 1 only for FPC0231, which covers 13 Jan-25 Nov). OHLC+vol are identical on all 93 traded bond-days, and none of the 33 no-trade bond-days has a row. No bond has a 4 Jun row. Last-trade dates and closes agree.
- Re-check of the May output with today's downloads: WIBOR/WIBID (20 C), PRIBOR (19 C with a CZ fixing), BUBOR (20), EURIBOR (20-28 May, 7), NBP (25-28 May, 4), POLSTR (22 index dates), Catalyst (114 bond-days) are all identical: 491 fields/bond-days, 0 mismatches. There are no source revisions.
- GPWB operational communiques (POST ajaxindex.php action=GPWKomunikat&start=ajaxSearch&page=komunikaty-operacyjne&format=html&lang=PL&offset=0&limit=50): nothing is dated between 11 May (equity index item) and 6 Jul 2026.
- GPWB error-impact reports (post-window; read only to confirm that nothing was restated). Index: https://gpwbenchmark.pl/raporty-rewizji-danych (WIBID/WIBOR) and /raporty-z-rewizji-danych (WIRON/POLSTR); PDFs under /pub/BENCHMARK/files/{WIBID_WIBOR,WIRON,POLSTR}/Raport_rewizja_danych_*_Q{2,3}2026.pdf.
  - WIBOR Q2 (PDF 21 Jul 2026): fixings are never re-set; 2 Q2 fixings would have differed (6M -1bp, 1Y -2bp), no dates.
  - WIBOR Q3 (PDF 21 Oct 2026): after one contributor corrected its non-transactional data (used in the method from 1 Jun 2026, per the report), the Q2 count rises to 8 (ON 6 cases: 3 x 1bp, 2 x 4bp, 1 x >4bp; 6M 1; 1Y 1). No dates. Not revised. (The 1 Jun methodology element is taken from a post-window report and is not used as a fact.)
  - WIRON Q2 (2 Jul) / Q3 (21 Oct): Q2 dates 12 and 18 May only; Q3 adds 2, 3, 9 Jul. No June date.
  - POLSTR Q2/Q3: no May or June date (Q2 lists 20 and 26 Feb only).
  - All reports say the history is not revised. The stored values are the published ones.

## Access
- Plain curl with the default UA worked everywhere (gpwbenchmark, erste -L, bundesbank, cnb, mnb, nbp, gpwcatalyst POST + files, biznesradar at 0.5 s spacing). There were no errors and no retries.

## Corpus Christi (Thu 4 Jun) and other holidays (what the data show)
- GPWB did NOT fix on 4 Jun: there is no WIBOR/WIBID row and no POLSTR/WIRON index date.
  The POLSTR CI accrues 2 days from 3 to 5 Jun at the 3 Jun rate (implied 3.3800 vs 3.380).
  published_by_convention: 3 Jun -> 5 Jun.
- On 4 Jun there was also no NBP table, no Catalyst session (month list, 302 on the file, no biznesradar rows) and no Erste issue.
  EURIBOR (TARGET open), PRIBOR and BUBOR did fix on 4 Jun. No C falls on 4 Jun, so they are not used.
- Erste issue of Fri 5 Jun (169489, C=3 Jun): headed 03.06.2026 in both blocks. All tables are the 3 Jun close with changes vs 2 Jun; nothing for 4 Jun.
  Erste issue of Mon 8 Jun (169491, C=5 Jun): PL IRS/FRA/bond changes are vs 3 Jun (chain OK, PL IRS +4..+9 over two sessions); US/EZ IRS changes are one-day moves vs 4 Jun (US 1L-5L value-change is 3-4bp below the 3 Jun value; EZ 10L 5bp); the spread change (+7) is not a 3->5 Jun change.
- Fri 19 Jun (Juneteenth): US only. GPWB WIBOR/POLSTR, NBP 117/A, EURIBOR, PRIBOR, BUBOR and a Catalyst session all exist.
  Erste 22 Jun (169527, C=19 Jun): every US IRS change is 0 (US closed; 18 Jun levels carried, 10L 4.31 vs 4.32). PL and EZ updated.
- CZ/HU: no holiday in June 2026. PRIBOR and BUBOR have a row on every June weekday, so no fallback was needed. bubor.date = C on all 21 C; no pribor src carries a fallback remark.

## Erste Codziennik flags (C+1 cross-check)
- Chain check (erste_chain.txt, 672 checks): from issue to issue, IRS/FRA/bond/US/EZ/CDS/spread value minus change = previous value within 1bp, except:
  - 169472 (1 Jun, C=29 May): PL-Bund 10Y spread row 283 (+2) is IDENTICAL to 169465 while the text says PL yields -14..-18bp and core moves negligible. Stale spread row.
  - 169489 (5 Jun): spread 275 (+3) vs 280 in 169482 (8bp chain break).
  - 169491 (8 Jun): US/EZ changes vs 4 Jun (above).
  - 169495 (10 Jun, C=9 Jun): bond table partly STALE. WS0428 4.64 (0) repeats the 8 Jun level; DS1035 5.87 (+6) and spread 281 (+6) are identical to 169494. The text says the curve fell 14bp on 9 Jun and IRS 12-15bp; the IRS table (-12..-15) is updated, PS0731 5.37 (-8) is updated.
    The next issue 169498 (C=10 Jun) shows WS0428 -22, DS1035 -13, spread -14, i.e. two sessions.
    NOTE FOR CURVE AGENTS: do not use the R=10 Jun Erste 2L/10L bond or spread rows as 9 Jun levels.
  - 169515 (16 Jun): CDS 5Y 50 (0) vs 52 in 169503 (2bp break).
  - 169527 (22 Jun): US IRS all 0 (Juneteenth carry).
- None stale in WIBOR/fixing tables, none missing, and no duplicate issue. Bond benchmarks stay WS0428/PS0731/DS1035 all month.
- In-window context read from the issues: RPP held 3.75% on 2 Jun (169482); Glapinski on 3 Jun said the low May CPI reduced the probability of hikes (169489); MNB cut 25bp on 23 Jun (169534).

## WIBOR
- Ranges over the 21 C: ON 3.57 (2 Jun)-3.88 (11-12 Jun), SW 3.78 (29 Jun)-3.85 (9 Jun), 1M 3.73 (15 Jun)-3.84 (9 Jun), 3M 3.83 (22 Jun)-3.88 (9 Jun), 6M 3.90 (26/29 Jun)-3.95 (10 Jun), 1Y 3.93 (26 Jun)-4.01 (10 Jun).
- 6M/1Y drift: 3.94/4.00 (29 May) -> 3.95/4.01 (10 Jun) -> 3.90/3.93-3.94 (26-29 Jun).
- No WZ coupon reset falls in June (WZ resets 25 May / 25 Nov), so no averaging window is listed.

## POLSTR publication (d+1 convention on the GPWB calendar, timestamps not verified)
28.05->29.05, 29.05->01.06, 01->02, 02->03, 03->05 (no GPWB fixing on 4 Jun), 05->08, 08->09, 09->10, 10->11, 11->12, 12->15, 15->16, 16->17, 17->18, 18->19,
19->22 (GPWB open on Juneteenth), 22->23, 23->24, 24->25, 25->26, 26->29, 29->30 Jun (30 Jun is the last report date, so the 29 Jun index is not used by any report: the builder uses published_by_convention < R).
CI accrual: the multi-day steps are 03->05 Jun (2d) and 29.05->01.06, 05->08, 12->15, 19->22, 26->29 (3d). Every step matches POLSTR x days/365 to 0.0001.
Month-end dip: index 29 May POLSTR 3.407 / WIRON 2.071 (28 May 3.506/2.799; 1 Jun 3.612/3.274). Index 29 Jun POLSTR 3.346 (26 Jun 3.597); index 30 Jun 2.698/2.178 is published on 1 Jul and is not stored.
Low WIRON prints, all in the source: 3 Jun 2.775, 11 Jun 2.835. POLSTR high 3.692 (25 Jun); WIRON high 3.405 (18 Jun).

## Other fixings
- EURIBOR 12M: 2.804 (29 May) -> 2.761 (1 Jun) -> 2.874 (12 Jun, high) -> 2.748 (18 Jun) -> 2.817 (23 Jun) -> 2.732 (29 Jun, low). 3M: 2.268 -> 2.417 (17 Jun) -> 2.317. 1M 1.964-2.285. Single source.
- PRIBOR: 3M 3.57 (29 May) -> 3.65 (18 Jun) -> 3.82 (19 Jun) -> 3.83 (29 Jun); 6M 3.67-3.89; 1Y 3.80 (1 Jun) -> 3.91 (18 Jun) -> 4.00 (19 Jun) -> 4.00.
  The 19 Jun step (3M +17bp) is in the source; the cause was not researched (no CNB item in the June Codziennik issues).
- BUBOR: 5.99/5.92/5.81 (29 May-1 Jun) -> 5.94/5.84/5.75 (12 Jun) -> 5.89/5.80/5.70 (17-19 Jun) -> 5.85/5.75/5.66 (23 Jun) -> 5.76/5.67/5.57 (24 Jun, after the 23 Jun MNB cut per Erste 169534) -> 5.70/5.63/5.54 (29 Jun).
- NBP: EUR 4.2322 (29 May)-4.2890 (29 Jun), USD 3.6319 (1 Jun)-3.7756 (24 Jun), CHF 4.6030 (10 Jun)-4.6526 (24 Jun). CHF is single source.
  Repeated mids are non-consecutive coincidences in distinct tables: EUR 4.2462 (108/A 8 Jun, 114/A 16 Jun); CHF 4.6042 (9/16 Jun), 4.6118 (15/19 Jun), 4.6516 (25/29 Jun).

## Catalyst findings
- Units unchanged. turnover_pln = official value (thous.) x 1000. The biznesradar Obrot ratio is 10.00-10.26 (exactly 10.00 for FPC0630 on 29 May, 1 and 2 Jun: accrued 0).
- No-trade days (33 bond-days; official #trades=0; close = reference = last trade close):
  - FPC0231 traded only 11 Jun (30 bonds, 103.00, +1.20), 24 Jun (29, 104.00) and 25 Jun (20, 104.00), each a single trade.
    No trade 29 May-10 Jun (last 19 May, 101.80, 1,902: 8 C here, 15 sessions in all), 12-23 Jun (last 11 Jun), 26/29 Jun (last 25 Jun): 18 bond-days.
  - FPC0229: 1 Jun (last 29 May, 102.30, 193), 3 Jun (last 2 Jun, 102.40, 30), 16-17 Jun (last 15 Jun, 102.95, 82), 24 Jun (last 23 Jun, 102.95, 10), 26 Jun (last 25 Jun, 104.00, 264): 6.
  - FPC0733: 3 and 5 Jun (last 2 Jun, 80.73, FOUR bonds), 11 Jun (last 10 Jun, 82.09, 597), 18 Jun (last 17 Jun, 81.92, 24), 22 Jun (last 19 Jun, 82.30, 929), 24 Jun (last 23 Jun, 82.33, 1,275): 6.
  - FPC0332: 9 Jun (last 8 Jun, 95.27, 163), 15 Jun (last 12 Jun, 95.28, 2,464), 23 Jun (last 22 Jun, 95.45, 239): 3. (First FPC0332 no-trade records since April.)
  - FPC0630 and FPC0235 traded every C.
- Thin/suspicious (median vol over traded C: 0229 14, 0630 548, 0231 29, 0733 236, 0235 669, 0332 141):
  - FPC0229: swings on tiny prints: 9 Jun -0.77 (3 bonds), 15 Jun +0.94 (82), 18 Jun -0.94 (14), 22 Jun +0.65 (13), 25 Jun +1.05 to 104.00 (264, range 102.95-104.00); 12 Jun 4,210 bonds in 6 trades (~300x median; high 102.70 vs close 102.01).
  - FPC0630: 16 Jun high 90.99 vs close 90.40, 17 Jun open/high 90.99 vs close 90.59; heavy 10-12 Jun (4,960 / 6,145 / 3,305); 24 Jun 15 bonds.
  - FPC0733: 9 Jun +1.05 to 82.05 on one 236-bond trade; 1 Jun -0.82 on 15 bonds; 3-5 Jun close held by a 4-bond print; heavy 25-26 Jun (4,015 / 2,999).
  - FPC0235: 8 Jun -0.70 to 100.60 (4,949); 15 Jun +0.83 to 103.20 on 16,755 bonds in 34 trades (~25x median); 12 Jun +0.60 on 70 bonds; 29 May +1.20 on 3,394. Rose 100.60 (8 Jun) -> 104.28 (29 Jun), high 104.30 (26 Jun).
  - FPC0332: 16 Jun one bond (95.46, +0.18) then one 2,700-bond trade on 17 Jun (95.30); 12 Jun 2,464; open/low 94.70 on 29 May, 1 Jun (7 bonds) and 8 Jun vs closes 95.06-95.27 (repeated off-market print).
- Coupons: FPC0630 (2.125%, coupon 5 Jun) was ex-coupon from 26 May. Accrued is 0.00 on 26 May-2 Jun and restarts at 0.17 on 3 Jun (3 days: a 3 Jun trade settles 8 Jun, T+2 skipping Corpus Christi), 0.23 on 5 Jun, rising monotonically to 1.51 on 29 Jun.
  Turnover = vol x price exactly on 29 May, 1, 2 Jun; from 3 Jun it exceeds vol x price by vol x accrued. Prices are clean (89.47-89.50 on 2-5 Jun, no coupon-size jump).
  The FPC0630 coupon cell is blank in the 8 Jun file only (2.125 before and after; cosmetic).
  No other bond has a coupon or record date in the window. Accrued rises monotonically, and FPC0332 stays at 3.72%.
- New lines: NONE for BGK/FWSZ/PFR in June. The BGK (PL00005...) and PFR sets are identical to May in every file 1-30 Jun.
  BGK: FPC0229/0231/0235/0328/0332/0342/0427/0630/0631/0733/1140, BGK1127, FPU1130, FWA0931, IWS0645. PFR: PFR0330/0627/0827/0927, PF10927. No FWSZ-named line exists.
  Treasury: 38 lines, each on GPW RR and BS RR, unchanged from the 18 May file (OK0129 added then) through 30 Jun. No Treasury line was added or removed in June.

## Gaps
None. Every field for every C has a value.
No holiday fallback was needed in June (no C on 4 Jun; no CZ/HU holiday on a C).
Flags only: Catalyst 16 Jun file posted 17 Jun (content = 16 Jun); Erste stale/mixed rows for curve agents (1 Jun spread, 8 Jun US/EZ changes, 10 Jun bonds/spread, 22 Jun US IRS).
Single-source fields: WIBOR 1Y, WIBID, NBP CHF, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
