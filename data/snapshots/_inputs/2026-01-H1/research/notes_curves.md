# Working notes: Jan 2026 curves (R 7-15 Jan; C 5, 7, 8, 9, 12, 13, 14 Jan)
Output: curves.json (same folder). Raw parses: erste_raw.json, paptab_raw.json. Downloads: dl/erste, dl/si, dl/alt. Scripts: scripts/.

## Sources / access
- Erste Codziennik archive (full list with ids): https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum
  (link precedes its date label in the HTML; data-item-id = id). Jan 2026 ids: 05-01 168959, 07-01 168963, 08-01 168966,
  09-01 168968, 12-01 168976, 13-01 168983, 14-01 168984, 15-01 168985, 16-01 168993.
  Download: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL
- PDF CreationDate (UTC): 07 Jan 07:49:40, 08 Jan 08:15:35, 09 Jan 07:48:12, 12 Jan 07:15:55 (URL upload stamp 13:55),
  13 Jan 07:21:54, 14 Jan 07:17:40, 15 Jan 07:14:52. All on the morning of R.
- Table footnote: "Informacje odnoszą się do stawek kupna na rynku międzybankowym na koniec dnia" = bid, interbank, EOD; source LSEG Datastream.
  IRS tenors: 1,2,3,4,5,8,10 (no 7Y) for PL, US, EZ. FRA: 1x4, 3x6, 6x9, 9x12, 3x9, 6x12. Column order PL | US | EZ checked against the rendered PDF (14 Jan).
- PAP table: https://strefainwestorow.pl/wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela (one edition per day, ~06:35).
- strefainwestorow listing pages (as of 26 Nov 2026): 5 Jan = p.544-545, 7 Jan = 541-543, 8 Jan = 538-541, 9 Jan = 536-538,
  12 Jan = 534-536, 13 Jan = 532-534, 14 Jan = 531-532, 15 Jan = 528-531.

## A. Erste tables (main values in curves.json)
- R 01-07 / C 05.01: GAP. No Erste table headed 05.01.2026. The 5 Jan daily is headed 02.01; there was no daily on 6 Jan (PL holiday); the 7 Jan daily is headed 06.01.2026.
  PKO 7 Jan daily (cdn-netpr.pl, created 07 Jan 06:59Z) is also headed 2026-01-06 and has no IRS/FRA table. DB daily260107pol and Millennium daily260107 return 404 (Millennium has only IRS 2/5/10 with no date header).
  -> main fields null. The 06.01-headed values are kept in `alt_erste_hdr_0601`. In that table all PL IRS, FRA, bond and CDS change columns are 0, which suggests the PL values are the 5 Jan close carried over the holiday (inference only).
  EZ/US IRS moved on 6 Jan, so they are post-C. 5 Jan EZ/US IRS back-computed as value minus change are stored as a labelled derived block. They are not a direct read and are good to about ±1bp because of rounding.
  Check: the change baseline for EZ/US is not 2 Jan (EZ 3Y 2.39 -> 2.35 with -3 implies a 2.38 baseline), so the baseline is 5 Jan.
- Other R: the table header equals C in every case (07.01.2026, 08.01.2026, 09/01/2026, 12/01/2026, 13/01/2026, 14/01/2026).
- Day-to-day changes in the IRS change columns are internally consistent (e.g. US 10Y 4.00 -> 4.05 (+5) -> 4.03 (-2) -> 4.10 (+7) -> 4.09 (-1) -> 4.06 (-3)).

### Suspicious items in the Erste tables
- 14 Jan daily (headed 13/01): the CDS and 10Y-spread table is an exact copy of the 13 Jan daily's 12/01 table for all 8 countries, change columns included (PL 59/235(+4), HU 107/389(-5)...). Suspected stale; flagged in curves.json.
- The CDS change column is always 0 even when the level changes (60 -> 59), so it is unreliable.
- The PL-Bund spread (Erste) is 4-10bp wider than the PL10Y-DE10Y gap from the PAP/Bloomberg table: 07.01 234 vs 231; 08.01 233 vs 227; 09.01 233 vs 226; 12.01 235 vs 229; 13.01 235 vs 225; 14.01 231 vs 228. The benchmarks differ.
- The Erste bond table (OK0128/PS0131/DS1035, not requested) does not match PAP: 07.01 3.80/4.56/5.14 vs PAP 3.71/4.50/5.11; 08.01 3.81/4.57/5.15 vs 3.71/4.51/5.12; 13/01 OK0128 3.77 vs 3.66. Its change columns don't match level differences either. Do not use it.
  pdftotext drops DS1035 in the 14 and 15 Jan dailies, but the rendered page shows 5.12 (-4) on 14 Jan.
- PL IRS barely moved on 7 Jan (2Y 3.54 unchanged, 5Y -1) while PAP shows OK0128 -8bp (3.79 on 5 Jan 15:07 -> 3.71). This is plausible (a bond-led move) but worth noting.
- EURPLN close (Erste) vs PAP late-afternoon: 07.01 4.2091 vs 4.2111 (16:37); 08.01 4.2123 vs 4.2137; 09.01 4.2113 vs 4.2123; 12.01 4.2104 vs 4.2104; 13.01 4.2118 vs 4.2115; 14.01 4.2110 vs 4.2128 (14:47). OK.

## B. PAP/Bloomberg tables
- Columns: current, 1D, 5D, 1M, 3M, 12M (arrays in curves.json in that order; HU uses 3Y).
- 7 Jan ed. (06:41): PL stamped 05.01 (= C). All other EU/CEE/TR rows are stamped 06.01, which is after C, so they are flagged after_C and d1 (= 5 Jan close) is given.
  d1 was verified to equal the current column of the 6 Jan edition. JP/US are stamped 06:35 (live 7 Jan) and their d1 is the 6 Jan close, which is also after C.
  The 5 Jan US/JP closes come from the 6 Jan 06:34 edition's 1D column (US 3.45/3.70/4.16; JP 1.20/1.60/2.13), and the full 6 Jan edition is included as `pap_table_0106_edition`.
- 8 Jan ed. (06:34): rows stamped 07.01; JP/US live at 06:30, so d1 is used.
- 9 Jan ed. (07:04): no stamp column. Cross-check: the 12 Jan edition's 1D equals this edition's current for all EU/CEE/TR rows (so they are the C close).
  For US and JP, the 12 Jan edition's 1D equals this edition's 1D, so the current column was live on 9 Jan. They are flagged live (inferred).
- 12 Jan ed. (06:38): all rows stamped 09.01 incl. US/JP (JP holiday 12 Jan). No live rows.
- 13 Jan ed. (06:41): the stamps are clock times later than the publication time (PL/EU 17:59, CZ 17:32-17:51, HU 14:01, TR 15:32, US 18:00, JP 09:34). So this is a snapshot taken on the evening of C, 12 Jan.
  US at 18:00 CET is mid-session NY, not the close. JP is unchanged from 9 Jan because of the holiday. Flagged intraday_on_C, and the 1D column is 9 Jan.
- 14 Jan ed. (06:35): rows stamped 13.01; JP/US live 06:32, so d1 is used.
- 15 Jan ed. (06:34): rows stamped 14.01; JP/US live at 06:30-06:31, so d1 is used.

## C. PAP Dzień na FX/FI (afternoon/closing piece on C)
| C | published | quotes | EURPLN | OK0128 | PS0131 | DS1035 |
|---|---|---|---|---|---|---|
| 05.01 | 15:15 | 15:07 | 4.2157 | 3.79 | 4.56 | 5.16 | (no later FX/FI piece that day)
| 07.01 | 16:51 | 16:37 | 4.2111 | 3.71 | 4.50 | 5.11 |
| 08.01 | 17:01 | 16:44 | 4.2137 | 3.71 | 4.51 | 5.12 |
| 09.01 | 16:54 | 16:43 | 4.2123 | 3.70 | 4.50 | 5.11 |
| 12.01 | 17:21 | 16:57 | 4.2104 | 3.70 | 4.53 | 5.12 |
| 13.01 | 17:08 | 16:26 | 4.2115 | 3.66 | 4.48 | 5.09 |
| 14.01 | 14:59 | 14:47 | 4.2128 | 3.69 | 4.51 | 5.10 | (RPP day; no later FX/FI piece)

PAP table PL (Bloomberg generic) vs the PAP note: 05.01 3.81/4.56/5.16 vs 3.79/4.56/5.16; 07.01 3.73/4.52/5.12 vs 3.71/4.50/5.11; 08.01 3.74/4.53/5.13 vs 3.71/4.51/5.12;
09.01 3.71/4.52/5.12 vs 3.70/4.50/5.11; 12.01 3.72/4.54/5.13 vs 3.70/4.53/5.12; 13.01 3.71/4.50/5.10 vs 3.66/4.48/5.09 (2Y +5bp!); 14.01 3.71/4.51/5.09 vs 3.69/4.51/5.10.
The Bloomberg 2Y generic is consistently 1-3bp above OK0128 (5bp on 13 Jan).
