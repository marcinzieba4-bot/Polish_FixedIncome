# Working notes: Jan 2026 fixings, part 2 (C = 15,16,19,20,21,22,23,26,27,28,29 Jan 2026)
All pages fetched 2026-11-26. Later-published pages used only to read the row dated C.
Output: fixings.json (same folder). Builder: bin/build.py (-> core.json) + bin/finalize.py. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip `<!-- -->` first). Header: WIBID ON,1M,3M,6M,SW | WIBOR ON,1M,3M,6M,1Y,SW.
  Rolling table still starts at 2026-01-02. (ON/SW show '-' in Nov 2026 rows; Jan rows complete.)
  Cross-check: Santander/Erste Codziennik issued C+1, "Stawki WIBOR" table (no 1Y), labelled C:
  C -> erste id: 15->168993, 16->168995, 19->168998, 20->169000, 21->169002, 22->169004, 23->169007,
  26->169011, 27->169014, 28->169015, 29->169016. URL pattern:
  https://www.erste.pl/regulation_file_server/time20260105150318/download?id=<id>&lang=pl_PL
  ON/SW/1M/3M/6M match GPWB on all 11 dates.
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione, "Data wskaźnika" = index date. Cols: POLSTR, comp 1M/3M/6M, CI, '', WIRON, comp 1M/3M/6M.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-01-12&endPeriod=2026-01-30 ("Stand vom 25.11.2026").
- PRIBOR: CNB year.txt?year=2026, split "|": idx 12=3M, 14=6M, 18=1Y (date format "15 Jan 2026").
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (row 1 English header; col 6=3M, 9=6M, 15=12M).
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-01-14/2026-01-30/?format=json (tables 009..019/A/NBP/2026).
  EUR/USD cross-checked vs Codziennik "Poprzednia sesja na rynku FX <C>" fixing column: all match.
- Catalyst PRIMARY (new): official GPW daily stats
  https://gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls (Jan 2026 files are .xls; recent ones .xlsx).
  List per month: POST year=2026&month=01 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL.
  Sheet "instrumenty": col 11 close, 12 reference, 14 open, 15 low, 16 high, 17 last, 18 avg, 19 #trades, 20 vol (szt.),
  21 value (thous. PLN), 22/23 block vol/value. Each file saved on C at ~17:28 (point-in-time).
- Catalyst cross-check: https://www.biznesradar.pl/notowania-historyczne/FPCxxxx[,N] pages 1-7. OHLC+vol identical on all traded bond-days.

## Access tips (new)
- gpwbenchmark.pl "empty reply" is triggered by a browser-like User-Agent; plain curl (default UA) works. Same for gpwcatalyst.pl,
  which the H1 run reported as unreachable: it works with default curl UA.
- stooq.pl: still connection reset.

## Catalyst findings
- Nominal is 1,000 PLN per bond (official file). biznesradar "Obrót" = vol x price(%) -> 10.0-10.6x below official value
  (which also includes accrued interest). H1 turnover_pln (from biznesradar) is understated ~10x; H1 "100 PLN nominal" note is wrong.
  Here turnover_pln = official value x 1000.
- No-trade days (official #trades=0; closing = reference price = last trade close):
  FPC0229 15,16,19 Jan (last 14 Jan, 104.10, 1,100); FPC0231 15-22 Jan (last 14 Jan, 105.00, 9), 26-27 Jan (last 23 Jan, 105.48, 20),
  29 Jan (last 28 Jan, 105.50, 8); FPC0733 23 Jan (last 22 Jan, 83.20, 10); FPC0332 27 Jan (last 26 Jan, 96.10, 489).
- FPC0332 = PL0000500476, issuer BGK (per GPW file), 4.70% current coupon, matures 2032-03-03; trades on 10 of 11 C.
- No block/off-session trades in any FPC on any C.
- Thin/suspicious: FPC0229 21 Jan 10,993 and 22 Jan exactly 10,000 bonds; FPC0630 16 Jan 4 bonds at 90.59;
  FPC0733 19 Jan +1.34 pts (82.61->83.99) on 1,125 bonds, 28 Jan 1 bond; FPC0231 very illiquid.
- H1 flag FPC0733 14/15 Jan near-identical rows: official shows 5 vs 11 trades, 599.65k vs 589.69k PLN, so genuine.

## Overlap checks vs H1 fixings.json (14 Jan and earlier)
- WIBOR 14 Jan, POLSTR/WIRON 14 Jan, EURIBOR/PRIBOR 12-14 Jan, NBP 14 Jan, Catalyst 14 Jan OHLCV: identical.

## POLSTR publication (d+1 convention, timestamps not verified)
14->15, 15->16, 16->19, 19->20, 20->21, 21->22, 22->23, 23->26, 26->27, 27->28, 28->29, 29->30 Jan.

## Gaps
None. Single-source fields: WIBOR 1Y, CHF fixing, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
