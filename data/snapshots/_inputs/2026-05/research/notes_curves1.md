# Working notes: May 2026 curves, part 1 (R 4-8, 11-14 May; C 30 Apr, 4-8, 11-13 May)
Output: curves.json in this folder, keyed by R. Same schema as 2026-04/research/curves_pap_1.json, checked programmatically (scripts/build_may.py asserts
and scripts/schema_check.py run against curves_pap_1.json and curves_pap_2.json): identical top-level, irs/fra/eur_irs/usd_irs/eurpln_session/irs_src,
pap_table, row and pap_close (+bonds) key sets and key order; the full key signature of every R equals that of an April R.
Optional keys used: `flags` (right after irs_gap_note), row `note`, and one alt edition `pap_table_0501_edition` in R 2026-05-04 (placed right after
pap_table, with a `why` key, as `pap_table_0406_edition` in April R 7 Apr). `irs_gap_note` is extended in R 2026-05-05.
Benchmarks: 2Y WS0428 throughout (`bonds.OK0128` null), 5Y PS0731 throughout (`bonds.PS0131` null), 10Y DS1035 to C = 11 May, **DS0436 from C = 12 May**
(`bonds.DS1035` null in R 13 and 14 May).
Content-level novelties: R 4 May Erste values read under a 01.05 header (PL = 30 Apr closes) with US/EZ IRS DERIVED; R 5 May PL IRS NULL (stale feed);
Bloomberg/PAP 10Y apparently rolled to DS0436 on 7 May.
Raw parses: erste_raw_all.json (27 Apr to 18 May dailies), erste_ctrl.json (control dailies 22, 25, 26, 27 May, 31 Aug, 1, 2 Sep; feed-behaviour check only),
paptab_raw.json (PAP tables 28 Apr to 22 May), fx_raw.json (FX/FI pieces 29 Apr to 15 May), xcheck_obs.json, stale_out.txt, xcheck_out.txt.
Downloads: dl/erste (archiwum.html, ids.tsv, PDF + pdftotext -layout), dl/erste_ctrl, dl/si/tab, dl/si/fx (+ fx_slugs.txt), dl/si/list (p331-365, all_links.txt).
Scripts (copied from agent_apr_curves2 and adapted): erste.py (fix: section headers matched only at line start, because the 7 and 8 May commentaries contain
"Stawki IRS" in running text), paptab.py (+ ticker layout of the 15 May edition), fxparse.py, stale.py, xcheck.py (May unstamped editions; intraday clock-stamped
snapshots no longer counted as closes), show.py, build_may.py, schema_check.py.
Renders: render/cmp_0504v0505.png (page 2 of the 4 and 5 May dailies side by side: 01.05 vs 04/05 tables, identical PL IRS), render/cmp_0508v0512.png,
p2_0504/0505/0506 (parse spot-checks: FX, IRS PL/US/EZ, FRA, CDS/spread all match).

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum), ids by publication date: 27-04 169378, 28-04 169382, 29-04 169385, 30-04 169390,
  **(no 1 May daily)**, 04-05 169396, 05-05 169401, 06-05 169402, 07-05 169407, 08-05 169409, 11-05 169416, 12-05 169421, 13-05 169422, 14-05 169425, 15-05 169429,
  18-05 169434. URL pattern https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. All 4 pages, Erste-branded.
- PDF CreationDate (UTC) / URL upload stamp (CEST), all created on the morning of their date: 04 May 06:32:52Z / 08:58:23; 05 May 06:30:50Z / 08:47:34;
  06 May 06:39:50Z / 08:52:31; 07 May 06:24:16Z / 08:39:24; 08 May 06:25:13Z / 08:37:32; 11 May 06:36:25Z / 08:50:13; 12 May 06:42:41Z / 08:53:45;
  13 May 06:36:33Z / 08:57:44; 14 May 06:53:18Z / 09:12:40. None late.
- Headers: 01.05.2026 (4 May daily), dd/mm/yyyy (5-8, 13-14 May), dd.mm.yyyy (11, 12 May). Decimal commas in the 4, 11, 12, 13 May dailies, points in 5-8 and
  14 May. Footnote "Informacje odnoszą się do stawek kupna na rynku międzybankowym na koniec dnia", source LSEG, in every daily.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026): 29 Apr = p.363-365; 30 Apr = 360-363; 1-3 May = 359-360; 4 May = 357-359;
  5 May = 355-357; 6 May = 352-355; 7 May = 349-352; 8-10 May = 347-349; 11 May = 345-347; 12 May = 342-345; 13 May = 340-342; 14 May = 337-340; 15 May = 335-337.
  Pages 331-365 fetched in ascending order; p.353 failed on the first pass (no response) and was refetched with 352/354, so no gap.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. Editions found 28-30 Apr, **1 May (Labour Day, 06:35)**, 4-8, 11-15, 18-22 May.
  2, 3, 9, 10, 16, 17 May return 404 (2 May and 8 May: first try no response, retry 404 / 200).
- FX/FI pieces: two per C (morning + afternoon) for every C in scope; slugs in dl/si/fx/fx_slugs.txt.

## A. Erste tables (main values in curves.json)
- R 6, 7, 8, 11, 12, 13, 14 May: the R-dated daily exists and both its "Rynek stopy procentowej" and FX "Poprzednia sesja" headers equal C. Direct reads.
- IRS 7Y is not in the table (1,2,3,4,5,8,10Y): null and irs_gap_note set for every R.
- Change columns vs day-on-day level differences (stale_out.txt), all within +-1bp for IRS PL/US/EZ, FRA and PL spread on 27.04 -> 28.04 -> 29.04 -> [01.05] and
  04/05 -> 05/05 -> ... -> 15.05, except the two cases below and non-PL spread rows (12 May daily HU 271(-24) vs 275 printed; 13 May daily HU spread "-";
  14 May daily ES 42(+5) vs 43; 4 May daily HU 307(+3) vs 300; 5 May daily IE 20(-13) vs 25; none used). Exact-copy test vs the previous daily: every block "diff"
  (the only copy is the PL IRS block of the 5 May daily, see below). CDS change column always 0 even when the level moves (HU 80 -> 76 etc.), unreliable as before.

### R 2026-05-04 (C 30 Apr): R-dated daily headed 01.05.2026 (Labour Day). Flagged.
No Erste table is headed 30.04 (30 Apr daily = 29.04; no 1 May daily). The 4 May daily (id 169396) heads both tables 01.05.2026. Block by block:
- **PL IRS, FRA, bonds: change columns exactly 0 in every row** = measured against the last Polish session, so the printed levels are the 30 Apr closes
  (level minus change = printed). PL IRS 4.27/4.44/4.47/4.51/4.55/4.68/4.76; FRA 3.86/4.05/4.37/4.57/4.16/4.48. Implied 30 Apr moves vs 29.04: IRS
  +3/+1/-1/-2/-2/-4/-5, FRA -1/+4/+4/+4/+2/+5, bonds 0/-1/-3. Checks: BBG PL 30 Apr +3/-1/-3 (1 May edition, stamped 30.04); PAP WS0428/PS0731/DS1035 +2/-1/-2
  (16:56 -> 16:52); the daily's own text (short yields unchanged, longer -1 to -3bp, "podobnie stopy IRS"); April CPI flash 3.2% on 30 Apr (FRA up).
- **WIBOR and the 10Y-spread column are measured vs 29.04** (O/N 3.47 (-10) vs 3.57; PL 274 (+4) vs 270; FR/ES/IT/PT/IE consistent, HU not) = 30 Apr values.
  PL-Bund 274 vs BBG gap 271 (+3; usual). Kept: pl_bund_10y 274, cds5y 52 (PL CDS 52 in the 29.04, 01.05, 04/05, 05/05 tables; change col unreliable).
- **US IRS block = 1 May session** (US traded): change cols 0/+1/+1/+2/+3/+1/+3 are not the differences from 29.04; the 5 May daily's US change cols match the
  differences from the 01.05 levels. usd_irs = 01.05 level minus change = **DERIVED** 30 Apr: 3.99/3.97/3.94/3.93/3.96/4.13/4.19 (30 Apr moves -4..-9 vs UST
  -8/-7/-6; UST 1 May +1/0/0). eur_irs likewise derived (01.05 changes 0..+1; Bunds closed 1 May): 2.78/2.85/2.85/2.85/2.88/2.99/3.08 (moves -2..-8 vs Bund
  -10/-9/-7). +-1bp.
- **FX block = 1 May holiday trading**: min/max/open/close 4.2406/4.2573/4.2542/4.2436 (close 120 pips below the PAP 30 Apr 16:52 4.2558; the daily's text: EUR/PLN
  briefly below 4.24 over the weekend); only the fixing 4.2589 is a 30 Apr number (NBP 083/A). eurpln_close and eurpln_session = null; fx_header_date = null.
- header_date recorded as printed (01.05.2026). All values are from the R-dated daily (allowed morning table); the 5/6 May dailies were read only to classify blocks.
- Coordinator's mid-run note (content of 169396 = 30 Apr session): confirmed for PL IRS/FRA/bonds/WIBOR/spread/fixing, **not** for the US IRS block (1 May) and the
  FX min/max/open/close (1 May).

### R 2026-05-05 (C 4 May): PL IRS STALE -> irs null. Flagged.
- The 5 May daily (id 169401, headed 04/05) repeats the 01.05 (= 30 Apr) PL IRS levels exactly, all seven change cols 0 (render/cmp_0504v0505.png). 4 May was a UK
  bank holiday; every other block moved: FRA +2/-1/-1/-1/-2/-4 (consistent with 01.05), US IRS +4..+8, EZ +4..+8, bonds 5Y/10Y +5/+4, BBG PL +4/+4/+4, Bund +9/+6/+5.
- Reconstruction attempt: the 6 May daily's PL change cols (+4/+4/+5/+5/+5/+5/+7) give level minus change = exactly the stale levels, i.e. they are measured against
  the stale feed value and span 30 Apr -> 5 May (BBG PL two-day +3/+5/+5; 5 May alone -1/+1/+1). Not a clean reconstruction of 4 May -> **irs all null**.
- Feed check (audit only, documents published long after R, no value used): 26 May daily (headed 25.05, UK Spring bank holiday, PL open): PL IRS 0/+1/+1/0/0/0/0 while
  PL 5Y/10Y bonds -10; next day -5..-9. 1 Sep daily (headed 31.08, UK Summer bank holiday): PL IRS mostly 0 (5Y +4) while bonds +8..+10, FRA +9; next day +10..+15.
  The LSEG PL IRS feed does not (fully) update on UK-only holidays; FRA, bonds, spreads do.
- Kept (fresh): fra, eur_irs, usd_irs, cds5y 52, pl_bund_10y 273 (-1; BBG gap 270), eurpln_close 4.2569, session (fixing 4.2544 = NBP 4 May).
- Bond table (not used): 2Y labelled OK0128 4.67 (+13) although the text says 2Y yields fell slightly; the 6 May daily relabels the rows WS0428/PS0731.
- Agrees with the coordinator's mid-run note (169401 PL IRS stale; FRA/CDS/spread fresh).

### R 2026-05-06 (C 5 May): levels fresh; PL IRS change column is a two-session change (vs the stale 04/05 print). Flagged (Erste note), values used.

### Erste PL-Bund spread vs BBG PL10Y-DE10Y gap
29.04 270/267; 30.04 274/271; 04.05 273/270; 05.05 276/274; 06.05 263/260; **07.05 261/267; 08.05 261/268; 11.05 268/276; 12.05 269/278; 13.05 273/282**.
Erste was 2-3bp above until 6 May and is 6-9bp below from 7 May: the BBG 10Y generic jumped +7 on 7 May (2Y -5, 5Y -2) while the LSEG DS1035 fell 2bp and IRS 10Y -1
(BBG 10Y minus Erste IRS 10Y: 93bp on 6 May, 101-108bp from 7 May; Erste DS1035 minus IRS 10Y stable 94-101bp). See C. The Erste spread itself is unaffected.

### EUR/PLN close, Erste vs PAP last quote
30.04 n/a (01.05 block = 1 May) / 4.2558 (16:52); 04.05 4.2569/4.2555 (14:44); 05.05 4.2452/4.2479 (17:02); 06.05 4.2337/4.2323 (16:55); 07.05 4.2264/4.2265 (16:44);
08.05 4.2332/4.2319 (16:39); 11.05 4.2373/4.2400 (14:03); 12.05 4.2522/4.2490 (16:22); 13.05 4.2465/4.2501 (16:40). Fixings = NBP table A of C (checked 4-13 May).

## B. PAP/Bloomberg tables
- Columns current, 1D, 5D, 1M, 3M, 12M (array order as before; HU 3Y). R editions: 4 May 06:35, 5 May 06:37, 6 May 06:33, 7 May 06:33, 8 May 07:21 (unstamped),
  11 May 06:37, 12 May 06:34 (clock stamps), 13 May 06:41, 14 May 06:33.
- **4 May edition (C 30 Apr)**: HU, TR stamped 30.04 (= C; closed 1 May) -> current col. PL, CZ, IE, IT, PT, ES, DE, FR stamped 01.05 with current = 1D (holiday carry);
  UK stamped 01.05 (gilts traded 1 May); JP/US date-stamped 01.05 (1 May closes, NOT live). These 11 rows: after_C, d1 = 1D col = 30 Apr close (confirmed by the
  1 May edition). The **1 May 06:35 edition** (inside the window) is included as `pap_table_0501_edition`: all EU/CEE/TR rows stamped 30.04 (current col), JP/US
  live (06:33) with d1 = 30 Apr close. The builder's switch rule (>3 after_C rows) picks the alt edition, which gives the same C closes with C-based columns.
- **5 May edition (C 4 May)**: all date-stamped 04.05 except TR 2Y 30.04. JP (Greenery Day) and UK (bank holiday) current = 1 May close carried; US current = 4 May close
  (not live). TR 2Y c_close 37.67 = 30 Apr close (no TR 2Y print 4-5 May). Flagged.
- **6 May edition (C 5 May)**: all stamped 05.05 (TR 2Y 30.04); JP 5 May holiday carry; US current = 5 May close (seen only here). Flagged.
- **7 May edition (C 6 May)**: EU stamped 06.05; JP/US live. JP d1 = 1 May close (JGB closed 4-6 May). Flagged.
- **8 May edition (07:21, C 7 May): no stamp column.** EU/CEE/TR current = 7 May close (11 May edition 1D, 15 May edition 5D). US/JP inferred live 8 May (5D col =
  1 May close; current = 1D in all tenors); d1 = 7 May close, confirmed by the 14 May edition 5D col. Row notes; the flag concerns the 10Y roll.
- **11 May edition (C 8 May)**: CZ 10Y stamped 07.05 (Czech Liberation Day): c_close 4.80 = 7 May close. Flagged.
- **12 May edition (C 11 May): every row clock-stamped later than the 06:34 publication** (PL/EU 17:59, CZ 17:41-17:59, TR 16:32, HU 13:52, JP 09:59, US 18:01) ->
  intraday_on_C, c_close = current col (Jan 13 / Mar 25 precedent, notes only, no flag). All EU/CEE/TR/JP snapshots equal the 11 May close seen later; HU snapshot =
  8 May close = 11 May close (unchanged); **US 18:01 CEST is mid-session NY: 3.92/4.04/4.39 vs the 11 May close 3.95/4.07/4.41 (18 May edition 5D col)**.
- 13, 14 May editions: standard (EU stamped C, JP/US live). R 14: DE unchanged vs 12 May in all three tenors (note only).
- **BBG PL 10Y generic roll (inference)**: 5.60 -> 5.67 on 7 May (+7bp; 2Y -5, 5Y -2) with the Erste/LSEG DS1035 -2 and IRS 10Y -1, and a persistent 9-11bp shift of
  BBG vs Erste from 7 May (see A). PAP's FX/FI "DS1035" row jumped the same day (5.59 -> 5.66) and on 12 May PAP relabels the row DS0436 ("*nowy benchmark") with its
  11 May 14:03 value (5.78, published as DS1035) unchanged. Flagged in R 2026-05-08 (post-R confirmation marked "audit only"); row note on PL in R 8.
- Cross-check (scripts/xcheck.py, editions 28 Apr to 22 May; per-tenor dating; intraday snapshots excluded): for every C in scope all 39 series have 0 conflicts.
  Single observations: TR 2Y 4 May (12 May edition 5D col, = 30 Apr carry), US/JP 5 May (6 May edition current col), US/JP 11 May (18 May edition 5D col).
  build_may.py asserts every non-intraday c_close equals the cross-edition consensus.
- BBG PL generic vs PAP note (2Y/5Y/10Y): 30.04 4.60/5.37/5.75 vs 4.56/5.35/5.74; 04.05 4.64/5.41/5.79 vs 4.58/5.37/5.76 (14:44, early, 6bp on 2Y, flagged);
  05.05 4.63/5.42/5.80 vs 4.60/5.41/5.80; 06.05 4.48/5.20/5.60 vs 4.44/5.19/5.59; 07.05 4.43/5.18/5.67 vs 4.42/5.16/5.66; 08.05 4.46/5.20/5.69 vs 4.43/5.18/5.67;
  11.05 4.52/5.31/5.80 vs 4.50/5.29/5.78 (14:03, early, 2bp, not flagged); 12.05 4.55/5.39/5.88 vs 4.53/5.38/5.86 (DS0436); 13.05 4.62/5.43/5.92 vs 4.59/5.41/5.90.

## C. PAP Dzień na FX/FI (afternoon piece on C)
Quote time of each afternoon piece checked against the previous-session column of the next piece. Only quote tables used for values.

| C | published | quotes | EURPLN | USDPLN | 2Y WS0428 | 5Y PS0731 | 10Y | |
|---|---|---|---|---|---|---|---|---|
| 30.04 | 17:03 | 16:52 | 4.2558 | 3.6301 | 4.56 | 5.35 | 5.74 (DS1035) | 30 Apr 09:10 column marked "*dane z 29.04.2026" (not used) |
| 04.05 | 14:49 | 14:44 | 4.2555 | 3.6348 | 4.58 | 5.37 | 5.76 (DS1035) | early; 5 May 09:40 prev col "pon. 14:44"; flagged |
| 05.05 | 17:16 | 17:02 | 4.2479 | 3.6288 | 4.60 | 5.41 | 5.80 (DS1035) | |
| 06.05 | 17:14 | 16:55 | 4.2323 | 3.5994 | 4.44 | 5.19 | 5.59 (DS1035) | |
| 07.05 | 17:06 | 16:44 | 4.2265 | 3.5906 | 4.42 | 5.16 | 5.66 ("DS1035") | 10Y row apparently DS0436 from 7 May |
| 08.05 | 17:03 | 16:39 | 4.2319 | 3.5944 | 4.43 | 5.18 | 5.67 ("DS1035") | |
| 11.05 | 14:10 | 14:03 | 4.2400 | 3.6032 | 4.50 | 5.29 | 5.78 ("DS1035") | early; 12 May 09:57 prev col "poniedziałek 14:03"; 2bp off BBG, not flagged |
| 12.05 | 16:34 | 16:22 | 4.2490 | 3.6219 | 4.53 | 5.38 | 5.86 (DS0436) | "*nowy benchmark" from the 09:57 piece; bonds.DS1035 null; flagged |
| 13.05 | 16:57 | 16:40 | 4.2501 | 3.6301 | 4.59 | 5.41 | 5.90 (DS0436) | |

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- R 2026-05-05 (C 4 May): PL IRS all null (stale LSEG feed on the UK bank holiday; not reconstructible).
- R 2026-05-04 (C 30 Apr): eurpln_close / eurpln_session null (the 01.05 FX block is the 1 May session; PAP 16:52 4.2558 and NBP fixing 4.2589 are the C-dated alternatives).
- Holiday carries (no C close exists): JP 4, 5, 6 May (= 1 May close); UK 4 May (= 1 May close); TR 2Y 4 and 5 May (= 30 Apr close); CZ 10Y 8 May (= 7 May close).
- C = 4 and 11 May: PAP close only as early quotes (14:44, 14:03). C = 11 May: US row is an intraday snapshot, not the close.
- Nothing else is null; nothing was filled from memory.

## Note for downstream (build_specs_may.py)
- ERSTE overrides suggested: R 2026-05-04 -> "Erste Codziennik of 4 May 2026 (tables headed 01.05.2026, Labour Day: PL IRS/FRA/spread = the 30 Apr closes (zero change
  columns vs 30 Apr); US/EZ IRS = 01.05 levels minus change column, +-1bp)"; R 2026-05-05 -> "PL IRS not available: the 5 May issue repeated the 30 Apr PL IRS levels
  (UK bank holiday, feed not updated); FRA/CDS/spread read directly". The default "table headed C" wording is wrong for these two R.
- R 2026-05-05 irs pillars are all None (not just 7Y): the spec/report must handle an empty IRS curve.
- pl_bund_10y is a direct read in every R (none derived): DERIVED_SPREAD stays empty.
- R 2026-05-04: the builder switches to pap_table_0501_edition (11 after_C rows in the main table); both give identical C closes.
- PL 10Y comparisons across 6/7 May (BBG generic and PAP y10) and PAP y10 across 11/12 May labels mix DS1035 and DS0436. PL 5Y unchanged bond (PS0731) throughout.
- Flag strings start with "Erste", "PAP table" or "PAP close note". Flags per R: 4 May 2, 5 May 3, 6 May 2, 7 May 1, 8 May 1, 11 May 1, 12 May 0, 13 May 1, 14 May 0.
