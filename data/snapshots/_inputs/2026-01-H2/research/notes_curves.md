# Working notes: Jan 2026 curves, part 2 (R 16-30 Jan; C 15, 16, 19-23, 26-29 Jan)
Output: curves.json in this folder, keyed by R. The schema is the same as 2026-01-H1/research/curves_pap.json (six PAP columns per row,
live/after_C/intraday_on_C flags, d1, c_close). Optional keys used, as in that file: `flags`, `irs_gap_note`, `pap_close.note`.
Raw parses: erste_raw_all.json (includes the 15 Jan daily from the earlier run, used for the staleness check), paptab_raw.json, fx_raw.json, xcheck_obs.json.
Downloads: dl/erste (PDF + pdftotext -layout), dl/si (PAP tables 15 Jan to 6 Feb), dl/si/fx (FX/FI notes), dl/si/list (listing pages 505-531). Scripts: scripts/.

## Sources / access
- Erste archive ids (archive HTML from the earlier run, 26 Nov 2026): 16-01 168993, 19-01 168995, 20-01 168998, 21-01 169000, 22-01 169002,
  23-01 169004, 26-01 169007, 27-01 169011, 28-01 169014, 29-01 169015, 30-01 169016, 02-02 169019.
  URL pattern: https://www.erste.pl/regulation_file_server/time<YYYYMMDDhhmmss>/download?id=<id>&lang=pl_PL. All returned HTTP 200.
- Format change: from the 26 Jan daily on, the tables use decimal commas, so the parser was patched. Values were checked against the rendered page 2 of the 21 and 28 Jan dailies.
- The PDFs still carry the Santander Bank Polska logo. The publisher label is kept as in the earlier file.
- strefainwestorow listing (26 Nov 2026): 15 Jan = p.528-531; 16 Jan = 527-528; 19 Jan = 525-526; 20 Jan = 523-525; 21 Jan = 521-523;
  22 Jan = 519-521; 23 Jan = 517-519; 26 Jan = 515-517; 27 Jan = 513-515; 28 Jan = 511-513; 29 Jan = 510-511; 30 Jan = 507-510.
- PAP table URL /wiadomosci/YYYYMMDD/rentownosci-obligacji-wybranych-panstw-tabela. One edition per weekday. 17, 18, 24, 25 and 31 Jan returned 404, so there are no weekend editions.

## A. Erste tables (main values in curves.json)
- In every case the R-dated daily exists, and its IRS/FRA table and its FX "Poprzednia sesja" table are both headed C. No fallback was needed.
- PDF CreationDate (UTC) / URL upload stamp (CET):
  16 Jan 08:01:05Z / 09:02:13; 19 Jan 08:00:43Z / 09:13:12; 20 Jan 07:46:19Z / 09:01:49; 21 Jan 08:16:49Z / 09:17:11; 22 Jan 07:42:14Z / 09:00:40;
  23 Jan 07:50:48Z / 08:59:53; 26 Jan 07:38:10Z / 08:40:58; 27 Jan 07:07:40Z / 08:17:28; 28 Jan 07:02:35Z / 08:05:55; 29 Jan 08:28:25Z / 09:31:02; 30 Jan 07:23:39Z / 08:27:18.
  All were created on the morning of R.
- IRS 7Y is not in the table (tenors 1,2,3,4,5,8,10), so it is null and `irs_gap_note` is set.
- The IRS and FRA change columns match the day-on-day level differences within ±1bp for all 11 tables (checked from 14.01 through 30.01).

### Staleness and suspicious items
- **21 Jan daily (headed 20.01): STALE CDS/10Y-spread table.** It is an exact copy of the 20 Jan daily's 19.01 table for all 8 countries, change columns included
  (PL 59(0)/232(+3), HU 107/400(+1), FR 14/66(-2)...). This was confirmed on the rendered PDF, and it is the same failure mode as the 14 Jan daily in the earlier run. Flagged.
- 16 Jan daily (headed 15/01): the CDS column for all 8 countries is identical to the 15 Jan daily (14/01). The spread column changed, so this is not a whole-table copy. Mild flag.
- 26 Jan daily (headed 23.01): the spread change column is inconsistent with the level differences (PL -2 vs -4, FR -4 vs -7, HU -8 vs -12). Flagged as a note.
- 28 Jan daily (headed 27.01): every PL IRS change is 0, and the levels equal 26.01 except 4Y (+1). It is not a copy, because FRA, US/EZ IRS, bonds and spreads moved.
  PAP/BBG PL bonds were also flat on 27 Jan (2Y 3.58, 10Y 5.11 both days). Noted, not treated as stale.
- The CDS change column is always 0, even when the level changes. It is unreliable, as already noted in the earlier run.
- The Erste PL-Bund spread is 2-5bp wider than the PAP/BBG PL10Y-DE10Y gap: 15.01 230 vs 227; 16.01 230/227; 19.01 232/230; 20.01 232(stale)/229;
  21.01 229/226; 22.01 229/224; 23.01 225/222; 26.01 226/224; 27.01 227/223; 28.01 227/223; 29.01 228/224. The benchmarks differ.
- The Erste bond table (not requested) is erratic against PAP and should not be used. For example, 15.01 OK0128 3.61 vs PAP 3.68; 16.01 3.72 (+11) vs 3.61; 20.01 3.57 (-13) vs 3.54.
- EUR/PLN close, Erste vs PAP last quote: 15.01 4.2131/4.2131 (17:21); 16.01 4.2211/4.2229 (16:30); 19.01 4.2232/4.2238 (14:26); 20.01 4.2245/4.2278 (16:50);
  21.01 4.2182/4.2178; 22.01 4.1976/4.2027 (15:55, PLN rallied late; Erste min 4.1955); 23.01 4.2080/4.2058; 26.01 4.2043/4.2076 (14:44);
  27.01 4.1966/4.1971; 28.01 4.2050/4.2049; 29.01 4.2118/4.2125. OK.
  Cross-check: the 23 Jan PAP note says EUR/PLN was "+0.2% to 4.2058", which implies a base of about 4.1976, matching the Erste 22.01 close.
- The 23.01 session fixing is printed with 3 decimals ("4,205"). It is stored as 4.205.

## B. PAP/Bloomberg tables
- Columns are current, 1D, 5D, 1M, 3M, 12M. The 5D column is 5 business days before the stamp date for EU rows, and 5 business days before the edition date for live US/JP rows. This was verified.
- Editions with per-row stamps: 19 Jan (06:38), 20 (06:46), 21 (06:35), 22 (06:35), 26 (06:41), 27 (06:41), 28 (06:34) and 29 (06:36).
  In each of them all EU/CEE/TR rows are stamped exactly C, and JP/US are live on the morning of R, so d1 is used for them.
- Editions with no stamp column: 16 Jan (07:29), 23 Jan (05:48, no "Obligacje" header, so the parser was patched) and 30 Jan (07:26).
  For EU/CEE/TR rows, the current column equals the next edition's 1D (19 Jan / 26 Jan / 2 Feb) and the 5D column 5 business days later, so it is the C close.
  US/JP are inferred live and d1 is used:
  - 16 Jan and 30 Jan: the current column differs from the next edition's 1D.
  - 23 Jan US: current equals 1D.
  - 23 Jan JP (05:48 CET = 13:48 JST, BoJ day): current equals the 23 Jan close, which is still after C.
- The rule about editions between C and R was **not triggered**. No R edition has European rows stamped later than C, and there are no weekend editions.
- Full cross-check (scripts/xcheck.py): for every C, all 39 country/tenor series appear 2-3 times across editions (current, 1D, 5D), with 0 conflicts. This used editions from 15 Jan to 6 Feb.
- Special cases:
  - **C = 19 Jan (R 20): US holiday (MLK Day).** The US d1 is the 16 Jan close (3.59/3.82/4.22). Flagged. In the 19 Jan edition (05:24), US current equals 1D for the same reason.
  - C = 28 Jan (FOMC day): the US close of 3.57/3.83/4.24 is identical to 27 Jan. This is confirmed by the 4 Feb edition 5D column, so it is genuine, not stale.
  - C = 27 Jan: FR/ES/PT are unchanged vs 26 Jan in all three tenors. Confirmed three times. Noted in the rows.
- The Bloomberg PL 2Y generic is 1-3bp above OK0128 in the PAP note, as before. Other gaps are within 0-4bp.
  BBG vs PAP 2Y/5Y/10Y: 15.01 3.70/4.50/5.09 vs 3.68/4.49/5.08; 16.01 3.64/4.48/5.11 vs 3.61/4.44/5.07 (5Y/10Y -4bp; PAP 16:30);
  19.01 3.62/4.49/5.14 vs 3.60/4.47/5.12 (PAP 14:26); 20.01 3.57/4.48/5.15 vs 3.54/4.46/5.15; 21.01 3.55/4.46/5.14 vs 3.53/4.44/5.13;
  22.01 3.58/4.45/5.13 vs 3.55/4.43/5.12; 23.01 3.60/4.46/5.13 vs 3.58/4.44/5.12; 26.01 3.58/4.45/5.11 vs 3.55/4.43/5.10 (PAP 14:44);
  27.01 3.58/4.44/5.11 vs 3.56/4.41/5.10; 28.01 3.55/4.42/5.09 vs 3.54/4.40/5.08; 29.01 3.57/4.40/5.08 vs 3.55/4.39/5.07.

## C. PAP Dzień na FX/FI (afternoon piece on C)
Every C has exactly two "Dzień na FX/FI" pieces, one in the morning and one in the afternoon. No other FX/FI-type pieces were found in the listing.

| C | published | quotes | EURPLN | USDPLN | OK0128 | PS0131 | DS1035 |
|---|---|---|---|---|---|---|---|
| 15.01 | 17:33 | 17:21 | 4.2131 | 3.6301 | 3.68 | 4.49 | 5.08 |
| 16.01 | 17:01 | 16:30 | 4.2229 | 3.6396 | 3.61 | 4.44 | 5.07 |
| 19.01 | 14:39 | 14:26 | 4.2238 | 3.6318 | 3.60 | 4.47 | 5.12 | (early; no later piece)
| 20.01 | 17:02 | 16:50 | 4.2278 | 3.6034 | 3.54 | 4.46 | 5.15 |
| 21.01 | 16:59 | 16:48 | 4.2178 | 3.6009 | 3.53 | 4.44 | 5.13 |
| 22.01 | 16:11 | 15:55 | 4.2027 | 3.5848 | 3.55 | 4.43 | 5.12 | (before close)
| 23.01 | 16:53 | 16:39 | 4.2058 | 3.5795 | 3.58 | 4.44 | 5.12 |
| 26.01 | 14:57 | 14:44 | 4.2076 | 3.5516 | 3.55 | 4.43 | 5.10 | (early; no later piece)
| 27.01 | 16:47 | 16:34 | 4.1971 | 3.5109 | 3.56 | 4.41 | 5.10 |
| 28.01 | 17:04 | 16:51 | 4.2049 | 3.5214 | 3.54 | 4.40 | 5.08 | (MF auction day; FOMC at 20:00, after these quotes)
| 29.01 | 18:06 | 17:47 | 4.2125 | 3.5261 | 3.55 | 4.39 | 5.07 |
The URLs are in curves.json under pap_close.url. Only the quote tables were used; the commentary was not.
