# Working notes: Feb 2026 fixings (C = 30 Jan; 2,3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26 Feb 2026)
All pages fetched 2026-11-26. Later-published pages used only to read the row dated C.
Output: fixings.json (same folder), same schema as 2026-01-H2/research/fixings.json (checked by script: identical key sets, no nulls).
Builder: bin/build.py (-> core.json, all cross-checks) + bin/finalize.py (adds notes). Parsers: bin/parse_gpwb.py, bin/cat_official.py. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip `<!-- -->` first). Header: WIBID ON,1M,3M,6M,SW | WIBOR ON,1M,3M,6M,1Y,SW.
  Rolling table still runs 2026-01-02..2026-11-24, so all Feb rows present.
  Cross-check: Santander/Erste Codziennik issued C+1, "Stawki WIBOR" table (no 1Y), labelled C.
  Ids taken from https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum (archive page lists all issues with timestamps):
  C -> id: 30.01->169019, 02.02->169025, 03->169027, 04->169031, 05->169034, 06->169043, 09->169046, 10->169047,
  11->169049, 12->169051, 13->169057, 16->169060, 17->169080, 18->169081, 19->169083, 20->169087, 23->169091,
  24->169120, 25->169121, 26->169122.
  URL: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL (timestamp from archive).
  ON/SW/1M/3M/6M match GPWB on all 20 dates. "Poprzednia sesja na rynku FX" label = C on all 20 (format varies 06/02/2026 vs 05.02.2026).
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione, "Data wskaźnika" = index date. Cols: POLSTR, comp 1M/3M/6M, CI, '', WIRON, comp 1M/3M/6M.
  All 21 index dates 2026-01-29..2026-02-26 present. 29 Jan identical to H2 file.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-01-26&endPeriod=2026-03-03 ("Stand vom 26.11.2026 13:24").
  29 Jan identical to H2 file.
- PRIBOR: CNB year.txt?year=2026, split "|": idx 12=3M, 14=6M, 18=1Y.
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (col 6=3M, 9=6M, 15=12M). Every C is a HU fixing day.
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-01-28/2026-02-27/?format=json (tables 020..039/A/NBP/2026 for the C dates).
  EUR/USD = Codziennik fixing column on all 20 dates.
- Catalyst PRIMARY: https://gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls (Feb files still .xls).
  Month list: POST year=2026&month=02 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL (all 20 Feb sessions listed).
  Sheet "instrumenty" layout unchanged. Header date = C in all files. Internal "Last Saved" = C, 17:27-18:59 (25 Feb 18:59, 26 Feb 18:10, others ~17:27-17:33).
  catalyst_20260217.xls: HTTP Last-Modified 2026-02-18 08:08 UTC (uploaded next morning) but internal save 17 Feb 17:28; content consistent with biznesradar.
  Jan 14-29 files copied from the H2 run for last-trade lookback.
- Catalyst cross-check: https://www.biznesradar.pl/notowania-historyczne/FPCxxxx[,N] pages 1-8. OHLC+vol identical on all 93 traded bond-days;
  every one of 27 no-trade bond-days is a missing biznesradar row; last-trade dates from official files alone = biznesradar.

## Access
- Same as H2 run: plain curl default UA works for gpwbenchmark.pl and gpwcatalyst.pl. Everything else HTTP 200 first try.

## Catalyst findings
- Units unchanged: nominal 1,000 PLN; turnover_pln = official value (thous.) x 1000; biznesradar Obrót 10.00-10.23x smaller.
- No block / off-session FPC trades on any C.
- No-trade days (official #trades=0; closing = reference = last trade close):
  FPC0231: 30 Jan, 2, 3 Feb (last 28 Jan, 105.50, 8); 6-26 Feb, 14 sessions (last 5 Feb, 105.25, 299). Traded only 4 Feb (2 bonds) and 5 Feb.
  FPC0229: 10, 11 Feb (last 9 Feb, 104.90, 18). FPC0630: 4 Feb (last 3 Feb, 91.60, 66); 17 Feb (last 16 Feb, 92.06, 1,434).
  FPC0733: 6 Feb (last 5 Feb, 83.70, 480); 11 Feb (last 10 Feb, 84.44, 44); 18 Feb (last 17 Feb, 85.00, 54); 20, 23 Feb (last 19 Feb, 85.18, 6).
  FPC0235, FPC0332: traded every C.
- Thin/suspicious:
  FPC0229 2 Feb: 2 trades, 2 bonds, open=high 106.70, close 104.86 (off-market print).
  FPC0630 9 Feb open=high 93.05 -> close 91.61; 10 Feb low 90.56 -> close 91.95.
  FPC0733 30 Jan O 84.59 H 85.00 C 84.00 (36 bonds); 12 Feb 83.60 -> 13 Feb 84.38 on 3 bonds; 1-trade days of 2-6 bonds on 13, 19, 25, 26 Feb.
  Big volume: FPC0235 9 Feb 11,177 bonds (11.84m PLN, 31 trades), 26 Feb 5,023; FPC0332 17 Feb 5,100, 18 Feb 3,457; FPC0733 4 Feb 2,068; FPC0630 30 Jan 2,905.
- FPC0229/FPC0231/FPC0235 mature 3 Feb 2029/2031/2035, so coupon date 3 Feb 2026 is inside the window (clean prices, no jump seen).
  ISINs: FPC0229 PL0000500443, FPC0630 PL0000500278, FPC0231 PL0000500450, FPC0733 PL0000500294, FPC0235 PL0000500468, FPC0332 PL0000500476.

## Other observations (genuine, in source)
- Month-end: WIBOR ON 30 Jan 3.82 (-20bp); POLSTR index 30 Jan 3.149, WIRON 2.388; WIRON index 2 Feb 2.983.
- BUBOR 25 Feb step (-9/-10bp): MNB cut 25bp to 6.25% on 24 Feb (Erste Codziennik 25 Feb, id 169120: "Węgierski bank centralny obniżył stopy procentowe o 25 pb, główną do 6,25%").
- Codziennik CHFPLN quote is a morning spot figure, stale at 4.5236 in the 2-6 Feb issues; not a usable CHF fixing check.

## POLSTR publication (d+1 convention, timestamps not verified)
29.01->30.01, 30.01->02.02, 02->03, 03->04, 04->05, 05->06, 06->09, 09->10, 10->11, 11->12, 12->13, 13->16, 16->17, 17->18,
18->19, 19->20, 20->23, 23->24, 24->25, 25->26, 26->27 Feb (27 Feb is after the last C).

## Gaps
None. Single-source fields: WIBOR 1Y, NBP CHF, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
