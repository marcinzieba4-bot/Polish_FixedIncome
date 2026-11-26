# Working notes: Feb 2026 curves (R 16-20, 23-27 Feb; C 13, 16-20, 23-26 Feb)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-01-H2/research/curves_pap.json: six PAP columns per row,
live/after_C/intraday_on_C flags, d1, c_close, and the optional keys `flags`, `irs_gap_note` and `pap_close.note`.
Raw parses: erste_raw_all.json (12 Feb to 2 Mar dailies), paptab_raw.json (PAP tables 12 Feb to 6 Mar), fx_raw.json, xcheck_obs.json.
Downloads: dl/erste (PDF + pdftotext -layout + archiwum.html), dl/si (PAP tables), dl/si/fx (FX/FI notes), dl/si/list (listing pages 464-493). Scripts: scripts/. Renders: render/.

## Sources / access (all fetched 26 Nov 2026, all HTTP 200 unless noted)
- Erste archive ids (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum): 12-02 169049, 13-02 169051, 16-02 169057, 17-02 169060,
  18-02 169080, 19-02 169081, 20-02 169083, 23-02 169087, 24-02 169091, 25-02 169120, 26-02 169121, 27-02 169122, 02-03 169124.
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL.
- The PDFs still carry the Santander Bank Polska logo. The publisher label is kept as in the earlier file.
- Format: from the 23 Feb daily (headed 20.02) on, the tables use decimal commas. The parser handles both formats.
  Verified on the rendered page 2 of the 18 Feb and 24 Feb dailies.
- strefainwestorow listing pages: 13 Feb = p.489-491; 16 Feb = 487-489; 17 Feb = 484-486; 18 Feb = 482-484; 19 Feb = 479-482;
  20 Feb = 478-479; 23 Feb = 475-477; 24 Feb = 473-475; 25 Feb = 470-472; 26 Feb = 468-470; 27 Feb = 466-468.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. One edition per weekday. 14, 15, 21, 22, 28 Feb and 1 Mar returned 404, so there are no weekend editions.
  The first fetch of 26 Feb had a connection reset; the retry returned 200.

## A. Erste tables (main values in curves.json)
- In every case the R-dated daily exists, and its IRS/FRA table ("Rynek stopy procentowej") and its FX "Poprzednia sesja" table are both headed C. No fallback was needed.
- PDF CreationDate (UTC) / URL upload stamp (CET). All were created on the morning of R:
  16 Feb 08:20:08Z / 09:26:27; 17 Feb 07:30:37Z / 08:54:15; 18 Feb 07:45:28Z / 09:04:02; 19 Feb 07:50:00Z / 09:04:31; 20 Feb 07:49:45Z / 09:02:16;
  23 Feb 07:47:23Z / 08:47:54; 24 Feb 05:58:48Z / 07:04:40; 25 Feb 07:52:13Z / 08:53:08; 26 Feb 07:36:05Z / 08:36:53; 27 Feb 07:11:59Z / 08:12:29.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set.
- The IRS (PL/US/EZ) and FRA change columns match the day-on-day level differences within ±1bp for all tables from 12.02 through 27.02.
- No IRS, FRA or FX table is an exact copy of the previous day's.

### Staleness and suspicious items
- **18 Feb daily (headed 17.02): STALE CDS/10Y-spread table.** It is an exact copy of the 17 Feb daily's 16.02 table for all 8 countries, change columns included
  (PL 55(0)/222(+2), HU 94/376(-11), ES 16/44(+6), IT 11/62(+1), IE 9/11(+1)). Confirmed on the rendered PDF page 2 (render/p260218-2.png).
  This is the same failure mode as the 14 Jan and 21 Jan dailies. Flagged in R 2026-02-18.
- 17 Feb daily (headed 16.02): the spread change column is inconsistent with the levels (PL +2 vs 0, HU -11 vs -8, IT +1 vs 0). Flagged as a note.
  C = 16 Feb was a US holiday: the USD IRS levels equal 13.02 except 1Y (+1). Flagged.
- 23 Feb daily (headed 20.02): the spread change column is inconsistent (PL +4 vs +6, HU +2 vs +4, ES -1 vs -2, IT -1 vs 0). Flagged as a note.
- 19 Feb daily (headed 18.02): the IE spread jumps 11 -> 27 (+17). This is probably a benchmark change; it is not PL and not flagged in the JSON.
- The CDS change column is mostly 0 even when the level changes (PL 55 -> 56 -> 55 ...). It is unreliable, as in earlier runs.
- Erste PL-Bund spread vs the PAP/BBG PL10Y-DE10Y gap: 13.02 222/218; 16.02 222/221; 17.02 222(stale)/219; 18.02 221/220; 19.02 221/221;
  20.02 227/225; 23.02 228/227; 24.02 227/225; 25.02 230/223 (7bp, flagged as a note in R 26); 26.02 226/225.
- The Erste bond table (not requested) is erratic against PAP and should not be used. For example, OK0128 24.02 3.42(-14), 25.02 3.55(+14), 26.02 3.59(+15) vs PAP 3.39/3.41/3.48.
- EUR/PLN close, Erste vs PAP last quote: 13.02 4.2116/4.2115 (16:10); 16.02 4.2130/4.2107 (14:19); 17.02 4.2183/4.2180; 18.02 4.2109/4.2144 (16:47; Erste min 4.2100);
  19.02 4.2221/4.2231; 20.02 4.2235/4.2215; 23.02 4.2180/4.2169 (13:34); 24.02 4.2147/4.2181 (16:17; Erste min 4.2145); 25.02 4.2178/4.2201; 26.02 4.2255/4.2230 (16:08). OK.
- Session fixings printed with 3 decimals are stored as printed: EURPLN 13.02 "4.214", 16.02 "4.208", 19.02 "4.222".

## B. PAP/Bloomberg tables
- Columns are current, 1D, 5D, 1M, 3M, 12M. All 10 R editions have per-row stamps:
  16 Feb (06:41), 17 (06:33), 18 (06:34), 19 (06:38), 20 (06:40), 23 (06:40), 24 (06:39), 25 (06:34), 26 (06:34) and 27 (06:34).
  In each of them all EU/CEE/TR rows (11 rows) are stamped exactly C. JP/US carry morning-of-R time stamps (live), so d1 is used for them,
  except in the 23 Feb edition, where **all 13 rows, US and JP included, are stamped 20.02.2026 = C**. That gives no live rows, so the current column is used.
- The rule about editions between C and R was **not triggered**. No R edition has European rows stamped later than C, and there are no weekend editions.
- Full cross-check (scripts/xcheck.py): for every C, all 39 country/tenor series appear 2-3 times across editions (current, 1D, 5D), with 0 conflicts.
  This used editions from 12 Feb to 6 Mar. Exceptions:
  - US/JP on 16 Feb have a single observation each (17 Feb edition 1D).
  - TR 2Y for 26 Feb is 33.46 twice but 33.58 in the 6 Mar 5D column. The 6 Mar edition is unstamped and outside the window.
- Holidays:
  - **16 Feb US (Presidents Day).** In the R 16 edition the US row is stamped 05:24 with current = 1D = 13 Feb close (3.41/3.60/4.05).
    **R 17 (C 16): the US d1 = 13 Feb close**, the last US close before C. Flagged.
  - **23 Feb JP (Emperor's Birthday).** The R 23 edition stamps JP 20.02. **R 24 (C 23): the JP d1 = 20 Feb close (1.26/1.62/2.12)**. Flagged.
- Unchanged rows (all three tenors equal the previous close; each confirmed in 3 editions) are noted in the rows:
  IT and PT on 17.02; IE on 18.02; HU and DE on 19.02; PT on 23.02; IE and DE on 24.02.
- **PL 2Y BBG +10bp on 26 Feb (3.43 -> 3.53)** with 5Y/10Y flat. Confirmed (27 Feb current, 2 Mar 1D, 6 Mar 5D). OK0128 in the PAP note rose +7 (3.41 -> 3.48 at 16:08). Flagged in R 27.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 13.02 3.47/4.26/4.94 vs 3.45/4.24/4.93; 16.02 3.51/4.27/4.96 vs 3.48/4.25/4.95 (PAP 14:19);
  17.02 3.47/4.23/4.93 vs 3.45/4.22/4.92; 18.02 3.49/4.24/4.94 vs 3.44/4.22/4.92 (2Y +5bp); 19.02 3.48/4.25/4.95 vs 3.46/4.24/4.95;
  20.02 3.47/4.28/4.99 vs 3.44/4.27/4.98; 23.02 3.43/4.27/4.98 vs 3.42/4.26/4.97 (PAP 13:34); 24.02 3.41/4.26/4.96 vs 3.39/4.24/4.95;
  25.02 3.43/4.25/4.94 vs 3.41/4.24/4.93; 26.02 3.53/4.25/4.94 vs 3.48/4.23/4.90 (PAP 16:08).

## C. PAP Dzień na FX/FI (afternoon piece on C)
Every C has exactly two "Dzień na FX/FI" pieces, one in the morning and one in the afternoon. Only the quote tables were used; the commentary was not.

| C | published | quotes | EURPLN | USDPLN | OK0128 | PS0131 | DS1035 |
|---|---|---|---|---|---|---|---|
| 13.02 | 16:32 | 16:10 | 4.2115 | 3.5491 | 3.45 | 4.24 | 4.93 |
| 16.02 | 14:30 | 14:19 | 4.2107 | 3.5528 | 3.48 | 4.25 | 4.95 | (early; no later piece; US holiday)
| 17.02 | 17:34 | 17:20 | 4.2180 | 3.5668 | 3.45 | 4.22 | 4.92 |
| 18.02 | 17:05 | 16:47 | 4.2144 | 3.5642 | 3.44 | 4.22 | 4.92 | (MF auction day)
| 19.02 | 16:42 | 16:30 | 4.2231 | 3.5891 | 3.46 | 4.24 | 4.95 |
| 20.02 | 17:26 | 17:00 | 4.2215 | 3.5813 | 3.44 | 4.27 | 4.98 |
| 23.02 | 13:49 | 13:34 | 4.2169 | 3.5799 | 3.42 | 4.26 | 4.97 | (early; no later piece)
| 24.02 | 16:44 | 16:17 | 4.2181 | 3.5842 | 3.39 | 4.24 | 4.95 |
| 25.02 | 17:19 | 16:46 | 4.2201 | 3.5782 | 3.41 | 4.24 | 4.93 | (MF auction day)
| 26.02 | 16:26 | 16:08 | 4.2230 | 3.5757 | 3.48 | 4.23 | 4.90 |
The URLs are in curves.json under pap_close.url.

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- US close for C = 16 Feb and JP close for C = 23 Feb do not exist (holidays). Their c_close is the last close before C, as labelled.
- No other nulls. Nothing was filled from memory.
