# Working notes: Mar 2026 curves, part 1 (R 2-6, 9-13, 16 Mar; C 27 Feb, 2-6 Mar, 9-13 Mar)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-02/research/curves_pap_1.json: six PAP columns per row,
live/after_C/intraday_on_C flags, d1, c_close, and the optional keys `flags`, `irs_gap_note` and `pap_close.note`.
Key sets and key order are checked programmatically against curves_pap_1.json (top level, irs_src, pap_table, pap_close, rows and row keys); they are identical.
Raw parses: erste_raw_all.json (26 Feb to 17 Mar dailies), paptab_raw.json (PAP tables 26 Feb to 23 Mar), fx_raw.json, xcheck_obs.json.
Downloads: dl/erste (PDF, pdftotext -layout output, archiwum.html), dl/si (PAP tables), dl/si/fx (FX/FI notes + fx_slugs.txt), dl/si/list (listing pages 438-472).
Scripts: scripts/. erste.py, paptab.py, fxparse.py, h2t.py and stale.py are copied unchanged from the Feb part-2 run. xcheck_mar2.py and build_mar.py are new (xcheck_mar.py is a first pass, superseded).
Renders: render/ (page 2 of the 6, 9, 13 and 16 Mar dailies).

## Sources / access (all fetched 27 Nov 2026, all HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum) has one daily per business day. The ids are:
  26-02 169121, 27-02 169122, 02-03 169124, 03-03 169129, 04-03 169132, 05-03 169135, 06-03 169139, 09-03 169141, 10-03 169147,
  11-03 169154, 12-03 169158, 13-03 169159, 16-03 169162, 17-03 169167. URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL.
  All are 3-page PDFs. The 27 Feb and 2 Mar PDFs are byte-identical to the Feb part-2 run's copies.
- strefainwestorow listing (27 Nov 2026): 26 Feb = p.470-471; 27 Feb = 468-470; 2 Mar = 466-468; 3 Mar = 463-466; 4 Mar = 460-463; 5 Mar = 458-460;
  6 Mar = 456-458; 9 Mar = 453-456; 10 Mar = 451-453; 11 Mar = 448-451; 12 Mar = 446-448; 13 Mar = 444-446; 16 Mar = 441-444.
- PAP table: one edition per weekday. 28 Feb, 1, 7, 8, 14 and 15 Mar returned 404, so there are no weekend editions.
- NBP API (api.nbp.pl, table A) was used only to identify the fixing in the stale 9 Mar FX block: EUR 6 Mar 4.2782, USD 3.6962 (045/A/NBP/2026). No value was taken from it.

## A. Erste tables (main values in curves.json)
- For 10 of 11 R the R-dated daily exists and both its "Rynek stopy procentowej" header and its FX "Poprzednia sesja" header equal C. No fallback was needed.
  Header format: dd.mm.yyyy up to 06 Mar, dd/mm/yyyy 09-13 Mar, dd.mm.yyyy again from 16 Mar. Number format: decimal commas in the 2, 3, 5 and 6 Mar dailies; the parser handles both.
- **R 9 Mar (C 6 Mar): HEADER MISMATCH.** The 9 Mar daily heads both tables **05/03/2026**. No daily anywhere carries a 06.03 header (6 Mar daily = 05.03.2026, 10 Mar daily = 09/03/2026), so the
  "first daily after C with a table headed C" fallback yields nothing. What the 9 Mar daily contains:
  - IRS (PL/US/EZ) and FRA tables: **new** data, not the 05.03 tables. Every level differs from the 6 Mar daily and the change columns match the differences within 1bp. The 10 Mar daily's change columns are consistent with these levels as its prior session.
    The same daily's bond table (OK0128 4.01(+24), PS0131 4.91(+18), DS1035 5.57(+18)) matches the C-dated PAP 16:29 note (3.96/4.88/5.58) and the BBG PL row stamped 06.03 (3.97/4.86/5.55). The page-2 charts end at "6 mar" (render/p260309-2.png).
    **Kept** as the 6 Mar session with header_date recorded as printed ("05/03/2026") and flagged. Null them if a strict header match is required.
  - FX "Poprzednia sesja" block: **STALE**. EURPLN/USDPLN/EURUSD min/max/open/close are identical to the 05.03 block; only the fixings changed, to the NBP 6 Mar fixings.
    eurpln_close = 4.2733 is the **5 Mar** close (kept as published, flagged). The only C-dated EUR/PLN is pap_close.eurpln 4.2769 (16:29).
  - 10Y-spread column: **STALE** (exact copy of the 05.03 column, change cols included; PL 254(+5)). The CDS column changed (PL 55 -> 56), so cds5y is not stale.
- PDF CreationDate (UTC) / URL upload stamp (CET). All were created on the morning of R:
  02 Mar 07:07:20Z / 08:32:25; 03 Mar 07:04:12Z / 08:20:56; 04 Mar 07:55:37Z / 09:08:01; 05 Mar 07:23:53Z / 08:27:04; 06 Mar 07:12:48Z / 08:25:11;
  09 Mar 07:42:28Z / 08:58:21; 10 Mar 07:48:06Z / 08:55:43; 11 Mar 07:31:48Z / 08:51:49; 12 Mar 07:47:30Z / 08:48:26; 13 Mar 07:15:04Z / 08:33:13; 16 Mar 07:54:46Z / 09:01:46.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set for every R.
- The IRS (PL/US/EZ) and FRA change columns match the day-on-day level differences within ±1bp for every transition from 25.02 through 16.03, including 05.03 -> "05/03" (9 Mar daily) -> 09/03.
- No IRS or FRA table is an exact copy of the previous day's. No CDS column is an exact copy either. The CDS change column is always 0 even when the level moves, so it is unreliable, as in earlier runs.

### Staleness and suspicious items
- **9 Mar daily (headed 05/03): STALE FX session block and STALE 10Y-spread column** (see above). Flagged in R 2026-03-09.
- **16 Mar daily (headed 13.03): STALE 10Y-spread column.** It is an exact copy of the 13 Mar daily's 12/03 column for all 7 countries, change columns included:
  PL 273(+19), FR 67(+3), HU 425(+3), ES 50(+4), IT 79(+8), PT 46(+4), IE 31(0). Confirmed on render/p260316-2.png. The CDS column changed (PL 57 -> 58, IT 12 -> 14). Flagged in R 2026-03-16.
- 10 Mar daily (headed 09/03): the spread change column does not match the previous printed (stale) levels (PL 277(+6) vs 254 = +23; HU 456(+40) vs 391 = +65). It implies an unprinted 6 Mar baseline. Flagged as a note.
- **12 Mar daily (headed 11/03): suspicious PL spread 243(-7)**, against a BBG gap that rose 250 -> 253. That is Erste -10bp vs BBG, against a usual 0 to +4. ES and IT also show -7. The 13 Mar daily's change column implies 11 Mar PL 254, ES 46 and IT 71. Not a copy. Kept and flagged.
- 13 Mar daily (headed 12/03): the spread change column does not match the 11/03 levels for PL/ES/IT (+19 vs +30, +4 vs +12, +8 vs +20), consistent with the item above. Flagged as a note.
- Erste PL-Bund spread vs PAP/BBG PL10Y-DE10Y gap: 27.02 230/229; 02.03 236/233; 03.03 248/248; 04.03 249/246; 05.03 254/253; 06.03 254 (stale)/269; 09.03 277/274; 10.03 250/250;
  11.03 243 (!)/253; 12.03 273/269; 13.03 273 (stale)/277.
- Not flagged in the JSON (printed, change cols consistent, kept as published): odd USD IRS 10Y prints in the 10 Mar daily (10Y 3.92(-6) while 8Y 3.85(+1)) and the 12 Mar daily (10Y 4.07(+9) while 8Y 3.92(+1)),
  and the EZ 3Y in the 10 Mar daily (2.49(-5), below the 2Y at 2.51).
- The Erste bond table (not requested) drops DS1035 under pdftotext in the 9 and 13 Mar dailies (parsed as "2.0"; the render shows 5.57 on 9 Mar). Not used.
- EUR/PLN close, Erste vs PAP last quote: 27.02 4.2231/4.2206 (17:07); 02.03 4.2404/4.2403 (16:56); 03.03 4.2913/4.3020 (16:50, volatile, Erste max 4.3078); 04.03 4.2668/4.2717 (15:40);
  05.03 4.2733/4.2710 (16:40); 06.03 4.2733 (stale = 5 Mar)/4.2769 (16:29); 09.03 4.2740/4.2773 (14:24); 10.03 4.2578/4.2565; 11.03 4.2520/4.2492; 12.03 4.2664/4.2687; 13.03 4.2742/4.2764 (17:15).
- Session fixings printed with 3 decimals are stored as numbers (e.g. EURPLN 11/03 "4.274").

## B. PAP/Bloomberg tables
- Columns are current, 1D, 5D, 1M, 3M, 12M (array order as before).
- Editions with per-row stamps: 2 Mar (06:39), 3 (06:39), 4 (06:35), 5 (06:35), 9 (06:33), 10 (06:34), 11 (06:48), 12 (06:36) and 16 (06:38).
  In each of them all 11 EU/CEE/TR rows are stamped exactly C, and US/JP carry morning-of-R clock stamps (live), so d1 is used.
- **6 Mar edition (07:37): no stamp column.**
  - EU/CEE rows, and TR 5Y/10Y: current = C (5 Mar) close, confirmed by the 9 Mar edition 1D col and the 13 Mar edition 5D col.
  - **TR 2Y is live:** current 34.29 is not the 5 Mar close. Its 1D col 34.54 is the 5 Mar close, and its 5D col 33.58 is the 27 Feb close, i.e. the series is shifted one day (07:37 CET = 09:37 Istanbul).
    TR c_close is mixed: 34.54 (1D) / 31.40 / 28.35 (current). The d1 holds y2 only. live=true. Flagged in R 2026-03-06.
  - US row is dated 6 Mar: its 5D col is the 27 Feb close. current = 1D (no move by 07:37). d1 = 3.58/3.73/4.14, confirmed by the 12 Mar edition 5D col.
  - JP current is the 6 Mar value (15:37 JST), so it is after C. d1 = 1.26/1.62/2.16, confirmed by the 12 Mar edition 5D col.
- **13 Mar edition (07:14): no stamp column.**
  - EU/CEE/TR current = C (12 Mar) close, confirmed by the 16 Mar edition 1D col and the 20 Mar edition 5D col.
  - US is live (5D col = 6 Mar close; current differs from the 1D col). d1 = 3.74/3.87/4.26.
  - JP current is a 13 Mar intraday value (15:14 JST). d1 = 1.27/1.63/2.19.
  - Both d1s are confirmed by the 19 and 20 Mar edition 5D cols.
- The 20 Mar edition (07:05, unstamped, outside the window) has EU rows = 19 Mar close. Its US/JP rows are dated 19 Mar (their 1D/5D cols equal the 19 Mar edition's), so its 5D col is the 12 Mar close.
  As a result, **the US/JP 13 Mar closes (R 16 d1) are seen only once** (16 Mar edition 1D col). Noted in those rows.
- The rule about editions between C and R was **not triggered**. No R edition has EU rows stamped later than C, and there are no weekend editions. after_C is false everywhere and intraday_on_C is false everywhere.
- Full cross-check (scripts/xcheck_mar2.py, editions 26 Feb to 23 Mar, with per-row dating for the unstamped editions): for every C, all 39 country/tenor series have 0 conflicts.
  All have 2 or more observations, except US/JP on 13 Mar. build_mar.py asserts that every c_close equals the cross-edition consensus.
  The Feb part-2 note "TR 2Y for 26 Feb is 33.46 twice but 33.58 in the 6 Mar 5D column" is explained by the live TR 2Y row above: 33.58 is the 27 Feb close.
- No unchanged rows (all three tenors equal to the previous close) were found for any C. There are no US, JP, UK, TR or PL holidays on any C.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 27.02 3.54/4.25/4.93 vs 3.51/4.24/4.93; 02.03 3.64/4.38/5.04 vs 3.61/4.36/5.03; 03.03 3.82/4.58/5.23 vs 3.79/4.56/5.22;
  04.03 3.69/4.54/5.21 vs 3.66/4.51/5.19 (PAP 15:40); 05.03 3.78/4.70/5.37 vs 3.75/4.66/5.35; 06.03 3.97/4.86/5.55 vs 3.96/4.88/5.58; 09.03 4.05/4.92/5.60 vs 4.16/5.04/5.72 (PAP 14:24, **not a close**);
  10.03 3.81/4.67/5.34 vs 3.81/4.65/5.33; 11.03 3.99/4.80/5.46 vs 3.99/4.78/5.45; 12.03 4.31/5.02/5.65 vs 4.29/5.01/5.64; 13.03 4.50/5.19/5.75 vs 4.47/5.15/5.75.

## C. PAP Dzień na FX/FI (afternoon piece on C)
Only the quote tables were used; the commentary was not. The URLs are in curves.json under pap_close.url.

| C | published | quotes | EURPLN | USDPLN | OK0128 | PS0131 | DS1035 |
|---|---|---|---|---|---|---|---|
| 27.02 | 17:18 | 17:07 | 4.2206 | 3.5724 | 3.51 | 4.24 | 4.93 |
| 02.03 | 17:39 | 16:56 | 4.2403 | 3.6295 | 3.61 | 4.36 | 5.03 | (3 pieces: 07:14 no table, 09:42, 17:39)
| 03.03 | 17:19 | 16:50 | 4.3020 | 3.7163 | 3.79 | 4.56 | 5.22 |
| 04.03 | 15:59 | 15:40 | 4.2717 | 3.6733 | 3.66 | 4.51 | 5.19 | (RPP day; early; no later piece)
| 05.03 | 16:57 | 16:40 | 4.2710 | 3.6893 | 3.75 | 4.66 | 5.35 |
| 06.03 | 16:45 | 16:29 | 4.2769 | 3.6952 | 3.96 | 4.88 | 5.58 |
| 09.03 | 14:33 | 14:24 | 4.2773 | 3.6976 | 4.16 | 5.04 | 5.72 | (early; no later piece; NOT a close, BBG close 11-12bp lower)
| 10.03 | 17:04 | 16:54 | 4.2565 | 3.6542 | 3.81 | 4.65 | 5.33 |
| 11.03 | 17:09 | 16:53 | 4.2492 | 3.6720 | 3.99 | 4.78 | 5.45 |
| 12.03 | 17:13 | 16:56 | 4.2687 | 3.7052 | 4.29 | 5.01 | 5.64 |
| 13.03 | 17:35 | 17:15 | 4.2764 | 3.7383 | 4.47 | 5.15 | 5.75 |
- The early-piece status of 4 and 9 Mar is confirmed by the next-morning tables: 5 Mar "czwartek 09:19 / środa 15:40 / środa 09:11" and 10 Mar "wtorek 09:20 / poniedziałek 14:24 / poniedziałek 09:55".
  The next-morning commentary was not used.

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- No C-dated Erste EUR/PLN close or PL-Bund spread for C = 6 Mar (stale copies of 5 Mar kept and flagged), and none for the PL-Bund spread for C = 13 Mar (stale copy of 12 Mar kept and flagged).
- The Erste IRS/FRA for C = 6 Mar are not headed C (headed 05/03); kept as the 6 Mar session on the evidence above, and flagged.
- PAP close for C = 9 Mar exists only as a 14:24 quote; for C = 4 Mar only as a 15:40 quote.
- No values are null other than IRS 7Y. Nothing was filled from memory.
