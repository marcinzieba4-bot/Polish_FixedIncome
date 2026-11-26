# Working notes: Feb 2026 curves, part 1 (R 2-13 Feb; C 30 Jan, 2-6 Feb, 9-12 Feb)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-01-H2/research/curves_pap.json: six PAP columns per row,
live/after_C/intraday_on_C flags, d1 and c_close. The optional keys are also the same: `flags`, `irs_gap_note` and `pap_close.note`.
I checked the key sets and key order programmatically against the January file, and they are identical.
Raw parses: erste_raw_all.json (30 Jan to 16 Feb dailies), paptab_raw.json (PAP tables 30 Jan to 23 Feb), fx_raw.json and xcheck_obs.json.
Downloads: dl/erste (archive HTML, PDFs and pdftotext -layout output), dl/si (PAP tables), dl/si/fx (FX/FI notes) and dl/si/list (listing pages 480, 489-512).
Scripts: scripts/. erste.py, paptab.py, fxparse.py and h2t.py are reused unchanged from the January run. erste_check.py, xcheck_feb.py and build_feb.py are new.
Renders: render/ (page 2 of the 10, 11 and 13 Feb dailies).

## Sources / access (fetched 26 Nov 2026)
- Erste archive (https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum) has one daily per business day. The ids are:
  30-01 169016, 02-02 169019, 03-02 169025, 04-02 169027, 05-02 169031, 06-02 169034, 09-02 169043, 10-02 169046,
  11-02 169047, 12-02 169049, 13-02 169051, 16-02 169057. All downloads returned HTTP 200 (PDF, 3 pages).
  The 30 Jan and 2 Feb PDFs are byte-identical to the January run's copies.
- strefainwestorow listing (26 Nov 2026): 30 Jan = p.508-510; 2 Feb = 506-508; 3 Feb = 505-506; 4 Feb = 503-505; 5 Feb = 501-503;
  6 Feb = 499-501; 9 Feb = 497-498; 10 Feb = 495-497; 11 Feb = 493-495; 12 Feb = 491-493; 13 Feb = 489-491.
- PAP table: one edition per weekday. 31 Jan, 1, 7, 8, 14 and 15 Feb returned 404, so there are no weekend editions.

## A. Erste tables (main values in curves.json)
- In every case the R-dated daily exists, and both its "Rynek stopy procentowej" (IRS/FRA/CDS) header and its FX "Poprzednia sesja" header equal C. No fallback was needed.
  The header format switches from dd.mm.yyyy (to 05.02) to dd/mm/yyyy (06/02-12/02) and back (13.02).
- PDF CreationDate (UTC) / URL upload stamp (CET):
  02 Feb 07:16:14Z / 08:37:17; 03 Feb 07:12:17Z / 08:31:52; 04 Feb 07:27:44Z / 08:43:35; 05 Feb 07:16:44Z / 09:03:10; 06 Feb 07:19:05Z / 08:32:01;
  09 Feb 08:42:16Z / 09:44:46; 10 Feb 07:29:00Z / 08:43:33; 11 Feb 07:43:00Z / 10:31:49 (late upload); 12 Feb 07:19:57Z / 08:30:56; 13 Feb 07:26:07Z / 08:39:26.
  Every daily was created on the morning of R.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set.
- The IRS (PL/US/EZ), FRA and spread change columns match the day-on-day level differences within ±1bp for all 11 transitions (30.01 through 13.02).
- I spot-checked the 13 Feb daily (headed 12/02) against the rendered page: the IRS, FX and bond values and the PL|US|EZ column order all match the parse.

### Staleness and suspicious items
- **11 Feb daily (headed 10/02): STALE 10Y-spread column.** It is an exact copy of the 10 Feb daily's 09/02 column for all 7 countries, change columns included:
  PL 227(+1), FR 60(0), HU 376(0), ES 37(-1), IT 62(-1), PT 36(-1), IE 9(+1). As a result, 5 of the 7 change columns disagree with the level differences, which are all 0.
  I confirmed this side by side on the rendered page 2 (render/spr_10v11.png). The CDS column did change (PT 8 -> 9, DE 3 -> 4), so only the spread column is stale. Flagged.
- **13 Feb daily (headed 12/02): PL spread 227(0) is suspicious.** PL 10Y fell about 7bp on 12 Feb (PAP note DS1035 5.04 -> 4.97; Erste's own bond table DS1035 -7; Bloomberg 5.04 -> 4.97)
  while DE10Y fell 1bp, yet the spread is unchanged. Erste minus the Bloomberg gap is +8bp here against a usual +1 to +3. The table is not a copy (HU 378 -> 384, FR 60 -> 59, IE 11 -> 10). Flagged, value kept.
- CDS column identical to the previous daily for all 8 countries in the 6 Feb (05.02), 9 Feb (06.02) and 12 Feb (11/02) dailies. The spread column changed each time.
  The 04.02, 05.02 and 06.02 CDS columns are the same three tables in a row. Mild flags, the same treatment as 16 Jan in the January run.
  As before, the CDS change column is always 0 even when the level moves, so it is unreliable.
- Erste PL-Bund spread vs the PAP/Bloomberg PL10Y-DE10Y gap: 30.01 227/225; 02.02 226/223; 03.02 221/218; 04.02 224/222; 05.02 226/224; 06.02 226/225;
  09.02 227/225; 10.02 227 (stale)/224; 11.02 227/225; 12.02 227/219 (!); 13.02 (16 Feb daily) 222/218.
- The Erste bond table (not requested) is still erratic. For example, OK0128 3.64(+9) on 03.02 against PAP 3.52, and 3.44(-17) on 10.02. pdftotext drops DS1035 in the 9, 10 and 12 Feb dailies (parsed as "2.0"). Not used.
- EUR/PLN close, Erste vs PAP last quote: 30.01 4.2101/4.2082 (16:45); 02.02 4.2220/- (no PM piece); 03.02 4.2223/4.2219 (16:48); 04.02 4.2158/4.2132 (16:42);
  05.02 4.2186/4.2209 (17:06); 06.02 4.2167/4.2168 (16:42); 09.02 4.2089/- (no PM piece); 10.02 4.2164/4.2171 (16:32); 11.02 4.2164/4.2166 (16:21); 12.02 4.2143/4.2131 (16:47). OK.

## B. PAP/Bloomberg tables
- Columns are current, 1D, 5D, 1M, 3M, 12M (array order as before). All R editions were published 06:34-06:41, except 13 Feb (07:30).
- 2, 3, 4, 5, 6, 9, 10 and 12 Feb editions: all EU/CEE/TR rows are stamped exactly C, and JP/US carry morning-of-R clock stamps (live), so d1 is used.
  Some stamps are lists, e.g. ['06:37:00','06:38:00'], as in January.
- **11 Feb edition (06:35):** every row, including US and JP, is stamped 10.02.2026 (= C). This is the same pattern as the 12 Jan edition in the H1 run, on a Japanese holiday (11 Feb).
  The US/JP current column is the 10 Feb close (US 3.45/3.70/4.14, JP 1.31/1.71/2.24), confirmed by the 17 Feb edition 5D column. So those rows are not live and the current column is used. Flagged.
- **13 Feb edition (07:30): no stamp column.** EU/CEE/TR current = C close, confirmed for all rows by the 16 Feb edition 1D column and the 19 Feb edition 5D column.
  US current 3.47/3.67/4.11 is not the 13 Feb close (3.41/3.60/4.05 per the 16 Feb edition), so it is inferred live and d1 = 3.46/3.66/4.10 (confirmed by the 19 Feb 5D column).
  JP current is a 13 Feb (15:30 JST) value, so it is after C and d1 = 1.31/1.71/2.24 (confirmed by the 19 Feb 5D column).
- **C = 11 Feb (R 12): Japanese holiday.** The JP d1 1.31/1.71/2.24 is the 10 Feb close, the last JP close on or before C. Flagged in the row note and in `flags`.
- **C = 4 Feb (R 5):** the US/JP d1 is seen only once (5 Feb edition 1D), because the 11 Feb edition is stamped 10.02, which moves its 5D column to 3 Feb. EU rows have 3 observations.
- The rule about editions between C and R was **not triggered**: there are no weekend editions, and no R edition has EU rows stamped after C. after_C is false everywhere and intraday_on_C is false everywhere.
- Full cross-check (scripts/xcheck_feb.py, editions 30 Jan to 23 Feb): for every C, all 39 country/tenor series match with 0 conflicts. All have 2 or more observations, except the 6 US/JP series on 4 Feb.
- No US holiday falls on any C. Presidents' Day is 16 Feb; that edition has US at 05:24 with current = 1D, as on MLK Day, but it is outside this set.
- Bloomberg PL generic vs PAP note (2Y/5Y/10Y): 30.01 3.55/4.40/5.09 vs 3.53/4.39/5.08; 03.02 3.55/4.37/5.07 vs 3.52/4.35/5.06; 04.02 3.55/4.38/5.08 vs 3.53/4.36/5.07;
  05.02 3.53/4.39/5.08 vs 3.50/4.36/5.07; 06.02 3.52/4.39/5.09 vs 3.49/4.37/5.08; 10.02 3.46/4.33/5.05 vs 3.44/4.32/5.04; 11.02 3.48/4.32/5.04 vs 3.45/4.31/5.04;
  12.02 3.47/4.28/4.97 vs 3.43/4.26/4.97. The 2Y generic is again 2-4bp above OK0128, and 5Y/10Y are within 0-3bp.

## C. PAP Dzień na FX/FI (afternoon piece on C)
| C | published | quotes | EURPLN | USDPLN | OK0128 | PS0131 | DS1035 |
|---|---|---|---|---|---|---|---|
| 30.01 | 17:00 | 16:45 | 4.2082 | 3.5368 | 3.53 | 4.39 | 5.08 |
| 02.02 | - | - | null | null | null | null | null | **GAP**: only a 09:28 morning piece (09:20 quotes 4.2117; 3.53/4.38/5.08, not used)
| 03.02 | 17:02 | 16:48 | 4.2219 | 3.5746 | 3.52 | 4.35 | 5.06 |
| 04.02 | 16:55 | 16:42 | 4.2132 | 3.5691 | 3.53 | 4.36 | 5.07 | (RPP decision day)
| 05.02 | 17:22 | 17:06 | 4.2209 | 3.5809 | 3.50 | 4.36 | 5.07 | (ECB day)
| 06.02 | 16:55 | 16:42 | 4.2168 | 3.5694 | 3.49 | 4.37 | 5.08 |
| 09.02 | - | - | null | null | null | null | null | **GAP**: only a 09:52 morning piece (09:40 quotes 4.2132; 3.52/4.39/5.10, not used)
| 10.02 | 16:48 | 16:32 | 4.2171 | 3.5441 | 3.44 | 4.32 | 5.04 |
| 11.02 | 16:46 | 16:21 | 4.2166 | 3.5549 | 3.45 | 4.31 | 5.04 | (quotes 16:21)
| 12.02 | 17:02 | 16:47 | 4.2131 | 3.5447 | 3.43 | 4.26 | 4.97 |
- The gaps are confirmed by PAP's own comparison tables in the next-morning pieces. The 3 Feb table columns are "wt. 09:40 / pon. 09:20 / piątek 16:45",
  and the 10 Feb columns are "wtorek 09:05 / pon. 09:40 / piątek 16:42". No 2 Feb or 9 Feb afternoon quote exists.
  The next-morning commentary was not used, per the rule.
- Every other C has exactly two FX/FI pieces, one in the morning and one in the afternoon. The URLs are in curves.json under pap_close.url. Only the quote tables were used; the commentary was not.
