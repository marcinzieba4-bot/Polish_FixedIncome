# Working notes: Apr 2026 curves, part 1 (R 1, 2, 7-10, 13-15 Apr; C 31 Mar, 1, 2, 7-10, 13, 14 Apr)
Output: curves.json in this folder, keyed by R. Same schema as 2026-03/research/curves_pap_2.json, checked programmatically (scripts/build_apr.py asserts and
scripts/schema_check.py): identical top-level, irs/fra/eur_irs/usd_irs/eurpln_session/irs_src, pap_table, row and pap_close (+bonds) key sets and key order.
Optional keys used: `flags` (after irs_gap_note, as in March), row `note`, `pap_close.note`, and one alt edition `pap_table_0406_edition` in R 2026-04-07 (placed right
after pap_table, with a `why` key, as `pap_table_0106_edition` in Jan H1). As in late March, the PAP 2Y benchmark is WS0428, so `pap_close.bonds.OK0128` is null and
`y2` carries WS0428. Content-level novelty: some Erste fields in R 9 Apr and R 14 Apr are DERIVED (level minus change column of a later daily; see A).
Raw parses: erste_raw_all.json (30 Mar to 16 Apr dailies), paptab_raw.json (PAP tables 30 Mar to 22 Apr), fx_raw.json, xcheck_obs.json.
Downloads: dl/erste (archiwum.html, ids_all.tsv, ids.tsv, PDF + pdftotext -layout), dl/si (PAP tables), dl/si/fx (FX/FI notes + fx_slugs.txt), dl/si/list (listing pages 372-414).
Scripts: scripts/ (rewritten, the March scripts were not available): erste.py, paptab.py, fxparse.py (label-driven), stale.py (exact-copy test + change-column test),
xcheck_apr.py (cross-edition "as-of" check), build_apr.py, schema_check.py.
Renders: render/ (page 2 of the 3, 7, 8, 9, 13, 14 Apr dailies; cmp_0408v0409.png = stale IRS table; cmp_0403v0407.png; cmp_0401_0410_0415.png = parse spot-check;
a13_p*.txt / a14_p*.txt = per-page text of the 13/14 Apr dailies).

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum), ids by publication date: 30-03 169186, 31-03 169188, 01-04 169190, 02-04 169191,
  **03-04 169192 (Good Friday)**, 07-04 169195, 08-04 169198, 09-04 169208, 10-04 169219, 13-04 169225, 14-04 169244, 15-04 169248, 16-04 169251. No daily on 6 Apr.
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. All PDFs 3 pages, still Santander-branded.
- PDF CreationDate (UTC) / URL upload stamp (CEST): 01 Apr 06:08:07Z / 15:06:39 (late); 02 Apr 06:04:39Z / 08:43:13; 03 Apr 06:05:04Z / 08:30:25; 07 Apr 06:28:58Z / 13:39:35 (late);
  08 Apr 06:51:31Z / 09:31:09; 09 Apr 06:31:01Z / 08:50:43; 10 Apr 06:22:45Z / 12:57:47 (late); **13 Apr 07:16:02Z / 2026-04-23 15:05:30 (re-uploaded 10 days later;
  the file itself was created on 13 Apr, and its page 2 is identical to the 14 Apr daily uploaded 14 Apr 09:34, so the 10/04 tables were public by 14 Apr at the latest)**;
  14 Apr 06:51:08Z / 09:34:09; 15 Apr 06:43:39Z / 08:50:56; 16 Apr 06:42:55Z / 09:11:34. All created on the morning of their date. The late upload stamps are recorded
  as printed in irs_src.upload (13 Apr with a "(re-upload; ...)" suffix); not flagged.
- Formats: headers dd.mm.yyyy (dailies 31 Mar to 3 Apr, 15-16 Apr) and dd/mm/yyyy (7-14 Apr). Decimal commas in the 31 Mar to 3 Apr and 15-16 Apr dailies, points in
  7-14 Apr; the parser handles both. Spot-checked against rendered page 2 of the 1, 3, 7, 8, 9, 10, 15 Apr dailies (IRS PL/US/EZ, FRA, CDS/spread, FX match).
  The 10 Apr daily prints the EURPLN fixing with 3 decimals ("4.261"), stored as a number.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026): 31 Mar = p.411-413; 1 Apr = 408-411; 2 Apr = 405-408; 3 Apr = 405; 4-6 Apr = 404-405;
  7 Apr = 402-404; 8 Apr = 399-402; 9 Apr = 397-399; 10 Apr = 395-397; 13 Apr = 393-395; 14 Apr = 391-393; 15 Apr = 388-391. Pages 372-414 fetched in ascending order;
  409 and 410 failed on the first pass (no response) and were refetched with 411 afterwards.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. Editions found: 30, 31 Mar; 1, 2, **6 (Easter Monday, 06:30)**, 7, 8, 9, 10, 13-17, 20-22 Apr.
  3 Apr (Good Friday), 4, 5, 11, 12 Apr returned 404 (4/5 Apr: first try no response, retry 404).

## A. Erste tables (main values in curves.json)
- R 1, 2, 8, 10, 13, 15 Apr: the R-dated daily exists and both its "Rynek stopy procentowej" and FX "Poprzednia sesja" headers equal C. Values are direct reads.
- **R 7 Apr (C 2 Apr): Easter.** Erste DID publish on Good Friday (3 Apr daily, id 169192, 08:05 CEST creation, inside the 2-6 Apr window); its tables are headed 02.04.2026.
  There was no daily on 6 Apr. The 7 Apr daily heads both tables **06/04/2026** (after C; PL IRS/FRA/bond change columns ~0 as Poland was closed; US IRS change
  column measured against 3 Apr, when the US traded; the HU spread 401(+5) is a copy of the 02.04 entry). Per the fallback rule (first daily after C whose table is headed C)
  **all Erste fields for R 7 Apr come from the 3 Apr daily**; irs_src describes it. Flagged ("Erste source: ...") because irs_src is not the R-dated daily.
- **R 9 Apr (C 8 Apr, ceasefire day): STALE IRS TABLE.** The 9 Apr daily (headed 08/04/2026) prints an IRS table (PL/US/EZ) that is an exact copy of the 8 Apr daily's
  07/04 table, levels and change columns included (render/cmp_0408v0409.png). FRA (3x6 -17, 6x9 -35, 9x12 -38), bonds (-35/-36/-37), CDS/spread (PL 258(-23)) and FX are fresh.
  No daily prints an 08/04 IRS table. Following the coordinator's rule for the analogous R 14 case (reconstruct from the next issue's change columns if clean), irs/eur_irs/
  usd_irs hold **derived** 8 Apr levels = 10 Apr daily (headed 09/04) level minus change column: PL 3.97/4.06/4.08/4.13/4.18/4.36/4.48 (1-10Y; -22 to -32bp on C vs BBG PL
  -33/-37/-37), US ~unchanged (UST also unchanged on C), EZ -11 to -20bp (Bund -23/-18/-14). Clean: the same reconstruction applied to that daily's FRA and spread reproduces
  the printed 08/04 FRA/spread within 1bp. The 10 Apr daily was published after I of R 9 (hindsight caveat stated in the flag; null these three dicts if only direct reads
  are acceptable; the printed stale values equal R 8 Apr).
- **R 14 Apr (C 13 Apr): NO TABLE HEADED C.** Confirmed the coordinator's heads-up: page 2 of the 14 Apr daily (id 169244) is a reprint of the 13 Apr daily's page 2 (both
  headed 10/04/2026; every IRS/FRA/WIBOR/bond/CDS/spread/FX value identical, change columns included; text diff = date line only; pixel diff of the rendered page 2 differs
  only in the date line). The 15 Apr daily is headed 14.04 (after C, never used for C). So no daily carries a 13.04 table. Per the coordinator's rule, the 13 Apr levels are
  **derived** from the 15 Apr daily (level minus change column; published 15 Apr, i.e. after R): PL IRS 4.04/4.15/4.18/4.22/4.27/4.45/4.57 (+4 to +6bp vs 10 Apr; BBG PL
  2Y/5Y/10Y +10/+5/+3), FRA 3.86/3.94/4.03/4.14/4.01/4.10, PL-Bund 247 (BBG gap 245; Erste normally 1-4bp above), US IRS 3.97/3.87/3.82/3.84/3.88/4.06/4.12 (the 10/04 US 8Y
  print looks odd, the derived shape matches 14.04/15.04), EZ IRS with **4Y null** (derived 2.86 = +4bp while all other EZ tenors moved -1..+1, kinking 2.80/2.86/2.87; its
  change column (-8) looks misprinted). **cds5y null** (CDS change column is always 0, not reconstructible) and **eurpln_close/eurpln_session null** (no FX change column;
  the only C-dated EUR/PLN is pap_close.eurpln 4.2526 at 15:11). irs_src = the 15 Apr daily with header_date "derived 13.04.2026 (= 14.04.2026 levels minus change col)"
  and fx_header_date null. Method validation: the 15->16 Apr control reproduces the printed 14.04 levels within 1bp for all blocks. Derived values are good to about +-1bp.
- IRS 7Y is not in the table (1,2,3,4,5,8,10Y), so it is null and irs_gap_note is set for every R (extended in R 9 and R 14).
- Change columns vs day-on-day level differences (scripts/stale.py), all within +-1bp for 30.03->31.03->01.04->02.04, 06/04->07/04, 09/04->10/04 and 14.04->15.04, except:
  - 02.04 -> 06/04 (7 Apr daily; not used): US IRS (vs 3 Apr), FRA 6x9/6x12 (+4/+5 vs +2/+2), HU spread copy.
  - 07/04 -> "08/04" (9 Apr daily): IRS exact copy (see above). FRA and spread consistent.
  - "08/04" -> 09/04 (10 Apr daily): PL/EZ IRS and US 8Y change columns imply the unprinted 8 Apr baseline (flagged in R 10, like March R 10 Mar). FRA/spread consistent.
  - 10/04 -> 10/04 (14 Apr daily): full copy. 10/04 -> 14.04 (15 Apr daily): IRS/FRA/spread change columns imply the unprinted 13 Apr baseline (flagged in R 15, like March R 17 Mar).
- Exact-copy test vs the previous daily: every block "diff" except the 9 Apr IRS (PL/US/EZ) and the whole 14 Apr page. CDS change column always 0 even when the level
  moves (e.g. PL 65 -> 60 on 09/04, HU 110 -> 97), unreliable as before.
- Erste PL-Bund spread vs BBG PL10Y-DE10Y: 31.03 290/288; 01.04 275/272; 02.04 275/273; 07.04 281/279; 08.04 258/256; 09.04 257/256; 10.04 249/245; 13.04 247 (derived)/245;
  14.04 250/249. Erste 1-4bp above, as usual.
- EUR/PLN close, Erste vs PAP last quote: 31.03 4.2951/4.2956 (17:00); 01.04 4.2797/4.2819 (16:50); 02.04 4.2721/4.2770 (16:40); 07.04 4.2753/4.2731 (13:50);
  08.04 4.2459/4.2507 (16:30); 09.04 4.2466/4.2513 (16:55); 10.04 4.2465/4.2448 (16:50); 13.04 none/4.2526 (15:11); 14.04 4.2392/4.2404 (16:50).
- Erste bond table (not used) still labels the 2Y benchmark OK0128; pdftotext drops DS1035 in the 9 Apr daily (render: 5.53 (-37)). The 3 Apr daily (02.04) shows PS0131/DS1035
  with 0 change while BBG PL 5Y/10Y were unchanged/+1; not used.

## B. PAP/Bloomberg tables
- Columns current, 1D, 5D, 1M, 3M, 12M (array order as before). R editions: 1 Apr (06:36), 2 (06:34), 7 (06:34), 8 (06:35), 9 (06:35), 10 (07:27, unstamped), 13 (06:34),
  14 (06:35), 15 (06:41).
- 1, 2, 8, 9, 13, 14, 15 Apr: all EU/CEE/TR rows stamped exactly C; JP/US carry morning-of-R clock stamps (live), so d1 is used.
- **7 Apr edition (C = 2 Apr)**, row by row:
  - PL, CZ, IE, IT, PT, ES, DE, FR, UK: stamped **03.04.2026** (Good Friday, no session; current col = 1D col = the 2 Apr close carried over) -> after_C, d1 = C close
    (= 6 Apr edition 1D col = 10 Apr edition 5D col).
  - HU: stamped **02.04.2026** = C (Hungary closed 3 and 6 Apr) -> current col (= 6 Apr edition current col = 10 Apr edition 5D col).
  - TR: stamped **06.04.2026** (Turkish sessions on 3 and 6 Apr) -> after_C; its d1 38.99/35.04/30.42 is the **3 Apr** close (also after C). The TR C close 38.95/34.98/30.41
    is the 1D col of the 6 Apr edition (TR stamped 03.04), confirmed by the 10 Apr edition 5D col. c_close set accordingly; d1 kept as printed (Jan precedent).
  - JP/US: live (06:30/06:31) with d1 = 6 Apr close (after C). No window edition carries their 2 Apr close (no 3 Apr edition; the 6 Apr edition is live 6 Apr with 1D = 3 Apr
    close). c_close = 9 Apr edition 5D col (US 3.80/3.95/4.30, JP 1.39/1.81/2.39), published after R and read only for the 2 Apr value (rolling-table rule); seen once.
  - The **6 Apr edition** (published Easter Monday 06:30, inside the window) is included as `pap_table_0406_edition`: EU/CEE/TR rows stamped 03.04 with d1 = 2 Apr close,
    HU 02.04, JP/US live 6 Apr. Every non-live row there yields the C close via current (HU) or d1, including TR. The March builder switches to this alt automatically
    (main table has 10 after_C rows > 3), which gives the right C closes. Flagged ("PAP table: ...").
- **10 Apr edition (07:27): no stamp column.** EU/CEE/TR current = 9 Apr close (13 Apr edition 1D col, 17 Apr edition 5D col). US/JP inferred live 10 Apr (5D col = 3 Apr close
  = 6 Apr edition 1D col); d1 = 9 Apr close (US 3.77/3.90/4.28, JP 1.39/1.80/2.39), confirmed by the 16 Apr edition 5D col. Standard pattern, so row notes only, no flag
  (as for 13 and 27 Mar). 07:27 CEST = 08:27 Istanbul, before the TR open; TR current confirmed as the 9 Apr close.
- The 17 Apr edition (07:34, outside the window) is also unstamped; used only as a 5D cross-check (its EU rows = 16 Apr).
- The rule about editions between C and R was triggered only for R 7 Apr (Easter). No weekend editions. intraday_on_C false everywhere.
- Full cross-check (scripts/xcheck_apr.py, editions 30 Mar to 22 Apr, as-of model: 1D = value as of the previous weekday, 5D = value as of Dc-7): for every C in scope all 39
  country/tenor series have >=2 consistent observations and 0 conflicts, except C = 2 Apr US/JP (one observation, 9 Apr edition 5D). build_apr.py asserts every c_close equals
  the cross-edition consensus. No unchanged rows (all tenors equal to the previous close) for any C.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 31.03 4.53/5.29/5.88 vs 4.53/5.27/5.87 (17:00); 01.04 4.33/5.10/5.71 vs 4.31/5.08/5.70; 02.04 4.34/5.10/5.72 vs 4.33/5.08/5.71;
  07.04 4.49/5.26/5.87 vs 4.36/5.12/5.76 (13:50, early, flagged); 08.04 4.16/4.89/5.50 vs 4.12/4.86/5.48; 09.04 4.20/4.92/5.55 vs 4.18/4.91/5.54; 10.04 4.16/4.87/5.51 vs
  4.15/4.86/5.51; 13.04 4.26/4.92/5.54 vs 4.18/4.88/5.52 (15:11, early, flagged); 14.04 4.25/4.89/5.51 vs 4.23/4.87/5.50.

## C. PAP Dzień na FX/FI (afternoon piece on C)
Two FX/FI pieces per C (morning + afternoon); also two on Good Friday 3 Apr (09:44, 15:06) and none on 6 Apr. Each afternoon quote time was checked against the previous-day
column of the next morning's piece. Only the quote tables were used; no commentary.

| C | published | quotes | EURPLN | USDPLN | WS0428 | PS0131 | DS1035 | |
|---|---|---|---|---|---|---|---|---|
| 31.03 | (17:10) | 17:00 | 4.2956 | 3.7294 | 4.53 | 5.27 | 5.87 | 17:10 piece = title only; numbers from the 1 Apr 09:41 piece's "wtorek 17:00" column (after I; flagged) |
| 01.04 | 17:13 | 16:50 | 4.2819 | 3.6838 | 4.31 | 5.08 | 5.70 | |
| 02.04 | 16:55 | 16:40 | 4.2770 | 3.7031 | 4.33 | 5.08 | 5.71 | 3 Apr pieces: "4,32* / 5,08* / 5,71*", "*zamknięcia z czwartku" |
| 07.04 | 14:19 | 13:50 | 4.2731 | 3.6970 | 4.36 | 5.12 | 5.76 | early; 8 Apr morning prev col = "wtorek 17:50" (unpublished on C) |
| 08.04 | 17:04 | 16:30 | 4.2507 | 3.6355 | 4.12 | 4.86 | 5.48 | |
| 09.04 | 17:20 | 16:55 | 4.2513 | 3.6406 | 4.18 | 4.91 | 5.54 | |
| 10.04 | 17:04 | 16:50 | 4.2448 | 3.6202 | 4.15 | 4.86 | 5.51 | |
| 13.04 | 15:21 | 15:11 | 4.2526 | 3.6356 | 4.18 | 4.88 | 5.52 | early; 14 Apr morning prev col = 15:11 |
| 14.04 | 17:06 | 16:50 | 4.2404 | 3.5925 | 4.23 | 4.87 | 5.50 | |
2Y benchmark = WS0428 throughout (bonds.OK0128 null). URLs are in curves.json under pap_close.url (R 1 Apr: the 1 Apr 09:41 piece; the empty 31 Mar 17:10 URL is in its note).

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- C = 13 Apr (R 14): no Erste table headed C anywhere; IRS/FRA/spread derived (see A); EZ IRS 4Y, cds5y, eurpln_close and eurpln_session null.
- C = 8 Apr (R 9): Erste IRS table stale; IRS PL/US/EZ derived from the 10 Apr daily (see A).
- C = 31 Mar: no C-dated PAP closing table on the site; quotes from the next morning's previous-session column.
- C = 7 Apr and 13 Apr: PAP close only as early quotes (13:50, 15:11).
- C = 2 Apr: US/JP closes appear in no window edition (taken from the 9 Apr edition 5D col).
- Nothing else is null; nothing was filled from memory.

## Note for downstream
- irs_src for R 7 Apr is the 3 Apr daily (label "Codziennik of 3 Apr", tables headed 02.04), not the R-dated daily. For R 14 Apr irs_src is the 15 Apr daily and its
  header_date is a "derived ..." string.
- Derived (not directly read) fields: R 9 irs/eur_irs/usd_irs; R 14 irs/fra/pl_bund_10y/eur_irs/usd_irs. Both come from dailies published after I of that R (coordinator rule).
- The March builder nulls pl_bund_10y whenever `flags` is non-empty. Flag strings start with "Erste", "STALE", "PAP table" or "PAP close note". Of the spread values, only R 14
  (derived 247) is questionable; the R 7, 9, 10 and 15 Erste flags concern the source document or the IRS/change columns, not the spread level.
