# Working notes: Apr 2026 curves, part 2 (R 16, 17, 20-24, 27-30 Apr; C 15-17, 20-24, 27-29 Apr)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-03/research/curves_pap_2.json, checked programmatically. The key signature
covers the top-level keys (minus the optional `flags`), irs, fra, eur_irs, usd_irs, eurpln_session, irs_src, pap_table, pap_close, pap_close.bonds, the
row codes and every row's keys (minus the optional `note`); it is identical for all 11 March R and all 11 April R, and `flags` always follows `irs_gap_note`.
Optional keys used: `flags`, `irs_gap_note`, row `note`, `pap_close.note`. The content-level differences from March:
- R 2026-04-23 has RECONSTRUCTED Erste values (see A).
- From C = 28 Apr the PAP 5Y benchmark is PS0731, so `pap_close.bonds.PS0131` is null and `y5` carries PS0731. `bonds.OK0128` is null throughout, because
  the 2Y benchmark has been WS0428 since 26 Mar. The bonds key set is unchanged.
Raw parses: erste_raw_all.json (13 Apr to 5 May dailies), paptab_raw.json (PAP tables 13 Apr to 8 May), fx_raw.json (FX/FI pieces 10 Apr to 4 May),
xcheck_obs.json (per series/date observations), pdfinfo.json, curves_stage1.json (intermediate).
Downloads: dl/erste (archiwum.html, komentarz_arch.html, ids.tsv, PDF + pdftotext -layout; probe/ = headers of probed unlisted ids), dl/si/tab (PAP tables),
dl/si/fx (FX/FI pieces + fx_slugs.txt), dl/si/list (listing pages 356-396 + all_links.json).
Scripts (new, written for this run because the March scripts were not available): scripts/erste.py (Erste parser), stale.py (copy and change-column
checks), paptab.py, fxparse.py (label-driven; handles "*" benchmark markers), xcheck.py (cross-edition check, dated per tenor), build.py (stage 1),
finalize.py (R 23 reconstruction, flags, notes, key-order and schema asserts vs March). Renders: render/ (page 2 of the 24 Apr and 30 Apr dailies;
spot-checked FX, IRS PL/US/EZ, FRA and CDS/spread against the parse: all match).

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum). The ids by publication date are:
  13-04 169225, 14-04 169244, 15-04 169248, 16-04 169251, 17-04 169254, 20-04 169284, 21-04 169295, 22-04 169321, **23-04 none**, 24-04 169336,
  27-04 169378, 28-04 169382, 29-04 169385, 30-04 169390, 04-05 169396, 05-05 169401.
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. The time part is ignored by the server:
  the same PDF comes back with any or no time part. Server filenames are dzienny2604DD.pdf, except the 13 and 27 Apr dailies (CMS-named).
  The dailies are 3 pages to 24 Apr and 4 pages from 27 Apr. They carry Santander branding to 24 Apr and "Erste Bank Polska" branding from 27 Apr.
- The 13-04 archive entry (169225) has a URL stamp of 2026-04-23 15:05:30 and Last-Modified 23 Apr 13:05:30 GMT, but its content is still the 13 Apr daily
  (CreationDate 13 Apr 07:16:02Z, headed 10/04/2026). This is possibly related to the missing 23 Apr issue; nothing recoverable.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026): 15 Apr = p.388-391; 16 Apr = 386-388; 17 Apr = 384-386;
  20 Apr = 382-384; 21 Apr = 379-382; 22 Apr = 377-379; 23 Apr = 374-377; 24 Apr = 372-374; 27 Apr = 369-372; 28 Apr = 367-369; 29 Apr = 363-367; 30 Apr = 360-363.
  Pages 356-396 were fetched in ascending order. p.374 failed on the first pass (proxy tunnel closed); p.373-375 were refetched together, so no gap.
- PAP table URL: /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. There is one edition per weekday, including Fri 1 May (a PL holiday,
  outside this set). 18, 19, 25 and 26 Apr and 2 and 3 May return 404, so there are no weekend editions. The first fetch of 13 Apr failed (proxy); the retry returned 200.
- Wayback CDX (web.archive.org) is not reachable from here.

## A. Erste tables (main values in curves.json)
- For 10 of 11 R, the R-dated daily exists and both its "Rynek stopy procentowej" header and its FX "Poprzednia sesja" header equal C.
  Header format: dd.mm.yyyy, except the 17 Apr daily (16/04/2026). Decimal points in the 13, 14 and 17 Apr dailies (and 5 May); decimal commas elsewhere.
  The parser handles both. Session fixings printed with 3 decimals are stored as numbers (e.g. EURPLN 15.04 "4,237").
- PDF CreationDate (UTC) / URL upload stamp (CEST). All were created on the morning of R:
  16 Apr 06:42:55Z / 09:11:34; 17 Apr 07:00:25Z / 09:29:04; 20 Apr 06:44:52Z / 08:53:32; 21 Apr 06:17:08Z / 08:29:28; 22 Apr 06:19:48Z / 08:32:08;
  24 Apr 06:06:20Z / 08:17:42; **27 Apr 09:56:19Z / 12:24:09 (late)**; 28 Apr 06:39:07Z / 08:49:00; 29 Apr 06:39:15Z / 09:00:08; 30 Apr 07:14:00Z / 10:30:28 (late).
  The late ones are still the R-dated issue with tables headed C, so they are used as the "Erste Codziennik of R" (as with the late 19 Mar issue in March). Not flagged.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set for every R.
- **First R (16 Apr), compared with the 15 Apr daily (headed 14.04):** every IRS (PL/US/EZ), FRA, spread and bond change column in the 16 Apr daily
  (headed 15.04) matches the day-on-day difference from the 14.04 levels within ±1bp. There are no copies.
- IRS (PL/US/EZ), FRA, PL-Bund spread and bond change columns match the day-on-day level differences within ±1bp for every transition
  14.04 -> 15.04 -> 16.04 -> 17.04 -> 20.04 -> 21.04 and 23.04 -> 24.04 -> 27.04 -> 28.04 -> 29.04. The only failure is 21.04 -> 23.04, explained below.
  No IRS, FRA, FX, CDS or spread block of any R in this set is an exact copy of the previous daily's (stale.py: every block "diff").
- The CDS change column is always 0 even when the level moves (e.g. PL 57 -> 52 on 20.04, HU 97 -> 92 on 15.04). It is unreliable, as in earlier runs.

### R 2026-04-23 (C 22 Apr): NO 23 Apr DAILY; values RECONSTRUCTED (flagged)
- No Erste Codziennik dated 23 Apr exists. The archive goes from 22 Apr (169321) to 24 Apr (169336). Unlisted ids 169296-169377 were probed by header:
  they are insurance terms (OWU), Erste TFI notes, AGM documents, the tyg260424 weekly and a 21 Apr komentarz. 169330 returns an HTML "400 - Erste" page;
  169331, 169343 and 169356 return 404. The komentarz-ekonomiczny archive has no Codziennik for 23 Apr (only a komentarz dated 23-04 uploaded 24 Apr 15:22).
- Fallback: the first later daily (24 Apr) heads both tables **23.04.2026**, so it carries no table headed 22.04.
- Per the coordinator's instruction, 22.04 levels were reconstructed as (23.04 level − 23.04 change column) for irs, fra, eur_irs, usd_irs and pl_bund_10y.
  This was done only because the change columns are clearly day-on-day against the unprinted 22.04 session:
  (1) Every other April transition matches within 1bp. After the stale 14 Apr daily (an exact copy of the 13 Apr daily, headed 10/04), the 15 Apr daily's
      changes were measured against the true 13.04 session, not against the last printed table. So Erste's change column is always the change vs the previous session.
  (2) Against 21.04 the changes do not fit. PL IRS 2Y 4.15 -> 4.27 is +12 in two days vs a printed +5; 5Y +12 vs +4; FRA 6x9 +16 vs +8; PL spread +12 vs +6.
      Over the same two days BBG PL 2Y/5Y/10Y rose +12/+14/+12.
  (3) The implied 22.04 values fit independent C-dated data:
      - PL-Bund 255 vs a BBG PL10Y-DE10Y gap of 251 (Erste usually 1-4bp above BBG: 21.04 249/247, 23.04 261/258); HU 300 vs BBG 291.
      - PL IRS moves on 22 Apr of +4 to +8bp vs BBG PL +6/+6/+5; US IRS +1 to +3 vs UST +2/+2/+1.
  Reconstructed 22.04 values:
  - PL IRS 1-10Y 4.11/4.22/4.24/4.28/4.34/–/4.49/4.60
  - FRA 3.87/3.98/4.14/4.23/4.08/4.21
  - EZ IRS 2.63/2.73/2.75/2.79/2.84/2.96/3.05
  - US IRS 3.97/3.89/3.85/3.86/3.89/4.07/4.13
  - pl_bund_10y 255
  The rounding uncertainty is about ±1bp. EZ 3Y/4Y carry about ±3bp, because the 23.04 EZ 3Y print 2.81 (+6, above the 4Y) looks off.
- Not reconstructed (null):
  - cds5y: the CDS change column is unreliable. PL CDS is 52 in both the 21.04 and 23.04 tables.
  - eurpln_close / eurpln_session: the FX block has no change column. The C-dated alternative is pap_close.eurpln 4.2442 (16:43).
- irs_src points to the 24 Apr daily. header_date = "23.04.2026" as printed (the header of the source table, not C); fx_header_date = null.
- **Hindsight caveat:** the 24 Apr daily was first published 24 Apr 08:17, after this report's cut-off. It is used only to recover the 22 Apr closing levels,
  which are C-dated facts. Null these keys if a strict no-later-document rule is preferred. The last Erste table published before R = 23 Apr is the
  21.04 table (R 2026-04-22), one session stale.

### Other staleness and suspicious items
- **R 2026-04-24 (table headed 23.04):** the change columns cannot be verified against a printed previous session (there is no 22.04 table). They do not
  match the differences vs 21.04 (see above). The levels are not a copy. Flagged as an Erste flag. pl_bund_10y 261 vs BBG gap 258, which is normal.
  The EZ IRS 3Y 2.81 (+6), above the 4Y 2.79 (0), looks off by about 5bp: the 24.04 table has 2.75 (-5). It is kept as published and mentioned in the flag.
- Erste PL-Bund spread vs the PAP/BBG PL10Y-DE10Y gap: 15.04 250/248; 16.04 251/250; 17.04 243/241; 20.04 246/243; 21.04 249/247; 22.04 255 (rec.)/251;
  23.04 261/258; 24.04 261/260; 27.04 264/262; 28.04 270/267; 29.04 270/267. Erste is 1-4bp above, as usual.
  29.04 270(0) is not a copy: the other countries moved (HU -8, IT +3), and the BBG gap was also unchanged.
- EUR/PLN close, Erste vs the PAP last quote: 15.04 4.2334/4.2337 (16:54); 16.04 4.2401/4.2398 (16:35); 17.04 4.2244/4.2234 (16:50);
  20.04 4.2295/4.2310 (14:26); 21.04 4.2340/4.2342 (16:50); 22.04 n/a/4.2442 (16:43); 23.04 4.2397/4.2378 (16:37); 24.04 4.2411/4.2404 (16:40);
  27.04 4.2486/4.2467 (16:45); 28.04 4.2495/4.2467 (16:11); 29.04 4.2596/4.2565 (16:56). OK.
- Erste bond table (not requested, not used): it labels the 5Y "PS0131 (5L)" throughout, but prints 5.23 (+9) at 28.04 and 5.46 (+24) at 29.04, while DS1035
  is +4 and the 2Y -2. This looks like a silent switch to PS0731 on 29.04. Its 2Y label is still OK0128.
- **Outside this set, for the other agents:**
  - The 14 Apr daily (R 14 Apr) is an exact copy of the 13 Apr daily: headed 10/04/2026, every block identical, change columns included.
  - The 4 May daily heads its tables 01.05.2026 (a PL holiday). PL IRS change columns are all 0, but its levels differ from 29.04; there is no Erste table
    headed 30.04 at all. The 5 May daily (headed 04/05) repeats the 01.05 PL IRS levels with 0 changes.

## B. PAP/Bloomberg tables
- Columns: current, 1D, 5D, 1M, 3M, 12M (arrays in curves.json in that order; HU uses 3Y).
- R editions: 16 Apr (06:34), 17 (07:34), 20 (06:35), 21 (06:35), 22 (06:40), 23 (06:36), 24 (06:33), 27 (06:36), 28 (06:40), 29 (06:34), 30 (06:39).
- 16, 20, 21, 22, 23, 27, 28 and 30 Apr: all 11 EU/CEE/TR rows are stamped exactly C. JP/US carry morning-of-R clock stamps (live), so d1 is used.
  In the 21 Apr (JP) and 24 Apr (US) editions the tenors carry different clock stamps (06:31/06:32); the stamp is stored as a list.
- **17 Apr edition (07:34): no stamp column** (same pattern as 13 Mar; not flagged).
  - EU/CEE/TR current = C (16 Apr) close, confirmed by the 20 Apr edition 1D col and, except TR, by the 24 Apr edition 5D col.
    TR has only the 1D confirmation: the 24 Apr TR row is stamped 22.04, so its 5D col is 15 Apr.
  - US and JP are live 17 Apr quotes. Their current cols differ from the 17 Apr closes (20 Apr edition 1D), and their 5D col is the 10 Apr close.
    JP at 07:34 CET is 14:34 JST, before the JGB close. d1 = 3.77/3.92/4.31 (US) and 1.37/1.83/2.41 (JP), both confirmed by the 23 Apr edition 5D col.
- **24 Apr edition: TR stamped 22.04.2026.** There was no Turkish session on 23 Apr (National Sovereignty and Children's Day). TR c_close is the 22 Apr close
  (36.88/34.01/30.43). Flagged, as March did for TR on 20 Mar.
- **29 Apr edition: US and JP stamped 28.04.2026 (not live).** R = 29 Apr was a Japanese holiday (Showa Day). The US row is also date-stamped: its 1D col is
  the 27 Apr close, its 5D col the 21 Apr close, and the current col 3.84/3.98/4.35 = 28 Apr close (6 May edition 5D col). The current col is used for all 13 rows.
  Flagged, as with the 20 Mar edition in March.
- **BBG PL 5Y generic roll on 28 Apr:** PL 5Y went 5.09 -> 5.33 (+24bp) while 2Y +6 and 10Y +9; on 29 Apr it was 5.38. This coincides with the PAP FX/FI switch to
  PS0731. Flagged in R 2026-04-29, with row notes in R 29 and R 30: the 1D/5D/1M cols there refer to the old 5Y bond.
- **C = 29 Apr was a JGB holiday.** The JP d1 in the 30 Apr edition (1.38/1.87/2.48) = 28 Apr close. Flagged, as March did for 20 Mar.
- The rule about editions between C and R was **not triggered**: there are no weekend editions, and no R edition has EU rows stamped later than C.
  after_C = false and intraday_on_C = false everywhere.
- Full cross-check (scripts/xcheck.py, editions 13 Apr to 8 May, dated per tenor because the TR 2Y row in the 5 and 6 May editions keeps a 30.04 stamp):
  for every C, all 39 country/tenor series have 0 conflicts and at least 2 observations, with these exceptions:
  - US/JP 22 Apr (R 23): one observation (23 Apr edition 1D). The 29 Apr edition's US/JP rows are dated 28.04, so their 5D col is 21 Apr.
  - US 29 Apr (R 30): one observation (30 Apr edition 1D). The 6 May 5D col is 28 Apr and the 7 May 5D col is 30 Apr.
  - JP 29 Apr: a holiday; the value is the 28 Apr close, which is seen 3 times (29 Apr edition current col, 30 Apr edition 1D col, 6 May edition 5D col).
  finalize.py asserts that every c_close equals the cross-edition consensus.
- No unchanged rows (all three tenors equal to the previous C close) were found for any C.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 15.04 4.30/4.92/5.52 vs 4.29/4.90/5.51; 16.04 4.31/4.93/5.53 vs 4.29/4.91/5.50; 17.04 4.16/4.76/5.37 vs 4.16/4.74/5.36;
  20.04 4.23/4.80/5.41 vs 4.21/4.78/5.40 (14:26); 21.04 4.29/4.86/5.47 vs 4.26/4.84/5.46; 22.04 4.35/4.92/5.52 vs 4.30/4.89/5.49 (2Y 5bp, at 16:43);
  23.04 4.41/5.00/5.59 vs 4.38/4.99/5.58; 24.04 4.43/5.03/5.59 vs 4.40/5.03/5.60; 27.04 4.47/5.09/5.65 vs 4.43/5.07/5.64;
  28.04 4.53/5.33/5.74 vs 4.49/5.32 (PS0731)/5.73; 29.04 4.57/5.38/5.78 vs 4.54/5.36 (PS0731)/5.76.
  The BBG 2Y generic runs 2-5bp above WS0428. No early piece is >=5bp off, so none is flagged.

## C. PAP Dzień na FX/FI (afternoon piece on C)
There are two FX/FI pieces per C (morning and afternoon), except 29 Apr: only the 17:13 piece is on the site, although its table has a "środa 09:12" column.
Each afternoon quote time was checked against the previous-session column of the next piece. Only the quote tables were used; no commentary.
The 2Y benchmark is **WS0428** throughout.

| C | published | quotes | EURPLN | USDPLN | 2Y WS0428 | 5Y | DS1035 | |
|---|---|---|---|---|---|---|---|---|
| 15.04 | 17:07 | 16:54 | 4.2337 | 3.5896 | 4.29 | 4.90 (PS0131) | 5.51 | |
| 16.04 | 16:55 | 16:35 | 4.2398 | 3.5994 | 4.29 | 4.91 | 5.50 | |
| 17.04 | 17:06 | 16:50 | 4.2234 | 3.5735 | 4.16 | 4.74 | 5.36 | |
| 20.04 | 14:34 | 14:26 | 4.2310 | 3.5980 | 4.21 | 4.78 | 5.40 | early; no later piece (21 Apr: "poniedziałek 14:26"); within 1-2bp of BBG, not flagged |
| 21.04 | 17:06 | 16:50 | 4.2342 | 3.6004 | 4.26 | 4.84 | 5.46 | |
| 22.04 | 17:01 | 16:43 | 4.2442 | 3.6183 | 4.30 | 4.89 | 5.49 | |
| 23.04 | 16:48 | 16:37 | 4.2378 | 3.6204 | 4.38 | 4.99 | 5.58 | |
| 24.04 | 17:02 | 16:40 | 4.2404 | 3.6199 | 4.40 | 5.03 | 5.60 | |
| 27.04 | 17:06 | 16:45 | 4.2467 | 3.6161 | 4.43 | 5.07 (PS0131) | 5.64 | last PS0131 day |
| 28.04 | 16:20 | 16:11 | 4.2467 | 3.6309 | 4.49 | 5.32 (PS0731*) | 5.73 | "*zmiana benchmarku" from the 09:26 piece (PS0731 5.28 at 09:15) |
| 29.04 | 17:13 | 16:56 | 4.2565 | 3.6385 | 4.54 | 5.36 (PS0731) | 5.76 | |
URLs are in curves.json under pap_close.url. The 28 Apr 09:15 table prints EUR/USD "4,1694" (a typo for 1.1694); not used.

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- R 2026-04-23: no Erste table headed 22.04 exists. irs/fra/eur_irs/usd_irs/pl_bund_10y are reconstructed from the 24 Apr daily (flagged; see A).
  cds5y, eurpln_close and eurpln_session are null.
- TR close for C = 23 Apr and JP close for C = 29 Apr do not exist (holidays). Their c_close is the previous close, as labelled and flagged.
- US/JP C closes for 22 Apr and US for 29 Apr are each seen only once (noted in the rows).
- No other nulls. Nothing was filled from memory.

## Note for downstream
- The March spec builder (build_specs_mar.py) sets pl_bund_10y = None whenever `flags` is non-empty. Each flag string starts with "Erste", "PAP table" or
  "PAP close note". In this set only R 23 and R 24 carry Erste flags. The R 23 flag covers reconstructed values, including pl_bund_10y = 255.
  R 24's flag concerns unverifiable change columns; its pl_bund_10y (261) is fine.
  R 29 (3 flags) and R 30 (1 flag) are PAP-only. R 16, 17, 20, 21, 22, 27 and 28 have no flags.
- The builder prints irs_src.header_date as "table headed ...". For R 23 that would read 23.04.2026, so special-case it (e.g. "reconstructed 22.04 from the
  24 Apr daily").
- PL 5Y comparisons across 27/28 Apr (BBG generic and PAP y5) mix two bonds.
