# Working notes: June 2026 curves, part 1 (R 1-3, 5, 8-12, 15 Jun; C 29 May, 1-3, 5, 8-12 Jun)
Output: curves.json in this folder, keyed by R. Same schema as 2026-05/research/curves_pap_1.json, checked programmatically (scripts/schema_check.py against
the April and May curves_pap_1/2.json: top-level key order (minus the optional `flags` and `pap_table_*_edition`), the key set and order of every nested
dict (irs, fra, eur_irs, usd_irs, eurpln_session, irs_src, pap_table, rows, d1, pap_close, bonds) and the value types at every path: **0 errors**, 125 of
125 template paths present, no new path; log schema_check.log). build.py also asserts every non-live c_close against the cross-edition consensus, and
scripts/sim_builder.py replays the PAP part of build_specs_may.py (edition switch, live rows dropped, d1 for after_C rows) and asserts the values that reach
the spec equal c_close (sim_builder.log).
Optional keys used: `flags` (right after irs_gap_note), row `note`, and one alt edition `pap_table_0604_edition` in R 2026-06-05 (right after pap_table, with
a `why` key, as `pap_table_0501_edition` in May R 4 May). New detail: in the R 5 Jun main table HU is after_C, so its `d1` has keys y3/y5/y10 (the builder
reads d1['y' + tenor]; no template row had a HU d1).
Benchmarks: PAP FX/FI 2Y WS0428, 5Y PS0731, 10Y DS0436 for every C; **2Y roll on C = 12 Jun** (see B/C; PAP relabels the row PS0728 only on 15 Jun 09:16,
after the last R). No switch to OK0129. Erste bond table labels unchanged throughout (WS0428 (2L), PS0731 (5L), DS1035 (10L); the 10L has tracked DS0436
since 18 May, see the May notes). `bonds.OK0128/PS0131/DS1035` null for every R (none quoted).
Content-level novelties: R 1 Jun Erste CDS/spread table a stale copy (cds5y and pl_bund_10y NULL); R 5 Jun = Corpus Christi (Erste tables headed 03.06 = C;
PAP R edition mostly 4 Jun closes, alt 4 Jun edition used); R 10 Jun Erste PL 10Y/spread stale (pl_bund_10y NULL); Erste PL-Bund spread ~9bp too wide on
2 and 3 Jun (kept, flagged); Erste CDS block frozen 10-12 Jun (kept, flagged); PAP 2 Jun afternoon FX/FI piece not findable (close read from the next
morning piece); BBG FR 5Y/10Y series jump on 8 Jun; BBG/PAP 2Y roll on 12 Jun.
Raw parses: erste_raw_all.json (dailies 29 May to 16 Jun), pdfinfo.json, paptab_raw.json (PAP tables 28 May to 22 Jun), fx_raw.json (FX/FI pieces 28 May
to 17 Jun), xcheck_obs.json; logs stale.log, xcheck.log, build.log, schema_check.log, sim_builder.log.
Downloads: dl/erste (archiwum.html copy, ids.tsv, PDFs + pdftotext -layout), dl/si/tab (tYYYYMMDD = 200, xYYYYMMDD = 404 page), dl/si/fx (+ fx_slugs.txt),
dl/si/list (p280-313, re/ = refetch of p301-304, all_links.json), dl/nbp (NBP table A EUR/USD 27 May-16 Jun, cross-check of the Erste fixings).
Scripts (written fresh; the May scripts are not on disk): erste.py (page-2 parser, section anchors at line start), paptab.py (stamped / unstamped / raw
Bloomberg-ticker layouts), fxparse.py, stale.py (exact-copy test per block + change column vs level difference), xcheck.py (as-of consensus), build.py,
schema_check.py, sim_builder.py, show.py, tabdump.py. Run: `python3 -I scripts/erste.py dl/erste erste_raw_all.json`, `... paptab.py dl/si/tab
paptab_raw.json`, `... fxparse.py dl/si/fx fx_raw.json`, `... xcheck.py paptab_raw.json xcheck_obs.json`, `... build.py .`, then schema_check.py.
Renders: render/cmp_0601_0605_0610.png (page 2 of the 1, 5 and 10 Jun dailies side by side): confirms the copied CDS/spread table (1 Jun), the 03.06 headers
(5 Jun) and the DS1035 5.87 (6) / Polska 281 (6) rows (10 Jun); FX, IRS PL/US/EZ, WIBOR, FRA, CDS/spread all match the parse.

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (copy of SP/dl/erste_archiwum.html; ids taken from data-item-group-id/data-item-id + "Data publikacji", issue titles not used). Ids by
  publication date: 29-05 169465 (chain base), 01-06 169472, 02-06 169480, 03-06 169482, **(no 4 Jun daily)**, 05-06 169489, 08-06 169491, 09-06 169494,
  10-06 169495, 11-06 169498, 12-06 169499, 15-06 169503 (16-06 169515, audit only). Fetched with https://www.erste.pl/regulation_file_server/download?id=<id>&lang=pl_PL
  (curl -L); irs_src.url carries the archive's time<YYYYMMDDhhmmss> form. All 4 pages, Erste Bank Polska branding, footnote "**Informacje odnoszą się do stawek
  kupna na rynku międzybankowym na koniec dnia", source "LSEG, Datastream" in every daily.
- PDF CreationDate (UTC) / URL upload stamp (CEST), all on the morning of R: 1 Jun 06:53:03Z / 09:03:44; 2 Jun 06:56:39Z / 09:06:29; 3 Jun 07:01:47Z / 09:21:04;
  5 Jun 07:01:51Z / 09:16:20; 8 Jun 06:34:38Z / 08:43:47; 9 Jun 06:26:16Z / 08:41:01; 10 Jun 06:33:03Z / 08:41:39; 11 Jun 06:32:21Z / 08:48:10;
  12 Jun 06:45:31Z / 08:50:49; 15 Jun 06:32:11Z / 08:39:23. None late; not flagged.
- Header formats: dd/mm/yyyy in the 1, 2, 3, 8-12 Jun dailies, dd.mm.yyyy in the 29 May, 5 and 15 Jun dailies (recorded as printed); decimal commas in the
  29 May, 5 and 15 Jun dailies, points elsewhere.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026; found by probing p306 = 1 Jun and p280 = 17 Jun): 29 May = p.307-310;
  1 Jun = 304-307; 2 Jun = 302-304; 3 Jun = 299-302; 4 Jun = 299; 5 Jun = 297-298; 8 Jun = 295-297; 9 Jun = 293-295; 10 Jun = 290-293; 11 Jun = 288-290;
  12 Jun = 286-288; 15 Jun = 284-286. Pages 281-313 fetched in ascending order (all 200, retries built in), 301-304 refetched once.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. Editions: every weekday 28 May to 22 Jun incl. **4 Jun (Corpus Christi,
  06:34)**; 30, 31 May, 6, 7, 13, 14 Jun return 404 (no weekend editions). 15 and 22 Jun failed on the first pass (connection reset) and returned 200 on retry.
- FX/FI pieces: two per C (morning + afternoon) for every C except **2 Jun (only the 09:56 morning piece is linked; the afternoon piece, whose 16:20 quotes the
  3 Jun 09:32 piece shows as "wtorek 16:20", is on no listing page and was not found by web search)**; no pieces on 4 Jun. Slugs in dl/si/fx/fx_slugs.txt.
- NBP API table A (api.nbp.pl): EUR fixings 29 May 4.2322 (103/A), 1 Jun 4.2341, 2 Jun 4.2334, 3 Jun 4.2433 (106/A), **no 4 Jun table**, 5 Jun 4.2348 (107/A),
  8 Jun 4.2462, 9 Jun 4.2359, 10 Jun 4.2481, 11 Jun 4.2530, 12 Jun 4.2484: every Erste "fixing" equals the NBP fixing of C.

## A. Erste tables (main values in curves.json)
- For all 10 R the R-dated daily exists and both its "Rynek stopy procentowej" and FX "Poprzednia sesja" headers equal C (5 Jun daily: 03.06 = C). Direct reads;
  nothing is derived or reconstructed.
- IRS 7Y is not in the table (1,2,3,4,5,8,10Y): null and irs_gap_note set for every R. No other IRS tenor is null.
- Change columns vs day-on-day level differences (stale.log), 28.05 -> 29/05 -> 01/06 -> 02/06 -> 03.06 -> 05/06 -> 08/06 -> ... -> 12.06 -> 15.06: PL IRS and
  FRA within +-1bp for every transition; US/EZ IRS within +-1bp except 03.06 -> 05/06 (measured vs unprinted 4 Jun levels) and EZ 10Y 3.12 -> 3.07 (0);
  PL spread except 29/05 (copy), 02/06 -> 03.06 (+3 vs -5) and 03.06 -> 05/06 (+7 vs +1); bonds except 08/06 -> 09/06 (10L copy). Exact-copy test: the CDS/spread
  table 28.05 -> 29/05 (all values and changes) and the CDS block 09/06 -> 10/06 -> 11/06 -> 12.06 are copies; every other block "diff". The CDS change column
  is always 0 except PL 03.06 (+1 on an unchanged 51): unreliable as before.

### R 2026-06-01 (C 29 May): CDS/spread table STALE -> cds5y and pl_bund_10y NULL. Flagged.
- The 1 Jun daily (headed 29/05) prints a CDS/spread table identical to the 28.05 table (PL 51 (0) / 283 (+2), FR 14/71 (+3), HU 72/253 (+2), ES 16/43, IT 13/74,
  PT 8/39, IE 9/19, DE 4) while every other block moved (PL IRS -12 to -18bp, FRA -4 to -23, bonds -24/-19/-15; BBG PL -13/-21/-13, Bund 10Y -2 -> BBG gap
  281 -> 270). No C-dated CDS or spread exists; last valid prints (28 May): CDS 51, spread 283. [Post-R: the 2 Jun daily's PL spread change -13 is vs 283.]
- US IRS 4Y 4.33 (0) repeats the 28.05 misprint (3Y 4.11, 5Y 4.14): kept, flagged unreliable. [Post-R: 2 Jun daily 4.14 (-19).]
- Erste bond table (not used): 2L WS0428 4.39 (-24) after the 4.62 (+10) glitch of 28.05; 01/06 2L 4.39 (0) unchanged while BBG 2Y +3 (glitch, not used).

### R 2026-06-02 (C 1 Jun): levels fresh; spread change column spans 29 May + 1 Jun (vs the stale 283). Flagged (Erste note), values used.
### R 2026-06-03 (C 2 Jun): PL-Bund 280 (+10) vs BBG gap 270: ~9bp too wide (Bund leg: Erste 10L 5.69 = BBG 5.68; FR/IT/PT spreads +8..+10 too). Kept, flagged.
### R 2026-06-05 (C 3 Jun, after Corpus Christi 4 Jun): tables headed 03.06.2026 = 3 Jun closes. Flagged.
- No daily dated 4 Jun. The 5 Jun daily (id 169489) heads FX and rates tables 03.06. Every change column (PL IRS +3/+4/+4/+4/+4/+4/+4, FRA, US IRS, EZ IRS, bonds,
  WIBOR O/N +11) matches the day-on-day difference from 02/06 within 1bp; US IRS 2Y/5Y/10Y +4/+5/+5 vs UST 3 Jun +4/+5/+5; EZ +5/+6/+10 vs Bund +5/+6/+6 (EZ 10Y
  3.12 ~3bp high; eur_irs not used by the builder). FX block = 3 Jun session: open 4.2362 ~ 2 Jun close 4.2353; close 4.2412 vs PAP 16:17 4.2407; fixing 4.2433 =
  NBP 106/A of 3 Jun. The 4 Jun core-market session is in no Erste table (precedent 1/4 May: there the R daily was headed 01.05 with blocks of mixed sessions;
  here every block is C). PL-Bund 275 (+3): the change is measured against ~272 (the 01/06 271), not 280; BBG gap 266 -> Erste again ~9bp wide. Kept, flagged.
- [Post-R audit: the 8 Jun daily's US/EZ IRS change columns are vs unprinted 4 Jun levels (US 4 Jun implied 4.11/4.17/4.16/4.16/4.18/4.29/4.35 = 3 Jun -1 to -4bp,
  UST 4 Jun -4/-4/-2); its PL IRS/FRA/bond changes are vs 03.06 (the PL feed carries 3 Jun through the holiday); spread change +7 vs 269.]
### R 2026-06-08 (C 5 Jun): levels fresh (spread 276 vs BBG 275); US/EZ IRS and spread change columns do not chain with 03.06. Flagged (Erste note).
### R 2026-06-09 (C 8 Jun): direct reads, no Erste flag (spread 281 vs BBG 279). Bond 5L 5.45 (+1) unchanged level while BBG 5Y +7 (not used).
### R 2026-06-10 (C 9 Jun): PL 10Y bond row and spread STALE -> pl_bund_10y NULL. Flagged.
- Table headed 09/06: 10L 5.87 (6) = exact copy of the 08/06 row, 2L 4.64 (0) unchanged, spread 281 (+6) = 08/06 level, while PL IRS -12..-15, FRA to -18, 5L -8,
  BBG PL 10Y -13, PAP DS0436 -8 (14:06 -> 17:14), Bund -2 (BBG gap 279 -> 268). The rest of the CDS/spread table updated (CDS FR/HU/IT/IE changed): cds5y 52 kept.
  [Post-R: the 10/06 changes 2L/10L/spread -22/-13/-14 are vs these stale prints.]
### R 2026-06-11 (C 10 Jun): spread 267 fresh (BBG 264); change columns of bonds/spread span 9+10 Jun; CDS block = copy of 09/06. Flagged (Erste note).
### R 2026-06-12, R 2026-06-15: CDS block identical for the 2nd/3rd daily in a row (PL 52, FR 14, HU 70, IT 13 ...; before 10 Jun FR/IT/IE moved +-1 almost
  daily; 15.06 then PL 50, HU 68): cds5y 52 kept but flagged as possibly stale since 9 Jun. Spreads fresh (267/265, 261/259).

### Erste PL-Bund spread vs BBG PL10Y-DE10Y gap
28.05 283/281; **29/05 283 (copy)/270**; 01/06 271/272; **02/06 280/270; 03.06 275/266**; 05/06 276/275; 08/06 281/279; **09/06 281 (stale)/268**; 10/06 267/264;
11/06 267/265; 12.06 261/259 [15.06 253/252, audit]. Normal basis 0-3bp above (Erste 10L = DS0436 tracks the BBG 10Y within 0-2bp on every clean day).

### EUR/PLN close, Erste vs PAP last quote
29.05 4.2287/4.2277 (16:55); 01.06 4.2354/4.2375 (16:45); 02.06 4.2353/4.2353 (16:20, via the 3 Jun piece); 03.06 4.2412/4.2407 (16:17); 05.06 4.2467/4.2341
(14:25, early); 08.06 4.2395/4.2422 (14:06, early); 09.06 4.2418/4.2385 (17:14); 10.06 4.2480/4.2462 (16:51); 11.06 4.2582/4.2563 (16:55); 12.06 4.2441/4.2444
(17:50). Fixings = NBP table A of C (all 10 checked).

## B. PAP/Bloomberg tables
- Columns current, 1D, 5D, 1M, 3M, 12M (array order as before; HU 3Y). R editions: 1 Jun 06:34, 2 Jun 06:42, 3 Jun 06:34, **5 Jun 05:55 (raw Bloomberg-ticker
  layout, unstamped)**, 8 Jun 06:33, 9 Jun 06:30, 10 Jun 06:34, 11 Jun 06:34, 12 Jun 06:34, 15 Jun 06:33. JP/US clock-stamped (live, d1 used) in every
  stamped edition; mixed clock stamps stored as lists (2 Jun US, 10 Jun JP, 15 Jun JP).
- **1 Jun edition (C 29 May)**: EU/CEE stamped 29.05; TR 25.05/26.05/25.05 (Kurban Bayrami 27-29 May; row identical to the 28 and 29 May editions'): TR c_close =
  39.78/36.03/32.94, not C-dated. Flagged.
- 2 and 3 Jun editions: standard (TR back, stamped 01.06 / 02.06).
- **5 Jun edition (C 3 Jun, Corpus Christi on 4 Jun)**: raw layout as on 15 May. HU, CZ, TR, IE, IT, PT, ES, DE, FR, UK = 4 Jun closes (8 Jun edition 1D col,
  12 Jun edition 5D col) -> after_C, d1 = 1D col = 3 Jun close (4 Jun edition current col, 11 Jun edition 5D col); PL row identical to the 4 Jun edition PL
  row (no Polish session) -> current col = C close; JP/US live 5 Jun (1D = 4 Jun close, 5D = 29 May close) with post-C d1, so their c_close = the 3 Jun close
  from the 4 Jun edition 1D col (also the 10 Jun edition 5D col; April 7 Apr precedent for c_close_src wording). The **4 Jun 06:34 edition** (in the window
  3-4 Jun; all EU/CEE/TR stamped 03.06 = C, JP/US live 4 Jun with d1 = 3 Jun close) is included as `pap_table_0604_edition`; the builder's switch rule
  (10 after_C rows > 3) picks it; both give identical C closes (sim_builder.log). Flagged.
- 8 Jun edition: standard. 9 and 10 Jun editions: **TR 2Y stamped 05.06** (no TR 2Y print 8-9 Jun; c_close 2Y = 39.74 = 5 Jun close). Flagged.
- **FR 5Y/10Y +16/+15bp on 8 Jun** (DE +2/+2, IT/ES/PT +2..+3, FR 2Y +5; Erste FR-Bund 65 -> 66): probably a Bloomberg FR generic series change; persists in later
  editions (Erste FR spread jumps +10 only on 15 Jun, audit). Row note + flag in R 9 Jun.
- **PL 2Y generic roll on 12 Jun**: BBG PL 2Y 4.38 -> 4.47 (+9) while 5Y/10Y -10/-9, Erste WS0428 -7, PL IRS 2Y -10. Row note + flag in R 15 Jun.
- Identical rows between consecutive editions (28 May to 22 Jun): TR 28->29 May->1 Jun (Kurban Bayrami), PL 4->5 Jun (Corpus Christi), TR 2Y 8->9->10 Jun.
  No stale edition. No edition between C and R has rows stamped later than C except the R 5 Jun case above.
- Cross-check (scripts/xcheck.py, editions 28 May to 22 Jun; as-of model: 1D = previous weekday of the row date, 5D = row date - 7, carried closes on
  non-trading days; 29 May and 19 Jun unstamped editions dated to the previous weekday, 5 Jun raw edition dated 4 Jun except PL (3 Jun), TR 29 May by copy
  source): **0 conflicts** over 39 series; for every C all 39 series observed, single observations only for TR 2Y 8 Jun (carry). build.py asserts every
  c_close against this consensus.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 29.05 4.45/5.14/5.64 vs 4.39/5.16/5.60; 01.06 4.48/5.27/5.72 vs 4.44/5.25/5.70; 02.06 4.46/5.23/5.68 vs 4.43/5.21/5.66
  (16:20); 03.06 4.47/5.26/5.70 vs 4.42/5.24/5.67; 05.06 4.55/5.36/5.79 vs 4.46/5.27/5.71 (14:25, flagged); 08.06 4.60/5.43/5.85 vs 4.52/5.35/5.79 (14:06,
  flagged); 09.06 4.48/5.28/5.72 vs 4.46/5.27/5.71; 10.06 4.44/5.27/5.72 vs 4.42/5.26/5.70; 11.06 4.38/5.20/5.68 vs 4.35/5.19/5.66; 12.06 4.47/5.10/5.59 vs
  4.45/5.09/5.57 (2Y = new bond in both).
- US C closes (d1/consensus): 29 May 4.00/4.14/4.44; 1 Jun 4.03/4.17/4.45; 2 Jun 4.04/4.17/4.44; 3 Jun 4.08/4.22/4.49; [4 Jun 4.04/4.18/4.47]; 5 Jun
  4.15/4.27/4.53; 8 Jun 4.16/4.29/4.56; 9 Jun 4.12/4.24/4.52; 10 Jun 4.14/4.28/4.55; 11 Jun 4.06/4.18/4.46; 12 Jun 4.08/4.21/4.48.

## C. PAP Dzień na FX/FI (last piece on C)
Quote time of each last piece checked against the previous-session (middle) column of the next morning piece (all match). Only quote tables used.
Early pieces flagged when any of 2Y/5Y/10Y is >= 5bp off the Bloomberg PL C close (April/May rule).

| C | published | quotes | EURPLN | USDPLN | 2Y | PS0731 | DS0436 | |
|---|---|---|---|---|---|---|---|---|
| 29.05 | 17:06 | 16:55 | 4.2277 | 3.6227 | 4.39 (WS0428) | 5.16 | 5.60 | |
| 01.06 | 17:02 | 16:45 | 4.2375 | 3.6476 | 4.44 (WS0428) | 5.25 | 5.70 | |
| 02.06 | (3 Jun 09:32) | 16:20 | 4.2353 | 3.6385 | 4.43 (WS0428) | 5.21 | 5.66 | afternoon piece not found; prev-session column of the 3 Jun piece; flagged |
| 03.06 | 16:38 | 16:17 | 4.2407 | 3.6538 | 4.42 (WS0428) | 5.24 | 5.67 | |
| 05.06 | 14:34 | 14:25 | 4.2341 | 3.6381 | 4.46 (WS0428) | 5.27 | 5.71 | early; 9/9/8bp below BBG, **flagged** |
| 08.06 | 14:14 | 14:06 | 4.2422 | 3.6756 | 4.52 (WS0428) | 5.35 | 5.79 | early; 8/8/6bp below BBG, **flagged** |
| 09.06 | 17:34 | 17:14 | 4.2385 | 3.6651 | 4.46 (WS0428) | 5.27 | 5.71 | |
| 10.06 | 17:04 | 16:51 | 4.2462 | 3.6750 | 4.42 (WS0428) | 5.26 | 5.70 | |
| 11.06 | 17:13 | 16:55 | 4.2563 | 3.6951 | 4.35 (WS0428) | 5.19 | 5.66 | |
| 12.06 | 18:14 | 17:50 | 4.2444 | 3.6667 | 4.45 ("WS0428") | 5.09 | 5.57 | 2Y row apparently PS0728 from 12 Jun 09:16 (+12bp jump vs 4.35); flagged |
2Y switch: the 15 Jun 09:16 piece (after the last R) relabels the 2Y row **PS0728** with "-" in both previous columns; no "*nowy benchmark" marker. Not OK0129.
URLs are in curves.json under pap_close.url (R 3 Jun: the 3 Jun 09:32 piece).

## Flags (by R)
1 Jun: Erste stale CDS/spread (nulls); Erste US 4Y misprint; PAP TR holiday. 2 Jun: Erste spread change basis. 3 Jun: Erste spread ~9bp wide; PAP close source.
5 Jun: Erste header 03.06 (Corpus Christi); Erste spread; PAP raw edition / alt 0604. 8 Jun: Erste change columns (US/EZ vs 4 Jun); PAP close early.
9 Jun: PAP TR 2Y 05.06; PAP FR series jump; PAP close early. 10 Jun: Erste stale PL 10Y/spread (null); PAP TR 2Y 05.06. 11 Jun: Erste change columns + CDS copy.
12 Jun: Erste CDS frozen. 15 Jun: Erste CDS frozen; PAP 2Y roll.

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- R 2026-06-01: cds5y and pl_bund_10y null (stale copied table). R 2026-06-10: pl_bund_10y null (stale 10Y input). Nothing else null; nothing derived,
  reconstructed or filled from memory.
- No C-dated close for TR on 29 May (25/26 May closes) and TR 2Y on 8 and 9 Jun (5 Jun close): labelled and flagged.
- PAP close for 5 and 8 Jun only as early quotes (14:25, 14:06); for 2 Jun only via the next morning piece's previous-session column (original piece not found).
- Possibly stale CDS 10-12 Jun (kept, flagged); Erste spread 2 and 3 Jun probably ~9bp too wide (kept, flagged).

## Note for downstream (build_specs)
- No ERSTE override needed: for every R the irs_src is the R-dated daily with tables headed C (5 Jun daily headed 03.06 = C). A wording note for R 5 Jun:
  "Erste Codziennik of 5 Jun 2026 (tables headed 03.06.2026; no issue on 4 Jun, Corpus Christi)".
- Null spread/CDS: R 1 Jun (both) and R 10 Jun (spread): write_facts drops the CDS/spread sentence when either is null. If a carried CDS is wanted for R 1 Jun,
  the last valid print is 51 (28 May close); the 28 May spread 283 must NOT be carried (BBG gap fell 11bp on 29 May).
- Consider treating pl_bund_10y of R 3 Jun (280) and R 5 Jun (275) as suspect (~9bp above the usual basis; BBG gap 270/266) if the level is quoted.
- R 5 Jun: the builder switches to pap_table_0604_edition (10 after_C rows in the main table); both give identical C closes.
- 2Y comparisons across 11/12 Jun (BBG generic and pap_close.y2) mix WS0428 and the new 2Y bond (PS0728); FR 5Y/10Y across 5/8 Jun mix two BBG series.
- Flag strings start with "Erste", "PAP table" or "PAP close note" (R 15 Jun: "PAP table / PAP close note").

## Coordinator mid-run note (checked)
- 2Y roll WS0428 -> PS0728 on 12 Jun: confirmed from the tables (BBG +9 vs 5Y/10Y -10/-9; PAP 2Y 4.35 -> 4.47 overnight; Erste WS0428 -7; relabel PS0728 on 15 Jun).
  The BondSpot 12 Jun fixings quoted in the note (WS0428 4.27, PS0728 4.44) were not checked here; cited in the R 15 Jun flag as the fixings agent's finding.
  pap_close.y2 = 4.45 as printed (label WS0428), bonds unchanged (all null).
- Erste: 1 Jun issue spread row stale - confirmed (whole CDS/spread table copied; CDS also nulled); 8 Jun issue PL changes vs 3 Jun, US/EZ one-day (vs 4 Jun) -
  confirmed; 10 Jun issue 2L/10L and spread stale - confirmed; no 4 Jun issue and the 5 Jun issue all 3 Jun data - confirmed.
