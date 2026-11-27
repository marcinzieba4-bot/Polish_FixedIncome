# Working notes: Mar 2026 fixings (C = 27 Feb; 2,3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30 Mar 2026)
All pages fetched 2026-11-27. Later-published pages used only to read the row dated C.
Output: fixings.json (same folder), same schema as 2026-02/research/fixings.json (checked by script: identical key sets at every level, no nulls).
Builder: bin/build.py (-> core.json, all cross-checks) + bin/finalize.py (adds notes). Parsers: bin/parse_gpwb.py, bin/cat_official.py (copied from the Feb run). Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip `<!-- -->` first). First request returned HTTP 500 ("problemy techniczne"); the retry a few seconds later returned 200.
  Header: WIBID ON,1M,3M,6M,SW | WIBOR ON,1M,3M,6M,1Y,SW. Rolling table runs 2026-01-02..2026-11-25.
  Cross-check: Santander/Erste Codziennik issued C+1, "Stawki WIBOR" table (no 1Y).
  C -> id (archive https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum):
  27.02->169124, 02.03->169129, 03->169132, 04->169135, 05->169139, 06->169141, 09->169147, 10->169154, 11->169158,
  12->169159, 13->169162, 16->169167, 17->169170, 18->169171, 19->169173, 20->169175, 23->169179, 24->169180,
  25->169183, 26->169184, 27->169186, 30->169188.
  URL: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL (timestamp from archive).
  ON/SW/1M/3M/6M match GPWB on all 22 dates. "Poprzednia sesja na rynku FX" and "Rynek stopy procentowej" labels = C on 21/22.
  EXCEPTION: the 9 Mar issue (169141, C=6 Mar) is labelled 05/03/2026, and its FX min/max/open/close are copied from the 6 Mar issue.
  Its WIBOR table (ON 3.90, change +19) and fixing column (EUR 4.2782, USD 3.6962) ARE the 6 Mar values, so the label is stale but the rates are not.
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione, "Data wskaźnika" = index date. Cols: POLSTR, comp 1M/3M/6M, CI, '', WIRON, comp 1M/3M/6M.
  The page is byte-identical to the 2026-11-26 download (latest index 2026-11-19). All 23 index dates 2026-02-26..2026-03-30 are present. 26 Feb is identical to the Feb file.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-02-20&endPeriod=2026-04-03 ("Stand vom 26.11.2026 13:24").
  26 Feb identical to Feb file.
- PRIBOR: CNB year.txt?year=2026, split "|": idx 12=3M, 14=6M, 18=1Y. File is identical to the 26 Nov download (last row 19 Nov). 26 Feb identical to Feb file.
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (col 6=3M, 9=6M, 15=12M). Every C is a HU fixing day (15 Mar = Sunday).
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-02-25/2026-03-31/?format=json (tables 040..061/A/NBP/2026 for the C dates).
  EUR/USD match the Codziennik fixing column on all 22 dates. 26 Feb identical to Feb file.
- Catalyst PRIMARY: https://gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls (Mar files still .xls).
  Month list: POST year=2026&month=02|03 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL (27 Feb + all 22 Mar sessions listed).
  Sheet "instrumenty" layout unchanged. Header date = C in all 22 files.
  HTTP Last-Modified is on C, 16:46-20:06 UTC (23 Mar 20:06 is the latest). Internal "Last Saved" (`file`) is on C, 16:26-18:17 UTC.
  The 30 Mar 16:26 save is the same local time as the others: DST began on 29 Mar.
  Jan 14 - Feb 26 official files were copied from the Feb run for last-trade lookback.
- Catalyst cross-check: https://www.biznesradar.pl/notowania-historyczne/FPCxxxx[,N] pages 1-8 (coverage back to 2024/2025 for all bonds).
  OHLC+vol identical on all 103 traded bond-days. Each of the 29 no-trade bond-days has no biznesradar row.
  Last-trade dates from the official files alone match biznesradar.

## Access
- Same as before: plain curl with the default UA works for gpwbenchmark.pl and gpwcatalyst.pl. gpwbenchmark dane-opoznione returned one transient 500. Everything else returned HTTP 200 on the first try.

## Catalyst findings
- Units unchanged: nominal 1,000 PLN; turnover_pln = official value (thous.) x 1000; biznesradar Obrót is 10.00-10.24x smaller.
- No block / off-session FPC trades on any C.
- No-trade days (official #trades=0; closing = reference = last trade close):
  FPC0231: traded only 27 Feb (2,574 bonds, 1 trade, 105.50), 6 Mar (1,100, 104.81), 24 Mar (50, 102.28), 26 Mar (30, 101.00).
    No trade 2-5 Mar (last 27 Feb); 9-23 Mar, 11 sessions (last 6 Mar); 25 Mar (last 24 Mar); 27, 30 Mar (last 26 Mar). 18 bond-days in total.
  FPC0229: 3 Mar (last 2 Mar, 104.90, 127); 9 Mar (last 6 Mar, 103.80, 237); 12 Mar (last 11 Mar, 104.35, 2);
    23 Mar (last 20 Mar, 103.49, 1); 26 Mar (last 25 Mar, 102.25, 354); 30 Mar (last 27 Mar, 101.80, 21).
  FPC0733: 2 Mar (last 27 Feb, 85.48, 742).
  FPC0332: 13 Mar (last 12 Mar, 95.52, 977); 20, 23 Mar (last 19 Mar, 95.50, 5); 26 Mar (last 25 Mar, 95.50, 101).
  FPC0630, FPC0235: traded every C.
- Thin/suspicious:
  FPC0231 stale 104.81 for 9-23 Mar while FPC0235 fell 102.79 -> 100.85; next print 24 Mar 102.28 (-2.53) on 50 bonds.
  FPC0229 13 Mar 1 bond @104.99 (+0.64), 16 Mar 103.55; 17 Mar 3 bonds, open=high 104.99, close 103.65; 19, 20 Mar 1 bond each @103.49.
  FPC0733 9 Mar low 80.50; 10 Mar close 83.49 (+2.02, 198 bonds), then 82.95, 82.00; 23 Mar range 80.50-82.80 on 94 bonds; 24 Mar 1 bond.
  FPC0630 2 Mar 4,957 bonds (~17x median), open=high 92.99 -> close 91.70.
  FPC0235 big volumes late Mar: 19 Mar 7,667; 23 Mar 7,765; 26 Mar 10,536; 27 Mar 11,101; 30 Mar 6,220 (median 2,107). Price 106.30 (27 Feb) -> 100.09 (30 Mar).
  FPC0332 27 Feb 5,266 bonds (~20x median); 9 Mar low 94.55 vs close 95.90.
- FPC0332 is a floater: coupon 4.70% -> 3.72% on 3 Mar (coupon date; maturity 3 Mar 2032). Ex-coupon from 20 Feb (accrued 0.00 to 27 Feb). Clean prices, no jump.
  Other bonds have no coupon date in the window (FPC0229/0231/0235 on 3 Feb, FPC0630 on 5 Jun, FPC0733 on 21 Jul).
  ISINs: FPC0229 PL0000500443, FPC0630 PL0000500278, FPC0231 PL0000500450, FPC0733 PL0000500294, FPC0235 PL0000500468, FPC0332 PL0000500476.

## Other observations (genuine, in source)
- RPP cut 25bp, reference rate to 3.75%, on 4 Mar (Codziennik 5 Mar, 169135: "RPP obniżyła stopy procentowe o 25pb").
  The WIBOR reaction was small:
  3M 3.81 (2 Mar) / 3.80 (4 Mar) / 3.76 (5 Mar) / 3.77 (6 Mar).
  SW 4.01 / 3.92 / 3.96 / 3.94.
  1Y 3.62 / 3.66 / 3.64 / 3.65.
  By 24-30 Mar, 3M was 3.84-3.86, 6M 3.88-3.90 and 1Y 3.91-3.94, while SW was 3.80 and 1M 3.77. Both sources agree.
- WIBOR ON 27 Feb 4.07 (+15bp, month-end). POLSTR index 27 Feb 3.958 / WIRON 2.964. WIRON lows 6 Mar 2.979 and 12 Mar 3.116.
- BUBOR rose from 9 Mar (3M 6.18 -> 6.28; 12M 6.12 -> 6.30) to 6.45/6.61/6.81 on 30 Mar. MNB held at 6.25% on 24 Mar (Codziennik 25 Mar, 169180), so this is market repricing.
- PRIBOR 1Y 3.42 -> 3.71 over the window. CNB held at 3.50% (Codziennik 20 Mar, 169173).
- Context: the Codziennik headlines from 2 Mar cover the Middle East / Iran conflict; all FPC fell during March.

## POLSTR publication (d+1 convention, timestamps not verified)
26.02->27.02, 27.02->02.03, 02->03, 03->04, 04->05, 05->06, 06->09, 09->10, 10->11, 11->12, 12->13, 13->16, 16->17, 17->18,
18->19, 19->20, 20->23, 23->24, 24->25, 25->26, 26->27, 27->30, 30->31 Mar (31 Mar is after the last C).

## Gaps
None. Single-source fields: WIBOR 1Y, NBP CHF, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
