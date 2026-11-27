# Working notes: Mar 2026 curves, part 2 (R 17-20, 23-27, 30, 31 Mar; C 16-20, 23-27, 30 Mar)
Output: curves.json in this folder, keyed by R. Same schema as 2026-02/research/curves_pap_2.json (checked programmatically: identical top-level, irs/fra/irs_src/
eurpln_session, pap_table, row and pap_close key sets and key order). Six PAP columns per row, live/after_C/intraday_on_C flags, d1, c_close; optional keys
`flags`, `irs_gap_note`, row `note` and `pap_close.note`. The only content-level difference: from C = 26 Mar the PAP 2Y benchmark is WS0428, so
`pap_close.bonds.OK0128` is null and `y2` carries the WS0428 yield (explained in each `pap_close.note`; the bonds key set was kept unchanged).
Raw parses: erste_raw_all.json (12 Mar to 2 Apr dailies), paptab_raw.json (PAP tables 12 Mar to 9 Apr), fx_raw.json, xcheck_obs.json.
Downloads: dl/erste (archiwum.html, ids.tsv, PDF + pdftotext -layout), dl/si (PAP tables), dl/si/fx (FX/FI notes), dl/si/list (listing pages 408-450).
Scripts: scripts/ (erste.py, paptab.py, h2t.py, stale.py reused unchanged from the Feb run; fxparse2.py = fxparse.py made label-driven for the WS0428* row and
"b.d." cells; xcheck_mar.py; build_mar.py). Renders: render/ (page 2 of the 13, 16, 17, 24 and 31 Mar dailies; spr_13v16.png = stale-column comparison).

## Sources / access (all fetched 27 Nov 2026, HTTP 200 unless noted)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum), ids by publication date: 12-03 169158, 13-03 169159, 16-03 169162, 17-03 169167,
  18-03 169170, 19-03 169171, 20-03 169173, 23-03 169175, 24-03 169179, 25-03 169180, 26-03 169183, 27-03 169184, 30-03 169186, 31-03 169188, 01-04 169190, 02-04 169191.
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. All PDFs 3 pages; they still carry Santander branding.
- Formats: header dd.mm.yyyy except the 24 Mar daily (23/03/2026). Decimal points in the 16-19 and 24 Mar dailies, decimal commas in the 20, 23, 25-31 Mar and 1 Apr
  dailies; the parser handles both. Spot-checked against the rendered page 2 of the 24 Mar (point) and 31 Mar (comma) dailies: IRS PL/US/EZ, FRA, CDS/spread, FX all match.
- strefainwestorow listing (https://strefainwestorow.pl/wiadomosci?page=N, 27 Nov 2026): 13 Mar = p.444-446; 16 Mar = 441-444; 17 Mar = 439-441; 18 Mar = 436-439;
  19 Mar = 433-436; 20 Mar = 431-433; 23 Mar = 428-431; 24 Mar = 425-428; 25 Mar = 423-425; 26 Mar = 417-423; 27 Mar = 415-417; 30 Mar = 413-415; 31 Mar = 410-413.
  Pages 412-450 were fetched in ascending order (no gaps possible from new items); p.429-431 were refetched to close a possible gap at 429/430 (one non-FX item recovered).
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. One edition per weekday. 14, 15, 21, 22, 28, 29 Mar and 3 (Good Friday), 4, 5 Apr
  returned 404: no weekend editions. The first fetch of 21 Mar had a proxy connection reset; the retry returned 404.

## A. Erste tables (main values in curves.json)
- Every R-dated daily exists; its "Rynek stopy procentowej" header and its FX "Poprzednia sesja" header both equal C. No fallback was needed.
- PDF CreationDate (UTC) / URL upload stamp (local time; CEST from 29 Mar). All created on the morning of R:
  17 Mar 07:33:01Z / 08:50:19; 18 Mar 07:54:39Z / 09:13:12; 19 Mar 09:16:25Z / 10:19:21 (late); 20 Mar 08:12:30Z / 09:19:12; 23 Mar 06:53:38Z / 07:57:44;
  24 Mar 07:23:18Z / 08:46:33; 25 Mar 07:41:13Z / 08:41:51; 26 Mar 07:26:17Z / 08:30:33; 27 Mar 07:46:33Z / 09:02:32; 30 Mar 06:27:02Z / 08:57:26; 31 Mar 06:05:49Z / 09:19:04.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set.
- The IRS (PL/US/EZ) and FRA change columns match the day-on-day level differences within ±1bp for every table from 12.03 through 01.04.
- No IRS, FRA, FX or CDS/spread table of any R in this set is an exact copy of the previous day's (stale.py: every block "diff").

### Staleness and suspicious items
- **16 Mar daily (headed 13.03; R = 16 Mar, NOT in this set): STALE 10Y-spread column.** Exact copy of the 13 Mar daily's 12/03 column for all 7 countries,
  change columns included: PL 273(+19), FR 67(+3), HU 425(+3), ES 50(+4), IT 79(+8), PT 46(+4), IE 31(0). The CDS column did change (PL 57 -> 58, HU 97 -> 98,
  IT 12 -> 14). Confirmed side by side on the rendered page 2 (render/spr_13v16.png). Relevant to whoever builds R = 16 Mar.
- **17 Mar daily (headed 16.03): spread change column inconsistent** with the level differences vs the stale 16 Mar daily (PL -6 vs +2, HU -7 vs +11, FR -2 vs 0,
  ES -2 vs -1, IT -3 vs -1). Consistent with the change being measured against the true 13.03 values. The 16.03 levels are not a copy. Flagged in R 2026-03-17.
- The CDS change column is always 0 even when the level moves (e.g. HU 98 -> 104 on 16.03, PL 60 -> 63 on 23.03). Unreliable, as in earlier runs.
- Erste PL-Bund spread vs the PAP/BBG PL10Y-DE10Y gap: 13.03 273 (stale) / 277; 16.03 275/273; 17.03 267/264; 18.03 273/271; 19.03 281/278; 20.03 280/278;
  23.03 270/269; 24.03 281/277; 25.03 277/274; 26.03 271/269; 27.03 279/276; 30.03 293/289. Erste is 1-4bp above, as usual. The +15 on 30.03 is matched by BBG (+13).
- EUR/PLN close, Erste vs PAP last quote: 16.03 4.2735/4.2655 (14:50); 17.03 4.2585/4.2596 (17:47); 18.03 4.2690/4.2713 (16:22); 19.03 4.2762/4.2797 (14:50);
  20.03 4.2765/4.2759 (14:04); 23.03 4.2605/4.2641 (14:50); 24.03 4.2785/4.2756 (17:00); 25.03 4.2736/4.2747 (16:32); 26.03 4.2745/4.2726 (16:50);
  27.03 4.2849/4.2843 (16:45); 30.03 4.2891/4.2916 (16:55). OK; the larger gaps are the early PAP pieces.
- Session fixing printed with 3 decimals, stored as printed: EURPLN 26.03 "4,271".
- The Erste bond table (not requested, not used) still labels the 2Y benchmark OK0128 (2L) through 30.03.

## B. PAP/Bloomberg tables
- Columns are current, 1D, 5D, 1M, 3M, 12M (array order as before). R editions: 17 Mar (06:36), 18 (06:32), 19 (06:41), 20 (07:05), 23 (06:34), 24 (06:34),
  25 (06:35), 26 (06:32), 27 (07:31), 30 (06:34), 31 (06:45).
- 17, 18, 19, 24, 26, 30, 31 Mar: all EU/CEE/TR rows stamped exactly C; JP/US carry morning-of-R clock stamps (live), so d1 is used for them.
- **20 Mar edition (07:05): no stamp column.** EU/CEE/TR current = 19 Mar close (23 Mar edition 1D, 27 Mar edition 5D; TR also = 23 Mar edition current, stamped 19.03).
  **US and JP are not live**: US current 3.79/3.88/4.25 = 19 Mar close (26 Mar edition 5D col) and its 1D/5D equal the 19 Mar edition's 1D/5D; JP current
  1.27/1.68/2.28 = 19 Mar close (23 Mar edition 1D, 26 Mar edition 5D) because 20 Mar was a Japanese holiday. So the current column is used for all 13 rows. Flagged.
- **23 Mar edition:** EU/CEE stamped 20.03; **TR stamped 19.03.2026** (no Turkish session on 20 Mar; the 24 Mar edition's TR 1D is also the 19 Mar value), so TR c_close
  is the 19 Mar close. **JP: C = 20 Mar was a Japanese holiday (Vernal Equinox Day)**, so the JP d1 = 19 Mar close. Both flagged in R 2026-03-23.
- **25 Mar edition (06:35): intraday snapshot on C.** Every row carries a clock stamp later than the publication time, i.e. the evening of 24 Mar:
  PL 17:29/17:49, HU 14:04, CZ 17:56, TR 15:32, IE/IT/PT/ES/DE/FR/UK 17:59, JP 08:59 (16:59 JST), US 18:00 (13:00 EDT). Same pattern as the 13 Jan edition (H1 run),
  handled the same way: intraday_on_C=true, c_close = current column, d1 = null. Later editions confirm that the EU/CEE/TR/JP values equal the 24 Mar close
  (26 Mar edition 1D, 31 Mar edition 5D). **US is mid-session, not the close**: the 24 Mar US close seen later (31 Mar edition 5D) is 3.89/3.99/4.36 vs 3.91/4.02/4.38
  in the snapshot. Not put in `flags` (as in H1; the row note says it); the downstream spec uses the US Treasury curve for US anyway.
- **27 Mar edition (07:31): no stamp column.** EU/CEE/TR current = 26 Mar close (30 Mar edition 1D; no 5D confirmation possible: no 3 Apr edition, and the 6 Apr
  edition is stamped 03.04). JP (07:31 CET = 15:31 JST, after the JGB close) and US are inferred live: their 5D column is the 20 Mar value, so they refer to 27 Mar;
  d1 = 26 Mar close, confirmed by the 2 Apr edition 5D column.
- The rule about editions between C and R was **not triggered**: no weekend editions, no R edition has EU rows stamped later than C; after_C is false everywhere.
- Full cross-check (scripts/xcheck_mar.py, editions 12 Mar to 9 Apr): for every C, all 39 country/tenor series are seen at least twice, with 0 conflicts, except
  - C = 24 Mar US (3 series): the 25 Mar 18:00 intraday snapshot vs the later close (expected, see above).
  - C = 27 Mar US/JP: one observation only (30 Mar edition 1D), because there is no 3 Apr edition and the 6 Apr 5D column is 30 Mar.
  - C = 26 Mar and 30 Mar EU/CEE/TR: two observations (current + next 1D).
- Unchanged rows (all three tenors equal the previous close): JP on 17 Mar (3 observations), noted in the R 18 row. TR and JP on 20 Mar are holiday carry-overs (flagged).
- BBG PL generic vs PAP note (2Y/5Y/10Y): 16.03 4.38/5.13/5.68 vs 4.32/5.06/5.63 (PAP 14:50); 17.03 4.29/5.01/5.55 vs 4.26/4.99/5.54; 18.03 4.35/5.11/5.65 vs 4.32/5.09/5.63;
  19.03 4.45/5.21/5.74 vs 4.45/5.24/5.77 (PAP 14:50); 20.03 4.61/5.35/5.82 vs 4.48/5.21/5.73 (PAP 14:04, 9-14bp below); 23.03 4.48/5.27/5.70 vs 4.62/5.39/5.79
  (PAP 14:50, 9-14bp above); 24.03 4.60/5.39/5.80 vs 4.56/5.36/5.79; 25.03 4.47/5.29/5.70 vs 4.45/5.27/5.69; 26.03 4.55/5.29/5.76 vs 4.53 (WS0428)/5.25/5.75;
  27.03 4.55/5.32/5.85 vs 4.53/5.31/5.85; 30.03 4.62/5.37/5.93 vs 4.60/5.35/5.93.
  Early PAP pieces that are >=5bp off the BBG close are flagged (R 17, 23, 24).

## C. PAP Dzień na FX/FI (afternoon piece on C)
Two FX/FI pieces per C (morning + afternoon), except 23 Mar (three: 09:29, a 12:23 flash with no quote table, 14:58). Each afternoon quote time was checked against the
previous-day column of the next morning's piece. Only the quote tables were used; no commentary.

| C | published | quotes | EURPLN | USDPLN | 2Y | PS0131 | DS1035 | |
|---|---|---|---|---|---|---|---|---|
| 16.03 | 15:03 | 14:50 | 4.2655 | 3.7120 | 4.32 (OK0128) | 5.06 | 5.63 | early; no later piece |
| 17.03 | 18:02 | 17:47 | 4.2596 | 3.6938 | 4.26 | 4.99 | 5.54 | |
| 18.03 | 16:34 | 16:22 | 4.2713 | 3.7085 | 4.32 | 5.09 | 5.63 | |
| 19.03 | 15:02 | 14:50 | 4.2797 | 3.7237 | 4.45 | 5.24 | 5.77 | early; no later piece |
| 20.03 | 14:16 | 14:04 | 4.2759 | 3.6985 | 4.48 | 5.21 | 5.73 | early; no later piece |
| 23.03 | 14:58 | 14:50 | 4.2641 | 3.6759 | 4.62 | 5.39 | 5.79 | early; printed "14.50" |
| 24.03 | 17:22 | 17:00 | 4.2756 | 3.6926 | 4.56 | 5.36 | 5.79 | |
| 25.03 | 16:48 | 16:32 | 4.2747 | 3.6926 | 4.45 (OK0128) | 5.27 | 5.69 | last OK0128 day |
| 26.03 | 17:07 | 16:50 | 4.2726 | 3.7021 | 4.53 (WS0428*) | 5.25 | 5.75 | "* - zmiana benchmarku" |
| 27.03 | 17:02 | 16:45 | 4.2843 | 3.7143 | 4.53 (WS0428) | 5.31 | 5.85 | |
| 30.03 | 17:08 | 16:55 | 4.2916 | 3.7423 | 4.60 (WS0428) | 5.35 | 5.93 | |
URLs are in curves.json under pap_close.url. Note: the 31 Mar afternoon piece (17:10) has no body text on the site (not needed here; C = 31 Mar is out of scope).

## Gaps
- IRS 7Y: null for all R (not published by Erste).
- JP close for C = 20 Mar and TR close for C = 20 Mar do not exist (holidays); their c_close is the 19 Mar close, as labelled and flagged.
- US for C = 24 Mar (R 25): only an intraday 18:00 CET value exists in the R edition; kept as the intraday_on_C value per the H1 convention.
- No other nulls. Nothing was filled from memory.

## Note for downstream
- The February spec builder (2026-02/tools/build_specs_feb.py) sets pl_bund_10y = None whenever `flags` is non-empty. In this set only the R 17 flag concerns the Erste
  CDS/spread table; the flags in R 20, 23, 24 and 27 are about the PAP table or the PAP close note (each flag string starts with "Erste", "PAP table" or "PAP close note").
