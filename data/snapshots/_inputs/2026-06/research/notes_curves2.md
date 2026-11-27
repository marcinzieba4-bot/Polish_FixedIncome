# Working notes: June 2026 curves, part 2 (R 16-19, 22-26, 29, 30 Jun; C 15-19, 22-26, 29 Jun)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-05/research/curves_pap_2.json. scripts/finalize.py checks it against every
May part-2 R, and scripts/schema_check.py checks it more strictly against all 19 May R (parts 1 and 2; schema.log: 0 errors). The checks cover the top-level
key order (the optional `flags`, when present, always follows `irs_gap_note`), the key order of irs, fra, eur_irs, usd_irs, eurpln_session, irs_src,
pap_table, pap_close and pap_close.bonds, the row codes, every row's keys (the optional `note` is always last), and every leaf value type.
Optional keys used: `flags`, row `note`, `pap_close.note`. No alt edition key: no R edition has a row stamped after C, and no edition falls between C and R.
Content-level differences from May:
- **2Y benchmark: WS0428 -> PS0728 (not OK0129).** The Bloomberg PL 2Y generic rolled on 12 Jun (C of R 15 Jun, part 1). From the 15 Jun 09:16 piece the
  PAP FX/FI table lists PS0728 instead of WS0428. pap_close.y2 is PS0728 for every R here. Erste's bond table switched silently on 17.06 (see A, not
  used). Details in B and in the R 2026-06-16 flag.
- 5Y (PS0731) and 10Y (DS0436) are unchanged through 2 Jul (PAP FX/FI), and so is the Bloomberg 10Y generic. `pap_close.bonds` (OK0128/PS0131/DS1035)
  stays all null; the key set is kept.
- **Juneteenth (Fri 19 Jun, US holiday):** the Erste US IRS block headed 19.06 is a carry of the 18.06 levels. In the 22 Jun PAP edition, US d1 = the
  18 Jun close. In the 19 Jun edition (R = Juneteenth), US current = 1D. Flagged in R 22. Row notes in R 19 and R 26.
- **Erste PL-Bund spread 6-7bp below the BBG gap in the 24.06 and 25.06 tables.** Erste's Bund leg looks ~8bp too high, and it is back in line on 26/06.
  Flagged in R 25, 26 and 29.
- Two unstamped PAP editions: 19 Jun (07:33) and 26 Jun (07:36). Both follow the 29 May pattern: EU/CEE/TR current = C close, US/JP live -> d1.
  Each is verified across editions. Row notes only.
Raw parses: erste_raw_all.json (dailies 12 Jun to 1 Jul), paptab_raw.json (PAP tables 10 Jun to 8 Jul), fx_raw.json (FX/FI pieces 9 Jun to 2 Jul),
xcheck_obs.json (observations per series and date), curves_stage1.json (intermediate). Logs: stale.log, xcheck.log, schema.log.
Downloads: dl/ids.tsv (June/July ids from SP/dl/erste_archiwum.html, group 06-2026 and 07-2026), dl/erste (PDFs + pdftotext -layout), dl/si/tab
(PAP tables; x*.html = 404 pages), dl/si/fx (FX/FI pieces + fx_slugs.txt), dl/si/list (listing pages 250, 252-294 + all_links.json), dl/nbp/eur.json
(NBP table A EUR 12-30 Jun).
Scripts (new, written for June in the May style): erste.py (page-2 tables; section anchors at line start), stale.py (change columns vs day-on-day
differences + exact-copy test), paptab.py (standard / unstamped / raw-Bloomberg layouts), xcheck.py (cross-edition consensus), fxparse.py,
build.py (stage 1, with asserts on headers, footnote, row dates vs consensus and quote-time checks), finalize.py (notes, flags, key order, schema check),
schema_check.py. Run: `python3 -I scripts/erste.py dl/erste erste_raw_all.json; python3 -I scripts/stale.py erste_raw_all.json;
python3 -I scripts/paptab.py dl/si/tab paptab_raw.json; python3 -I scripts/xcheck.py paptab_raw.json xcheck_obs.json; python3 -I scripts/fxparse.py dl/si/fx
fx_raw.json; python3 -I scripts/build.py <W>; python3 -I scripts/finalize.py <W> <May curves_pap_2.json>`.
Renders: render/p2_20260622-2.png and p2_20260625-2.png (page 2). The FX, IRS PL/US/EZ, FRA, CDS/spread and bond tables match the parse, including the
zero-change US block of 19.06 and the PL spread 246 (-7) of 24.06.

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive: the copy already downloaded to SP/dl/erste_archiwum.html (the June ids are under data-item-group-id="06-2026"). Ids by publication date:
  12-06 169499, 15-06 169503 (chain base, C 12 Jun), 16-06 169515, 17-06 169517, 18-06 169523, 19-06 169525, 22-06 169527, 23-06 169531, 24-06 169534,
  25-06 169536, 26-06 169539, 29-06 169541, 30-06 169544 (01-07 169547: a cross-check of the 29/06 -> 30/06 change columns only).
  **A daily exists for every R.** URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL (curl -L).
  All PDFs are 4 pages with Erste Bank Polska branding. Only the page-2 tables were read. The archive's issue titles (which list later issues) were not used.
- PDF CreationDate (UTC) / URL upload stamp (CEST), all on the morning of R: 16 Jun 06:25:56Z / 08:27:06; 17 Jun 06:29:12Z / 08:31:00;
  18 Jun 06:35:52Z / 08:37:20; 19 Jun 05:50:29Z / 07:55:45; 22 Jun 06:31:05Z / 08:45:18; 23 Jun 06:53:51Z / 08:54:04; 24 Jun 06:23:23Z / 08:26:41;
  25 Jun 06:56:45Z / 08:57:06; 26 Jun 06:33:26Z / 08:52:15; 29 Jun 06:19:46Z / 08:40:09; 30 Jun 06:20:08Z / 08:32:18 (base 15 Jun 06:32:11Z / 08:39:23).
  None is late, so none is flagged.
- Header formats: dd.mm.yyyy in the 15 Jun to 26 Jun dailies (headed 12.06 to 25.06), dd/mm/yyyy in the 12, 29, 30 Jun and 1 Jul dailies. The decimal
  separator follows the same split (commas / points). The bid footnote "Informacje odnoszą się do stawek kupna na rynku międzybankowym na koniec dnia"
  and "Źródło: LSEG, Datastream" appear in every daily. In the 25 and 30 Jun dailies the text layer splits words ("Inf ormacje"), so the check
  ignores whitespace.
- EUR/PLN fixing in the Erste FX block = NBP table A of C for every C (113/A 4.2447 ... 123/A 4.2890; api.nbp.pl, fetched today, C-dated).
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026). Probes: p.250 = 3 Jul, p.280 = 17 Jun. Dates by page:
  12 Jun = p.286-288; 15 Jun = 284-286; 16 Jun = 281-284; 17 Jun = 278-281; 18 Jun = 274-278; 19 Jun = 272-274; 22 Jun = 270-272; 23 Jun = 268-270;
  24 Jun = 265-267; 25 Jun = 263-265; 26 Jun = 261-263; 29 Jun = 259-261; 30 Jun = 256-259; 1-2 Jul = 252-256; 9-11 Jun = 288-294.
  Pages 252-294 were fetched in ascending order. p.278 and p.284 failed on the first pass (connection reset) and were refetched together with
  277/279 and 283/285, so there is no gap.
- PAP table URL: /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. Editions exist for every weekday from 10 Jun to 8 Jul, including
  Juneteenth (19 Jun). 13, 14, 20, 21, 27, 28 Jun and 4, 5 Jul return 404 (no weekend editions).
- FX/FI pieces: two per C, three on 15 Jun (07:59 is a flash with no quote table). 24 Jun 09:14 failed once (connection reset) and returned 200 on retry.
  Only one 30 Jun FX/FI piece is listed (17:06). It serves only to confirm the 29 Jun quote time.
- BondSpot fixing yields (WS0428/PS0728/OK0129/PS0731/DS1035/DS0436) come from the coordinator's SP/jun/raw/bondspot_YYYYMMDD.json. They are C-dated
  values, used only to identify which bond a generic or table row tracks.

## A. Erste tables (main values in curves.json)
- For all 11 R the R-dated daily exists, and both its "Rynek stopy procentowej" header and its FX "Poprzednia sesja" header equal C. All values are
  direct reads; nothing is derived or reconstructed in this set.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set for every R.
- **Chain base (15 Jun daily, headed 12.06) and change columns.** For every transition 11/06 -> 12.06 -> 15.06 -> ... -> 25.06 -> 26/06 -> 29/06
  (-> 30/06 control), the IRS (PL/US/EZ), FRA, WIBOR, bond and PL-spread change columns match the day-on-day level differences within +-1bp
  (stale.log). The only misses are non-PL spreads (HU 15.06 "0 (0)", HU 16.06 221 (-32); not used) and the CDS change column (always 0; PL CDS 52 -> 50
  on 15.06), which is unreliable as before. No IRS, FRA, FX, WIBOR, bond or spread block is an exact copy of the previous daily's. CDS blocks are
  identical on 12.06, 17.06, 22.06 and 26/06 (normal: CDS move rarely).
- **R 2026-06-22 (C 19 Jun, Juneteenth): US IRS block = 18 Jun levels, flagged.** All seven change columns are 0. 1Y-8Y equal the 18.06 levels and the 10Y
  prints 4.31 vs 4.32, still with change 0 (render checked). usd_irs is kept as printed (the 18 Jun levels; no US session). PL IRS (+1..+3bp; BBG PL
  0/+1/-1), FRA, EZ IRS (+2..+5) and the spread are fresh, as are CDS and FX.
- **R 2026-06-18 (C 17 Jun):** US IRS +5..+15bp (1Y +15). This matches the BBG US 2Y/5Y/10Y move of +13/+10/+5 on 17 Jun (18 Jun edition 1D vs the
  17 Jun edition 1D). It is a real move, not flagged.
- **Erste PL-Bund spread vs BBG PL10Y-DE10Y gap** (Erste/BBG; the Bund leg implied by Erste, = 10L minus spread, vs BBG DE 10Y):
  12.06 261/259; 15.06 253/252; 16.06 251/250; 17.06 251/249; 18.06 255/253; 19.06 247/246; 22.06 247/247; 23.06 253/250 (2.91/2.92);
  **24.06 246/252 (2.95/2.87); 25.06 241/248 (2.95/2.86)**; 26/06 244/243 (2.85/2.85); 29/06 247/244 (2.86/2.86).
  Erste normally sits 0-3bp above the BBG gap. In the 24.06 and 25.06 tables it sits 6-7bp below. The Erste 10Y yield is fine there (10L 5.41/5.36 vs BBG
  5.39/5.34), so the problem is Erste's Bund leg: it rose to 2.95 while the BBG DE 10Y fell to 2.87/2.86. Erste's FR/IT/PT spreads (68/65/31, 68/66/31)
  are 6-9bp below their Bloomberg equivalents too. The cause is a reference-bond change or a bad Bund print. It is back to normal on 26/06, where the
  printed PL +3 and FR/IT/PT +9/+10 reflect the end of the distortion (BBG gap -5). Flags: R 25 and R 26 (level ~6-7bp too low), R 29 (change not a
  market move). pl_bund_10y is a direct read everywhere.
- EUR/PLN close, Erste vs the PAP last quote: 15.06 4.2487/4.2489 (17:05); 16.06 4.2373/4.2396 (16:35); 17.06 4.2409/4.2420 (16:53);
  18.06 4.2597/4.2571 (16:42); 19.06 4.2576/4.2572 (17:00); 22.06 4.2728/4.2738 (15:18); 23.06 4.2814/4.2832 (16:26); 24.06 4.2906/4.2888 (16:50);
  25.06 4.2825/4.2815 (16:36); 26/06 4.2873/4.2870 (16:50); 29/06 4.2882/4.2885 (15:10). All within 26 pips. OK.
- Erste bond table (not requested, not used):
  - **'2L' (label WS0428 throughout) switches silently to PS0728 in the table headed 17.06.** It went 4.17 -> 4.27 (+10) while BBG PL 2Y moved -1
    (4.30 -> 4.29), PAP PS0728 -1 (4.27 -> 4.26), PL IRS 2Y +2 and the BondSpot fixings WS0428 -2 / PS0728 0. Up to 12.06 the 2L equals the WS0428
    fixing (12.06 4.27/4.27). From 17.06 it runs 0-3bp from the BBG 2Y generic (= PS0728) and 1-6bp above the PS0728 fixing. It is not OK0129
    (fixing 4.37-4.43 on 17-19 Jun).
  - '10L' (label DS1035) is DS0436 as in late May: 15.06 5.48 vs DS0436 fixing 5.44, DS1035 fixing 5.39.
  - '5L' PS0731 runs 7-13bp above PAP PS0731, as in May, and is noisy: 22.06 4.93 (-14) vs BBG -6; 23.06 4.99 (+7) vs BBG -1; 26/06 4.78 (-14) vs BBG -6;
    29/06 4.84 (+6) vs BBG -1.
  - Erste non-PL spreads are noisy as well (FR 12.06 64 vs BBG 75, back to 74 on 15.06; HU 15.06 = 0).

## B. PAP/Bloomberg tables
- Columns: current, 1D, 5D, 1M, 3M, 12M (arrays in that order; HU uses 3Y). R editions: 16 Jun (06:35), 17 (06:34), 18 (06:34), 19 (07:33, unstamped),
  22 (06:36), 23 (06:35), 24 (06:34), 25 (06:34), 26 (07:36, unstamped), 29 (06:37), 30 (06:34).
- Stamped editions: all 11 EU/CEE/TR rows are stamped exactly C, except TR 10Y on 23 Jun (below). JP/US are clock-stamped 06:29-06:35 on the morning of
  R, before publication: live, d1 used. In the 23 Jun edition the US tenors carry different clock stamps (06:33/06:32/06:32), stored as a list.
  No row is stamped after C (after_C false everywhere) and none is intraday on C.
- **19 Jun edition (07:33, unstamped; R = Juneteenth):** EU/CEE/TR current = 18 Jun close (22 Jun edition 1D col, 26 Jun edition 5D col). JP is live
  (14:33 JST; current differs from 1D; 1D = 18 Jun close, 5D = 12 Jun close). US current = 1D = 18 Jun close in all three tenors. The 5D col
  (4.08/4.21/4.48) is the 12 Jun close, not the 11 Jun one (4.06/4.18/4.46), so the row is a 19 Jun morning quote with no trading on the US holiday.
  It is marked live and d1 = C close. Row notes, no flag.
- **22 Jun edition (C 19 Jun = Juneteenth): US live, d1 = 4.18/4.23/4.45 = the 18 Jun close** (= the 19 Jun edition 1D col; the 26 Jun edition 5D col
  gives the same value for 19 Jun). JP d1 = the 19 Jun close. All EU/CEE/TR rows are stamped 19.06. Flagged (R 22).
- **23 Jun edition: TR 10Y stamped 19.06.2026** (2Y/5Y 22.06). The tenor is identical to the 22 Jun edition's (30.90 = 19 Jun close; the 24 Jun edition
  1D col and the 30 Jun edition 5D col also give 30.90 for 22 Jun). c_close 10Y = the 19 Jun close. Flagged (R 23). Note for the builder: row_stamps
  uses stamp[0] for list stamps, so it labels TR 10Y "22.06" (same limitation as the May 27 TR row).
- **26 Jun edition (07:36, unstamped):** EU/CEE/TR current = 25 Jun close (29 Jun edition 1D col, 3 Jul edition 5D col). US/JP are live (current differs
  from 1D; 1D = 25 Jun close = the 2 Jul edition 5D col; 5D = the 19 Jun value, which for US is the 18 Jun close carried). Row notes, no flag.
- **Bloomberg PL 2Y generic roll (12 Jun):** the generic went 4.38 (11 Jun) -> 4.47 (12 Jun, +9) while the 5Y/10Y generics fell 10/9bp, Erste
  WS0428 fell 7 and IRS 2Y fell 10. BondSpot fixings 11/12 Jun: WS0428 4.34/4.27, PS0728 4.51/4.44. So the generic tracks PS0728 from 12 Jun
  (C close vs PS0728 fixing: 15 Jun 4.34/4.31 ... 29 Jun 4.14/4.10). PL row notes in every R say which 2Y columns predate the roll: the 5D col until
  R 19 Jun (5D = 8-11 Jun) and the 1M/3M/12M cols throughout. Flag in R 16 (combined PAP table / PAP close note).
- Identical consecutive rows (10 Jun to 8 Jul editions): none. Identical single tenors: TR 10Y 22->23 Jun (above), TR 10Y 1->2 Jul and CZ 10Y 6->7 Jul
  (outside the set). No stale edition.
- Cross-check (scripts/xcheck.py, editions 10 Jun to 8 Jul). As-of model: 1D = previous weekday of the row date, 5D = row date - 7. Unstamped editions
  are dated EU/CEE/TR = previous weekday and JP/US = edition date. Result: **0 conflicts** across all 39 country/tenor series. Every C in scope has at
  least 2 close observations for every series. build.py asserts every row's c_close against this consensus.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 15.06 4.34/4.98/5.47 vs 4.32/4.96/5.45; 16.06 4.30/4.95/5.43 vs 4.27/4.93/5.41; 17.06 4.29/4.93/5.42 vs
  4.26/4.91/5.40; 18.06 4.34/4.97/5.46 vs 4.30/4.95/5.44; 19.06 4.34/4.98/5.45 vs 4.31/4.97/5.44; 22.06 4.29/4.92/5.42 vs 4.28/4.92/5.42 (15:18);
  23.06 4.27/4.91/5.42 vs 4.25/4.90/5.41; 24.06 4.23/4.87/5.39 vs 4.19/4.86/5.38; 25.06 4.18/4.83/5.34 vs 4.16/4.82/5.33; 26.06 4.14/4.77/5.28 vs
  4.10/4.75/5.27; 29.06 4.14/4.76/5.30 vs 4.12/4.76/5.30 (15:10). The BBG 2Y runs 1-4bp above PAP PS0728 (as it did above WS0428 in May).

## C. PAP Dzień na FX/FI (last piece on C)
Each quote time was checked against the matching column of the next FX/FI piece (build.py asserts that the EUR/PLN and PS0728 values are identical).
Only the quote tables were used; no commentary. Benchmarks: 2Y PS0728, 5Y PS0731, 10Y DS0436 for every C in the set. Early pieces are flagged when any
of 2Y/5Y/10Y is >= 5bp off the Bloomberg PL C close (April rule).

| C | published | quotes | EURPLN | USDPLN | PS0728 | PS0731 | DS0436 | |
|---|---|---|---|---|---|---|---|---|
| 15.06 | 17:20 | 17:05 | 4.2489 | 3.6615 | 4.32 | 4.96 | 5.45 | first C with PS0728 (09:16 piece: PS0728 4.38, previous columns '-'); 07:59 flash without table; flagged (benchmark) |
| 16.06 | 16:44 | 16:35 | 4.2396 | 3.6575 | 4.27 | 4.93 | 5.41 | |
| 17.06 | 17:02 | 16:53 | 4.2420 | 3.6592 | 4.26 | 4.91 | 5.40 | |
| 18.06 | 16:53 | 16:42 | 4.2571 | 3.7111 | 4.30 | 4.95 | 5.44 | |
| 19.06 | 17:13 | 17:00 | 4.2572 | 3.7130 | 4.31 | 4.97 | 5.44 | the piece labels its 17:00 column "czwartek" (typo); 22 Jun 09:18 prev col "piątek 17:00" |
| 22.06 | 15:30 | 15:18 | 4.2738 | 3.7348 | 4.28 | 4.92 | 5.42 | early; 23 Jun 09:54 prev col "poniedziałek 15:18"; 1/0/0bp vs BBG, not flagged |
| 23.06 | 16:48 | 16:26 | 4.2832 | 3.7638 | 4.25 | 4.90 | 5.41 | |
| 24.06 | 17:13 | 16:50 | 4.2888 | 3.7817 | 4.19 | 4.86 | 5.38 | 24 Jun 17:13 and 25 Jun 09:20 pieces print times without weekday labels |
| 25.06 | 16:48 | 16:36 | 4.2815 | 3.7635 | 4.16 | 4.82 | 5.33 | |
| 26.06 | 17:17 | 16:50 | 4.2870 | 3.7558 | 4.10 | 4.75 | 5.27 | |
| 29.06 | 15:15 | 15:10 | 4.2885 | 3.7605 | 4.12 | 4.76 | 5.30 | early; 30 Jun 17:06 piece (only 30 Jun FX/FI piece listed) prev col "pon. 15:10"; 2/0/0bp, not flagged |
Before the set (C of R 15 Jun, curves1 territory): the 12 Jun pieces still label the 2Y row WS0428, but it already jumped 4.35 (11 Jun 16:55) ->
4.47 (12 Jun 09:16) -> 4.45 (17:50), against Erste/BondSpot WS0428 4.27 and PS0728 4.44. It looks like PS0728 under the old label, as with
DS1035/DS0436 on 7-11 May. URLs are in curves.json under pap_close.url.

## Flags (by R)
- 16 Jun: PAP table / PAP close note: 2Y roll WS0428 -> PS0728 (BBG generic 12 Jun, PAP table relabel 15 Jun).
- 17, 18, 19 Jun: none (19 Jun: unstamped edition, row notes only).
- 22 Jun: Erste US IRS = 18 Jun carry (Juneteenth); PAP US d1 = 18 Jun close.
- 23 Jun: PAP TR 10Y stamped 19.06 (no 22 Jun print).
- 24 Jun: none. 25 Jun: Erste spread 6bp below the BBG gap (Bund leg). 26 Jun: same, 7bp below. 29 Jun: Erste spread back in line, printed change not a
  market move. 30 Jun: none.
- Not flagged (notes only): Erste bond-table 2Y switch on 17.06 (no output field uses the Erste bond table); unstamped PAP editions; early PAP pieces
  within 2bp.

## Gaps
- IRS 7Y: null for all R (Erste does not publish it). Nothing else is null; nothing is derived, reconstructed or filled from memory.
- Not C-dated, labelled and flagged: usd_irs in R 22 (18 Jun levels carried); US d1 in R 22 (18 Jun close); TR 10Y c_close in R 23 (19 Jun close).
- The PAP close for 22 and 29 Jun exists only as early quotes (15:18, 15:10), within 0-2bp of BBG.

## Note for downstream (build_specs)
- No ERSTE special-case entries are needed: every irs_src is the R-dated daily with the table headed C. R 22 usd_irs = the 18 Jun levels (not used by
  the builder). If the report quotes the Erste PL-Bund spread, R 25/26 levels are ~6-7bp too low vs the BBG gap and the R 26 -> R 29 change is distorted
  (see flags). pl_bund_10y is a direct read everywhere (DERIVED_SPREAD stays empty).
- No alt pap_table edition and no after_C rows. Live rows (JP/US in every R) are dropped by the builder; US comes from the Treasury curve. For C = 19 Jun
  (Juneteenth) no Treasury curve exists, so the builder's `max(d <= C)` picks 18 Jun, which matches the PAP d1.
- PL 2Y in pap rows and pap_close.y2 is PS0728 for every R here. Any comparison with dates before 12 Jun (5D col up to R 19, 1M/3M/12M, or y2 from the
  part-1 R) mixes WS0428 and PS0728 (PS0728 ~12-18bp above WS0428 on the June BondSpot fixings). If the static bond universe needs PS0728 (PL0000115192), it is quoted on BondSpot
  throughout June.
- Flag strings start with "Erste" or "PAP table" (R 16's starts "PAP table / PAP close note").
