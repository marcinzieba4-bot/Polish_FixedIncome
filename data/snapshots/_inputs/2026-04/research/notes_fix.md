# Working notes: Apr 2026 fixings (C = 31 Mar; 1, 2, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29 Apr 2026)
All pages fetched 2026-11-27. Later-published pages used only to read the row dated C.
Output: fixings.json (same folder), same schema as 2026-03/research/fixings.json. Checked by scripts/finalize.py and scripts/schema_paths.py: identical key sets at every level (140/140 key paths), same value types, no nulls.
Builder: scripts/build.py (-> core.json + checks.txt, all cross-checks) + scripts/finalize.py (adds notes, schema/null check).
Parsers: scripts/parse_gpwb.py, parse_erste.py, cat_official.py, cat_scan.py, parse_br.py, load_src.py. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip all `<!-- ... -->` comments, which hold the dead cells). HTTP 200 on the first try this time.
  Header: WIBID ON,1M,3M,6M,SW | WIBOR ON,1M,3M,6M,1Y,SW. The rolling table runs 2026-01-02..2026-11-25.
  The page now carries post-window text (ON/SW discontinued 1 Oct 2026). It was ignored.
  Cross-check: Erste (ex-Santander) Codziennik issued C+1, "Stawki WIBOR" table (no 1Y).
  C -> id (archive https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum):
  31.03->169190, 01.04->169191, 02->169192, 07->169198, 08->169208, 09->169219, 10->169225, 13->169244 (STALE), 14->169248,
  15->169251, 16->169254, 17->169284, 20->169295, 21->169321, 22->(none), 23->169336, 24->169378, 27->169382, 28->169385, 29->169390.
  Extra: 169195 = 7 Apr issue, which carries the 3 Apr (Good Friday) fixing.
  URL: https://www.erste.pl/regulation_file_server/time<stamp>/download?id=<id>&lang=pl_PL. The server ignores the time stamp; `download?id=` alone works.
  ON/SW/1M/3M/6M match GPWB on all 18 directly covered C, and their labels are C. On every issue, value minus the change column reproduces the previous GPWB fixing.
  - C=13 Apr: the 14 Apr issue 169244 is a stale copy. Its whole market page (FX session, fixing column, WIBOR, IRS/FRA, bond yields) shows the same numbers as the 13 Apr issue 169225 in every table checked, labelled 10/04/2026. Only the front page is new.
    13 Apr is confirmed through the change column of the 15 Apr issue (169248). NOTE FOR CURVE AGENTS: the Erste IRS/FRA table of R=14 Apr is the 10 Apr table.
  - C=22 Apr: the archive lists no 23 Apr issue. Item 169225 (13 Apr) has a file-server stamp of 23 Apr 15:05, but its PDF CreationDate is 13 Apr 07:16 UTC.
    Probing ids 169322-169335 found no Codziennik. 22 Apr is confirmed through the change column of the 24 Apr issue (169336, labelled 23.04).
  - Formats: dd/mm/yyyy with decimal points (169195-169244, 169254) or dd.mm.yyyy with commas. From 27 Apr the issue uses the new Erste Bank Polska 4-page layout; its tables are unchanged.
  - Late uploads (file-server stamp): 1 Apr 15:06, 7 Apr 13:39, 10 Apr 12:57, 27 Apr 12:24 (PDF created 09:56 UTC), 30 Apr 10:30. The others were created 06:04-07:16 UTC.
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione, "Data wskaźnika" = index date. Cols: POLSTR, comp 1M/3M/6M, CI, '', WIRON, comp 1M/3M/6M. Latest index date 2026-11-19.
  All 23 index dates 2026-03-27..2026-04-29 are present, including 3 Apr; there is no 6 Apr. The index dates are identical to the WIBOR fixing dates. 27 and 30 Mar are identical to the March file.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-03-20&endPeriod=2026-05-08 ("Stand vom 26.11.2026 13:24"). 3 and 6 Apr = "Kein Wert" (TARGET holidays).
- PRIBOR: CNB year.txt?year=2026, split "|": idx 12=3M, 14=6M, 18=1Y (last row 19 Nov). No rows on 3 and 6 Apr (CZ holidays).
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (col 6=3M, 9=6M, 15=12M). Every C is a HU fixing day, so date=C; 3 and 6 Apr have no fixing.
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-03-27/2026-04-30/?format=json. Tables 062..082/A for the C dates; 065/A = 3 Apr (published on Good Friday).
  EUR/USD match the Codziennik fixing column on all 18 directly covered dates. The stale 14 Apr issue shows NBP 10 Apr.
- Catalyst PRIMARY: https://gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls (April files are still .xls).
  Month list: POST year=2026&month=04 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL. It lists the 20 April sessions; there is no 3 Apr, and that URL returns 302.
  Sheet "instrumenty" layout unchanged (xlrd 2.0.2 installed with pip; columns as in March). The FPC lines appear only on GPW RR, one row each. No block or off-session FPC trades.
  Header date = C in all 20 files. HTTP Last-Modified is on C 16:30-17:45 UTC for 18 files. Internal "Last Saved" (`file`) is on C 16:25-16:59 UTC.
  Exceptions:
  - 8 Apr: Last-Modified 9 Apr 07:22 UTC (09:22 Warsaw), internal save 8 Apr 21:49 UTC. The official file was posted after the R=9 Apr pre-open; the session prices (= biznesradar) were public on 8 Apr.
  - 22 Apr: Last-Modified 23 Apr 10:05 UTC (internal 22 Apr 16:25, normal). Re-posted; first posting time unknown.
  - Month-end metadata artefact: 31 Mar internal "Sat Feb 28 16:25:56", 30 Apr internal "Tue Mar 31 16:26:12". Header and content are C (they match biznesradar).
  The 2-30 Mar official files were re-downloaded for last-trade lookback. Their FPC rows reproduce the 2026-03 output exactly (0 mismatches).
- Catalyst cross-check: https://www.biznesradar.pl/notowania-historyczne/FPCxxxx[,N] pages 1-8 (coverage back to 2024/2025 for all six bonds).
  OHLC+vol are identical on all 105 traded bond-days, and none of the 15 no-trade bond-days has a biznesradar row. Last-trade dates and closes agree.
- Re-check of the March output with today's downloads: WIBOR/WIBID (22 dates), PRIBOR (22), BUBOR (22), EURIBOR (7 in range), NBP (2), POLSTR (23 index dates) all identical. No source revisions.

## Access
- Plain curl with the default UA worked everywhere (gpwbenchmark, erste with -L, bundesbank, cnb, mnb, nbp, gpwcatalyst POST + files, biznesradar with 0.5 s spacing). There were no errors and no retries.
- Erste archive page (5.2 MB) holds item-ids, dates and titles: regex on `data-item-group-id="MM-YYYY" data-item-id=...`.

## Good Friday 3 Apr / Easter Monday 6 Apr (what the data show)
- GPW Benchmark fixed WIBOR on Fri 3 Apr. WIBOR ON 3.61, SW 3.80, 1M 3.77, 3M 3.85, 6M 3.88, 1Y 3.90; WIBID 3.31/3.60/3.57/3.65/3.68. There is no 6 Apr row.
  The 7 Apr Codziennik (169195) prints the 3 Apr fixing with changes vs 2 Apr (ON -8, 1M -5, SW/3M/6M 0). It labels the fixing 06/04/2026, the FX session date, although there was no fixing that day.
  Its fixing column is NBP 3 Apr, and its text says money-market rates moved negligibly "w piątek".
- POLSTR index date 3 Apr exists. CI accrual is 1 day for 2->3 Apr and 4 days for 3->7 Apr, so 3 Apr was a GPWB business day.
  published_by_convention: index 2 Apr -> 3 Apr; 3 Apr -> 7 Apr. Not verified with timestamps (d+1 rule as in March).
- NBP table 065/A published on 3 Apr. EURIBOR, PRIBOR, BUBOR and Catalyst: nothing on 3 or 6 Apr.
- by_date['2026-04-02'] keeps the 2 Apr row (schema: src_row_date = C). The 3 Apr fixing was the latest published before R=7 Apr.
  It differs only in ON (3.69 -> 3.61) and 1M (3.82 -> 3.77); 3M (3.85) and 6M (3.88) are the same.
- WIBOR 6M 15-24 Apr (May WZ resets): 15: 3.88, 16: 3.88, 17: 3.89, 20: 3.89, 21: 3.88, 22: 3.88, 23: 3.89, 24: 3.90.

## Catalyst findings
- Units unchanged: nominal 1,000 PLN; turnover_pln = official value (thous.) x 1000; biznesradar Obrót is 10.02-10.25x smaller.
- No-trade days (official #trades=0; closing = reference = last trade close):
  FPC0231: traded only 31 Mar (8 bonds, 2 trades, 100.78-102.49), 7 Apr (2, 103.15), 13 Apr (5, 104.94), 17 Apr (20, 103.68), 20 Apr (20, 104.68), 24 Apr (14, 104.37), 27 Apr (954 in 3 trades, 103.37) and 28 Apr (30, 102.32).
    No trade 1-2 Apr (last 31 Mar), 8-10 Apr (last 7 Apr), 14-16 Apr (last 13 Apr), 21-23 Apr (last 20 Apr), 29 Apr (last 28 Apr): 12 bond-days.
  FPC0229: 9 Apr (last 8 Apr, 102.45, 54). FPC0733: 29 Apr (last 28 Apr, 81.35, 1,438). FPC0332: 28 Apr (last 27 Apr, 95.06, 890).
  FPC0630, FPC0235: traded every C.
- Thin/suspicious (median vol over traded C: 0229 54, 0630 490, 0231 17, 0733 30, 0235 1,744, 0332 251):
  - FPC0231 jumps on tiny prints: 31 Mar +1.49 (range 1.71 on 8 bonds); 13 Apr +1.79 (5 bonds); 17 Apr -1.26; 20 Apr +1.00; 27 Apr -1.00 on 954 bonds (~56x median); 28 Apr -1.05.
    The direction is consistent with FPC0235 (7->13 Apr +1.67).
  - FPC0229: 20 Apr 3,833 bonds in 2 trades (~71x median); 17 Apr 1,100 (~20x); 24 Apr 1 bond; 21 and 28 Apr 4 bonds.
  - FPC0733: 28 Apr 1,438 bonds in ONE trade (~48x median); 24 Apr 1 bond.
  - FPC0630: 13 Apr 1 bond; 29 Apr 5 bonds; ~1pt intraday ranges on 1, 10, 14, 15, 16 and 20 Apr.
  - FPC0235: 8 Apr +1.43 to 102.10 (ceasefire day, Codziennik 169198). Heavy volume 14 Apr (11,049) and 16 Apr (9,489).
    Then 102.80 -> 100.25 (17/20 -> 29 Apr) on rising volume as oil rose again.
  - FPC0332: 1 Apr 94.55 (-1.05) then 95.30; 9 Apr low 94.55 vs close 95.75. 13 and 14 Apr each had one trade at 95.90 (223 vs 224 bonds; distinct trades with different turnover).
- Coupons: no coupon date in the window for the six; accrued interest rises monotonically; FPC0332 stays at 3.72%.
- New lines: NONE in April. The BGK (PL00005...) and PFR sets are identical to 31 Mar in every file.
  BGK: FPC0229/0231/0235/0328/0332/0342/0427/0630/0631/0733/1140, BGK1127, FPU1130, FWA0931, IWS0645. PFR: PFR0330/0627/0827/0927, PF10927.
  No FWSZ-named line exists; FWA0931 (BGK floater, reset to 3.80% on 15 Mar) predates April.
  Only state-related addition: the Treasury bond DS0436 (PL0000119087), listed from 28 Apr. OK0426 was last listed 21 Apr.

## Other observations (genuine, in source)
- RPP held at 3.75% on 9 Apr (Codziennik 10 Apr, 169219). WIBOR was flat all month: 3M 3.84-3.87, 6M 3.87-3.90, 1Y 3.88-3.94, 1M 3.74-3.82, SW 3.76-3.84.
  ON ranged 3.57-3.79 (peak 15 Apr 3.79 = 1M).
- POLSTR month-end dip: index 31 Mar 3.024 / WIRON 2.218 (30 Mar 3.414/3.269). The spec builder's month-end rule will fall back to 30 Mar.
  WIRON also printed low on 24 Apr (2.988) and 29 Apr (2.941).
- BUBOR fell after the 12 Apr Hungarian election (Orban's party lost; forint +2.5-3%, Codziennik 169225/169244): 6.38/6.52/6.68 (10 Apr) -> 6.30/6.38/6.48 (13 Apr) -> 6.25/6.25/6.31 from 24 Apr.
  MNB held at 6.25% on 28 Apr, hawkish (Codziennik 29 Apr, 169385).
- EURIBOR 12M: 2.870 (31 Mar), 2.872 (7 Apr), 2.860 (8 Apr), 2.680 (9 Apr), 2.640 (22 Apr), 2.765 (29 Apr).
- PRIBOR 1Y: 3.71 -> 3.64 (16-21 Apr) -> 3.74 (29 Apr); 3M is flat at 3.56-3.57.
- GPWB operational communique of 2 Apr 13:14: the 10:15 bond-index values on 2 Apr used 1 Apr TBSP prices (no TBSP fixing). For curve/TBSP agents.

## POLSTR publication (d+1 convention on the GPWB calendar, timestamps not verified)
27.03->30.03, 30->31.03, 31.03->01.04, 01->02, 02->03 (Good Friday, GPWB open), 03->07 (6 Apr Easter Monday), 07->08, 08->09, 09->10, 10->13, 13->14, 14->15,
15->16, 16->17, 17->20, 20->21, 21->22, 22->23, 23->24, 24->27, 27->28, 28->29, 29->30 Apr (30 Apr is after the last C).

## Gaps
None. Every field for every C has a value.
Single-source fields: WIBOR 1Y, NBP CHF, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
The Codziennik cross-check for C=13 Apr (stale 14 Apr issue) and C=22 Apr (no 23 Apr issue) is indirect, through the change column of the following issue.
