# Working notes: May 2026 curves, part 2 (R 15, 18-22, 25-29 May; C 14, 15, 18-22, 25-28 May)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-04/research/curves_pap_2.json, checked programmatically
(scripts/finalize.py asserts, against EVERY April R: top-level key order (minus the optional `flags`, which always follows `irs_gap_note`), the key order
of irs, fra, eur_irs, usd_irs, eurpln_session, irs_src, pap_table, pap_close, pap_close.bonds, the row codes and every row's keys (minus the optional
`note`, always last), plus value types). Optional keys used: `flags`, `irs_gap_note`, row `note`, `pap_close.note`. No alt edition keys.
Content-level differences from April:
- **10Y benchmark is DS0436 for every C in this set.** The PAP FX/FI table switched from DS1035 to DS0436 in the 12 May 09:57 piece (09:45 quotes marked
  "*nowy benchmark"; outside this set, found while dating the switch). pap_close.y10 carries DS0436 and `bonds.DS1035` is null. With OK0128 (2Y = WS0428
  since 26 Mar) and PS0131 (5Y = PS0731 since 28 Apr) also no longer quoted, **all three `pap_close.bonds` values are null**; the key set is kept.
- **No 2Y switch to OK0129 by 28 May**: the PAP FX/FI table quotes WS0428 through the 3 Jun piece. The Bloomberg PL generics show no roll either.
- **Erste switched its 10Y (bond table and PL-Bund spread) from DS1035 to DS0436 between the 15.05 and 18.05 tables**, label unchanged (see A, flagged).
- Whit Monday (25 May) is handled row by row in R 2026-05-26; Turkish holidays (19 May; Kurban Bayrami 26 May half day, 27-30 May) and US Memorial
  Day (25 May) produce stamp-before-C rows (flagged, as April did for TR 23 Apr and JP 29 Apr).
- Two PAP editions are unstamped: 15 May (07:42, a new "raw Bloomberg" layout with ticker columns and no header row) and 29 May (07:52, the 17 Apr
  pattern). Both follow the April rule (EU/CEE/TR current = C close, US/JP live -> d1), verified across editions.
Raw parses: erste_raw_all.json (13-29 May dailies), paptab_raw.json (PAP tables 12 May to 5 Jun), fx_raw.json (FX/FI pieces 13 May to 3 Jun),
xcheck_obs.json (per series/date observations), pdfinfo.json, curves_stage1.json (intermediate); logs stale.log, xcheck.log, finalize.log.
Downloads: dl/erste (archiwum.html, ids_all.tsv, ids.tsv, PDF + pdftotext -layout; e20260601 used only as a cross-check), dl/si/tab (PAP tables;
x*.html = 404 pages), dl/si/fx (FX/FI pieces + fx_slugs.txt; early/ = 5-12 May pieces used only to date the DS0436 switch), dl/si/list (listing pages
300-362 + all_links.json).
Scripts (copied from agent_apr_curves2 and adapted): erste.py (table anchors now match the table headers, because the 26 May and 29 May dailies mention
"Stawki FRA"/"Stawki IRS" in the commentary first), paptab.py (also parses the raw Bloomberg layout), fxparse.py, stale.py, xcheck.py (May unstamped
editions and holiday-copy overrides), build.py (stage 1, with per-row date expectations and special row notes), finalize.py (flags, pap_close notes,
key-order/schema asserts vs April). Run: `python3 -I scripts/build.py <W>` then `python3 -I scripts/finalize.py <W> <april curves_pap_2.json>`.
Renders: render/ (page 2 of the 15, 26 and 29 May dailies; spot-checked FX, IRS PL/US/EZ, FRA, CDS/spread and bonds against the parse: all match,
incl. the US 4Y 4.33 (+19) print on 29 May).

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum). Ids by publication date:
  13-05 169422, 14-05 169425, 15-05 169429, 18-05 169434, 19-05 169438, 20-05 169442, 21-05 169443, 22-05 169446, 25-05 169448, 26-05 169452,
  27-05 169454, 28-05 169462, 29-05 169465 (01-06 169472, cross-check only). **A daily exists for every R; none is missing.**
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. All PDFs 4 pages, Erste Bank Polska branding.
  Only the PDFs' page-2 tables were read; the archive page's issue titles (it lists later issues too) were not used.
- PDF CreationDate (UTC) / URL upload stamp (CEST), all on the morning of R: 15 May 06:55:41Z / 08:59:03; 18 May 06:34:09Z / 08:38:08;
  19 May 06:21:46Z / 08:24:15; 20 May 06:42:25Z / 08:46:43; 21 May 06:36:41Z / 08:37:29; 22 May 06:38:21Z / 08:40:29; 25 May 06:58:34Z / 09:03:25;
  26 May 05:45:05Z / 08:05:28; 27 May 05:53:58Z / 08:42:20; 28 May 07:15:04Z / 09:16:35; 29 May 06:34:50Z / 08:52:04. None late; not flagged.
- Header formats: dd/mm/yyyy in the 14, 15, 20, 22 and 25 May dailies, dd.mm.yyyy elsewhere; decimal points in the 14, 15, 20, 22, 25 May dailies,
  commas elsewhere. The 22 May daily prints the EURPLN fixing with 3 decimals ("4.246"), stored as a number.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026): 14 May = p.337-340; 15 May = 335-337; 18 May = 332-335;
  19 May = 330-332; 20 May = 326-330; 21 May = 322-326; 22 May = 320-322; 25 May = 317-319; 26 May = 315-317; 27 May = 312-315; 28 May = 309-312;
  29 May = 306-309. Pages 300-342 fetched in ascending order (all 200; probe 320 failed once and was refetched in the run), 343-362 for 4-12 May.
  The 20 May table is not linked from any listing page (329-331 refetched) but its URL returns 200. Two FX/FI pieces per day for every C.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. Editions: every weekday 12 May to 5 Jun (incl. Whit Monday 25 May
  and Corpus Christi 4 Jun). 16, 17, 23, 24, 30, 31 May return 404 (no weekend editions). 12 and 15 May failed on the first pass (proxy tunnel closed)
  and returned 200 on retry.

## A. Erste tables (main values in curves.json)
- For all 11 R the R-dated daily exists and both its "Rynek stopy procentowej" header and its FX "Poprzednia sesja" header equal C. All values are
  direct reads; nothing is derived or reconstructed in this set.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set for every R.
- **First R (15 May), compared with the 14 May daily (headed 13/05):** every IRS (PL/US/EZ), FRA, PL spread and bond change column in the 15 May daily
  (headed 14/05) matches the day-on-day difference within +-1bp; no block is a copy.
- IRS (PL/US/EZ), FRA, PL-Bund spread and bond change columns match the day-on-day level differences within +-1bp for EVERY transition
  12.05 -> 13/05 -> 14/05 -> 15.05 -> 18.05 -> 19/05 -> 20.05 -> 21/05 -> 22/05 -> 25.05 -> 26.05 -> 27.05 -> 28.05 (stale.log). Only non-PL
  spread entries miss (ES 13/05, HU 25.05; not used). No IRS, FRA, FX, CDS, spread or bond block is an exact copy of the previous daily's.
  The CDS change column is always 0 even when the level moves (PL 53 -> 51 on 27.05), unreliable as before.
- **Erste 10Y benchmark (flagged in R 15, 18, 19).** Up to the table headed 15.05 the Erste bond table '10L' is DS1035 and the PL-Bund spread is
  computed off it (14/05: 5.79 - Bund 3.04 ~ 275), while PAP (since 12 May) and the Bloomberg PL 10Y generic are on DS0436. Erste spread vs
  BBG PL10Y-DE10Y gap: 13/05 273/282; 14/05 275/282; 15.05 280/285, i.e. 5-9bp BELOW instead of the usual 1-4bp above. In the table headed 18.05 the
  '10L' (label still DS1035) jumps 5.95 -> 6.03 (+8) while BBG PL 10Y is unchanged (6.02/6.02) and PAP DS0436 +3bp, and the spread prints 287 (+7) vs a
  BBG gap move of +2: a silent switch to DS0436. From then on: 18.05 287/287; 19/05 286/285; 20.05 285/283; 21/05 283/281; 22/05 285/282;
  25.05 283/282; 26.05 280/278; 27.05 281/279; 28.05 283/281 (0-3bp above, normal). pl_bund_10y is a direct read everywhere; R 15/R 18 values are on
  the old bond (understate the DS0436 spread by ~5-8bp) and the 15->18 May change mixes two bonds.
- **R 2026-05-26 (C 25 May, Whit Monday; London (Spring Bank Holiday) and New York (Memorial Day) closed): flagged.** The table is headed 25.05 and is
  not a copy (PL IRS 1Y/10Y and FRA 6x9/9x12/6x12 differ from 22.05; change columns consistent), but PL IRS changes are 0/+1/+1/0/0/0/0bp and FRAs
  0/0/-1/+1/0/0bp while PL bonds fell 6-10bp (BBG -6/-7/-9; Erste bond table 5Y/10Y -10/-10), EZ IRS -9 to -13bp and Bunds -9/-10bp. Erste's own
  commentary in that issue says IRS and FRA were practically unchanged. Probably thin holiday contributions to the LSEG composite; kept as published.
  US IRS = 22.05 levels with zero changes (no US session). Cross-check after R (not used, hindsight): the 27 May daily's PL IRS change column is
  -5 to -9bp for 26 May while BBG PL moved -2/-1/-1, consistent with a delayed catch-up.
- **R 2026-05-29: US IRS 4Y 4.33 (+19)** between 3Y 4.13 and 5Y 4.14 while all other US tenors fell 1-5bp: misprint/bad LSEG point, kept as published
  and flagged (render confirms the print). Cross-check after R (not used): the 1 Jun daily still prints US 4Y 4.33 (0).
- EZ IRS single-tenor noise of 2-5bp (not flagged, eur_irs is not used by the spec builder): 14/05 4Y 2.87 (-5) below 3Y 2.89 (0) and 5Y 2.89;
  21/05 3Y 2.85 (-2) below 2Y 2.88 (+2) and 4Y 2.91 (+1).
- EUR/PLN close, Erste vs the PAP last quote: 14.05 4.2394/4.2401 (16:52); 15.05 4.2459/4.2442 (16:54); 18.05 4.2431/4.2445 (13:55);
  19.05 4.2517/4.2506 (16:48); 20.05 4.2463/4.2477 (16:42); 21.05 4.2453/4.2453 (16:43); 22.05 4.2380/4.2390 (16:45); 25.05 4.2303/4.2323 (15:26);
  26.05 4.2359/4.2320 (14:39); 27.05 4.2330/4.2346 (14:31); 28.05 4.2267/4.2275 (17:03). OK.
- Erste bond table (not requested, not used): the '5L' (PS0731) runs ~7-13bp above PAP PS0731 throughout; the '2L' (WS0428) prints 4.62 (+10) at
  28.05 against BBG 2Y +3 and PAP WS0428 +4 (looks like a glitch; the 1 Jun daily has 4.39). Labels unchanged (WS0428/PS0731/DS1035).

## B. PAP/Bloomberg tables
- Columns current, 1D, 5D, 1M, 3M, 12M (arrays in that order; HU uses 3Y). R editions: 15 May (07:42, raw layout, unstamped), 18 (06:34), 19 (06:36),
  20 (06:34), 21 (06:32), 22 (06:41), 25 (06:34), 26 (06:38), 27 (06:39), 28 (06:34), 29 (07:52, unstamped).
- 19, 21, 22 and 25 May editions: all 11 EU/CEE/TR rows stamped exactly C; 27 and 28 May: all except TR. JP/US are clock-stamped on the morning of R
  (live, d1 used) except US in the 25 May edition. In the 21 May edition the
  JP tenors carry different clock stamps (06:30/06:29), stored as a list.
- **15 May edition: new raw Bloomberg layout** (columns: ticker e.g. "POGB2YR Index", description, country, tenor, 6 values; no header row, no stamp
  column; the intro text gives the column order). `columns` = ["(no header row; intro: rentowność aktualna)", "1D", ...]. EU/CEE/TR current = 14 May
  close (18 May edition 1D col; 22 May edition 5D col). US/JP inferred live 15 May (1D = 14 May close, confirmed by the 21 May edition 5D col; 5D = 8 May
  close = 12 May edition 1D col); 07:42 CEST = 14:42 JST. Row notes only, no flag (April precedent for unstamped editions). The 5 Jun edition (outside the
  set, cross-check only) has the same raw layout.
- **29 May edition (07:52): no stamp column** (17 Apr pattern). EU/CEE current = 28 May close (1 Jun edition 1D col, 5 Jun edition 5D col); US/JP live
  29 May (d1 = 28 May close, confirmed by the 4 Jun edition 5D col). TR row = holiday copy (below). Row notes + a PAP flag (because of TR).
- **18 May edition: TR 2Y stamped 14.05** (5Y/10Y 15.05): no 15 May TR 2Y print; TR 2Y c_close = 38.64 = 14 May close. Flagged.
- **20 May edition: TR stamped 18.05** (19 May Commemoration of Ataturk, Youth and Sports Day); row identical to the 19 May edition's. c_close = 18 May
  close. Flagged.
- **25 May edition (R = Memorial Day): US stamped 22.05, NOT live**; current col = 22 May close (used; live = false). JP live as usual. Flagged.
- **26 May edition (C = Whit Monday 25 May), classified row by row relative to C:** PL, CZ, TR, IE, IT, PT, ES, FR and DE stamped 25.05 = C (DE printed
  despite the German holiday: Bund generics -10/-10/-9bp, confirmed later by the 27 May 1D col); **HU (public holiday) and UK (Spring Bank Holiday)
  stamped 22.05**, rows identical to the 25 May edition's: c_close = 22 May close, not C-dated; **US live but d1 = 22 May close** (Memorial Day);
  JP live, d1 = 25 May close. No row is stamped after C (after_C false everywhere; intraday_on_C false). Flagged.
- **27 May edition: TR 2Y/10Y stamped 25.05, 5Y 26.05** (Arife, half-day before Kurban Bayrami): c_close 2Y/10Y = 25 May close, 5Y = 26 May close. Flagged.
- **28 May edition: TR stamped 25.05/26.05** (Kurban Bayrami 27-30 May), identical to the 27 May edition's row (also in the 29 May and 1 Jun
  editions). c_close = last TR closes, not C-dated. Flagged (R 28 and R 29).
- Identical rows between consecutive editions (12 May to 5 Jun): only TR 19->20 May, HU and UK 25->26 May, TR 27->28->29 May->1 Jun, and PL 4->5 Jun
  (Corpus Christi, outside the set), all holiday carry-overs. No stale edition.
- The rule about editions between C and R was not triggered: no weekend editions, no R edition has a row stamped later than C.
- Full cross-check (scripts/xcheck.py, editions 12 May to 5 Jun; as-of model 1D = previous weekday of the row date, 5D = row date - 7; unstamped
  editions dated by hand; 29 May TR and 5 Jun PL rows dated by their copy source): for every C all 39 country/tenor series have **0 conflicts**;
  single observations only for US 18 May (19 May edition 1D; noted in the row) and for TR on its holidays (19, 26, 27, 28 May; carry-over values equal to
  the last TR close, which itself has 3-7 observations). build.py asserts every row date and every c_close against this consensus.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 14.05 4.60/5.39/5.86 vs 4.58/5.38/5.85; 15.05 4.76/5.56/6.02 vs 4.72/5.56/5.99; 18.05 4.76/5.57/6.02 vs
  4.76/5.57/6.02 (13:55); 19.05 4.78/5.59/6.04 vs 4.74/5.56/6.00; 20.05 4.67/5.47/5.93 vs 4.65/5.48/5.93; 21.05 4.65/5.45/5.91 vs 4.61/5.43/5.89;
  22.05 4.60/5.41/5.86 vs 4.58/5.40/5.84; 25.05 4.54/5.34/5.77 vs 4.49/5.29/5.75 (15:26); 26.05 4.52/5.33/5.76 vs 4.51/5.32/5.76 (14:39);
  27.05 4.55/5.35/5.78 vs 4.50/5.29/5.74 (14:31); 28.05 4.58/5.35/5.77 vs 4.54/5.33/5.76. BBG 2Y runs 2-4bp above WS0428 as in April.

## C. PAP Dzień na FX/FI (last piece on C)
Two FX/FI pieces per C (morning + afternoon/early afternoon). Each quote time was checked against the previous-session column of the next morning's piece
(all match, middle column). Only the quote tables were used; no commentary. Benchmarks: 2Y WS0428, 5Y PS0731, 10Y DS0436 throughout.
Early pieces are flagged when any of 2Y/5Y/10Y is >= 5bp off the Bloomberg PL C close (April rule).

| C | published | quotes | EURPLN | USDPLN | WS0428 | PS0731 | DS0436 | |
|---|---|---|---|---|---|---|---|---|
| 14.05 | 17:06 | 16:52 | 4.2401 | 3.6269 | 4.58 | 5.38 | 5.85 | |
| 15.05 | 17:08 | 16:54 | 4.2442 | 3.6500 | 4.72 | 5.56 | 5.99 | |
| 18.05 | 14:00 | 13:55 | 4.2445 | 3.6462 | 4.76 | 5.57 | 6.02 | early; 19 May morning prev col = "pon. 13:55"; 0/0/0bp vs BBG, not flagged |
| 19.05 | 17:06 | 16:48 | 4.2506 | 3.6650 | 4.74 | 5.56 | 6.00 | |
| 20.05 | 17:02 | 16:42 | 4.2477 | 3.6569 | 4.65 | 5.48 | 5.93 | |
| 21.05 | 16:52 | 16:43 | 4.2453 | 3.6631 | 4.61 | 5.43 | 5.89 | |
| 22.05 | 17:02 | 16:45 | 4.2390 | 3.6537 | 4.58 | 5.40 | 5.84 | |
| 25.05 | 15:51 | 15:26 | 4.2323 | 3.6344 | 4.49 | 5.29 | 5.75 | early; 5/5/2bp below BBG, **flagged** |
| 26.05 | 14:46 | 14:39 | 4.2320 | 3.6377 | 4.51 | 5.32 | 5.76 | early; 1/1/0bp, not flagged |
| 27.05 | 14:41 | 14:31 | 4.2346 | 3.6324 | 4.50 | 5.29 | 5.74 | early; 5/6/4bp below BBG, **flagged** |
| 28.05 | 17:20 | 17:03 | 4.2275 | 3.6284 | 4.54 | 5.33 | 5.76 | |
URLs are in curves.json under pap_close.url. bonds.OK0128/PS0131/DS1035 are null for every R (none quoted).

## Flags (by R)
- 15 May: Erste spread basis (DS1035). 18 May: Erste spread basis; PAP TR 2Y 14.05. 19 May: Erste 10Y switch. 20 May: PAP TR 18.05. 21, 22 May: none.
- 25 May: PAP US stamped 22.05 (Memorial Day). 26 May: Erste Whit Monday IRS/FRA; PAP Whit Monday rows (HU/UK/US); PAP close early (15:26).
- 27 May: PAP TR mixed stamps. 28 May: PAP TR holiday; PAP close early (14:31). 29 May: Erste US IRS 4Y misprint; PAP unstamped edition + TR holiday.

## Gaps
- IRS 7Y: null for all R (not published by Erste). Nothing else is null; nothing derived, reconstructed or filled from memory.
- No C-dated close exists for TR on 19, 27, 28 May (and 2Y/10Y on 26 May, 2Y on 15 May), HU/UK/US on 25 May: c_close = last close before C, labelled
  and flagged.
- PAP close for 18, 25, 26, 27 May only as early quotes (13:55, 15:26, 14:39, 14:31).
- US 18 May close seen only once across editions (noted).

## Note for downstream
- Flag strings start with "Erste", "PAP table" or "PAP close note". The April spec builder does not null pl_bund_10y on flags (only DERIVED_SPREAD);
  no spread in this set is derived. If a builder nulls pl_bund_10y on any flag, note that only R 15/18/19 Erste flags concern the spread (basis/
  benchmark change, levels are direct reads); R 26's Erste flag concerns PL IRS/FRA and says the spread is fine; R 29's concerns US IRS 4Y only.
- pap_close.y10 is DS0436 for every R here (DS1035 before 12 May): y10 series across 11/12 May mix two bonds (curves part 1 territory).
- irs_src.header_date is always the C-dated header; for all R the irs_src is the R-dated daily (no ERSTE special-case entries needed).
- For R 26 May the US row (live) and HU/UK rows carry 22 May closes; a "C closes" table built from non-live rows should label HU/UK as 22 May.
