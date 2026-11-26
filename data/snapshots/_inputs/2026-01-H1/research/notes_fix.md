# Working notes: Jan 2026 fixings (C = 5,7,8,9,12,13,14 Jan 2026)
All pages fetched 2026-11-26. Later-published pages used only to read the row dated C.
Output: fixings.json (same folder). Builder scripts: bin/build.py, bin/finalize.py. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione. HTML comments hide the TN/2W columns, so strip `<!-- -->` first.
  Live header: WIBID ON,1M,3M,6M,SW | WIBOR ON,1M,3M,6M,1Y,SW. The rolling table still reaches back to 2026-01-02.
  Cross-check: Santander/Erste Codziennik (erste.pl regulation_file_server ids 168963..168985, issued C+1 morning),
  "Stawki WIBOR" table: ON/SW/1M/3M/6M match on every C. That table has no 1Y.
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione, column "Data wskaźnika" = index date. Compound 1M/3M/6M and POLSTR CI also stored.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-01-01&endPeriod=2026-01-16
  (the /rest/download/ path now returns a 301 to /rest/data/; use curl -L).
- PRIBOR: CNB year.txt?year=2026. Split on "|": idx 12=3M, 14=6M, 18=1Y.
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls, sheet "2026" (header row 1 is in English).
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-01-02/2026-01-16/?format=json
- Catalyst: https://www.biznesradar.pl/notowania-historyczne/FPCxxxx[,N] (pages 1-6). Columns: Data, Otwarcie, Max, Min, Zamknięcie, Wolumen (bonds), Obrót (PLN).

## Unreachable
- gpwcatalyst.pl: empty reply. stooq.pl: connection reset. obligacje.pl: no response.
- data.bondspot.pl (BondSpot delayed data, redirected from bondspot.pl/1279): TLS failure.
- nbp.pl: 403.

## NBP reference rate check for 14 Jan
- PAP Biznes, 14.01.2026 14:37 (strefainwestorow): the MPC meeting on 13-14 Jan kept all rates unchanged (ref 4.00, lombard 4.50, deposit 3.50, rediscount 4.05, discount 4.10).
- PAP 14:59 FX/FI piece says the same. Codziennik 15 Jan 08:29: "brak zmiany stopy referencyjnej".
- NBP archive XML (static.nbp.pl): changes took effect on 2025-12-04 (4.00) and 2026-03-05 (3.75), with nothing in January.
- BondSpot /repo page ("Aktualizacja: 23.11.2026") lists only the GC allocation bonds. It has no rates.
=> No reference rate change on 14 Jan 2026 is documented.

## Quirks
- Codziennik 7 Jan labels its previous-session tables "06.01.2026" (a PL holiday), but the values are the 5 Jan fixings (WIBOR and the NBP EUR/USD fixing).
- BUBOR has no 2 Jan 2026 fixing. It does have a fixing on Sat 10 Jan (a HU working Saturday).
- Days with no trade on Catalyst: close is the last trade close, vol=0, traded=false. This is inferred from the missing biznesradar row.
- For thin or suspicious trading, see the notes in fixings.json.

## POLSTR publication (d+1 convention, timestamps not verified)
02->05, 05->07, 07->08, 08->09, 09->12, 12->13, 13->14, 14->15 Jan.
