# Working notes: May 2026 fixings (C = 30 Apr; 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28 May 2026)
All pages fetched 2026-11-27. Later-published pages were used only to read the rows dated C.
Output: fixings.json (same folder). It has the same schema as 2026-04/research/fixings.json, checked by scripts/finalize.py and scripts/verify_schema.py:
- Every record kind (top, by_date[C], wibor, wibor/wibid, euribor, pribor, bubor, nbp_fx, fpc, fpc[traded], fpc[notraded], polstr[d], polstr/*_comp) has exactly the April key set.
- Value types are the same and there are no nulls.
- scripts/schema_paths.py reports 133 vs 140 normalised paths. The 7 missing paths are FPC0332[notraded]: FPC0332 traded on every May C, so this is a data state, not a schema change.
Builder: scripts/build.py (-> core.json + checks.txt, all cross-checks) + scripts/finalize.py (adds notes from scripts/notes_may.py, runs the schema/null check).
Parsers: scripts/parse_gpwb.py, parse_erste.py, parse_erste_mkt.py (IRS/FRA/bond tables), erste_chain.py (-> erste_chain.txt), cat_official.py, cat_scan.py, parse_br.py, load_src.py. Re-check of the April output: scripts/check_april.py. Raw downloads: dl/.

## Sources and how they were read
- WIBOR: https://gpwbenchmark.pl/dane-opoznione (strip `<!-- -->` comments). HTTP 200 on the first try. The rolling table runs 2026-01-02..2026-11-25. Post-window page text (ON/SW discontinued 1 Oct 2026) was ignored.
  Cross-check: Erste Codziennik issued C+1, "Stawki WIBOR" (no 1Y). C -> id:
  30.04->169396 (issue 4 May, headed 01.05!), 04.05->169401, 05->169402, 06->169407, 07->169409, 08->169416, 11->169421, 12->169422, 13->169425, 14->169429,
  15->169434, 18->169438, 19->169442, 20->169443, 21->169446, 22->169448, 25->169452, 26->169454, 27->169462, 28->169465. (169390 = 30 Apr issue, C=29 Apr, used as the chain base.)
  URL: https://www.erste.pl/regulation_file_server/download?id=<id>&lang=pl_PL (-L). Archive: https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum (5.2 MB, regex `data-item-group-id="MM-YYYY" data-item-id=`).
  ON/SW/1M/3M/6M match GPWB on all 20 C. On every issue, value minus change = the previous GPWB fixing. The fixing column = NBP(C) on all 20 C.
  Archive: one issue per Polish business day 4-29 May and none on 1 May. Nothing is missing and no WIBOR table is stale.
  File-server stamps are 08:05-09:16 Warsaw on the issue date (none late). PDF CreationDate is 05:45-07:15 UTC.
  Formats: dd/mm/yyyy with points on 169401, 169402, 169407, 169409, 169425, 169429, 169442, 169446, 169448; dd.mm.yyyy with commas on the rest. All issues use the 4-page Erste Bank Polska layout.
- POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione (latest index date 2026-11-19). All 22 index dates 2026-04-28..2026-05-28 are present; there is no 1 May. The index dates equal the WIBOR fixing dates. 28/29 Apr are identical to the April file.
- EURIBOR: api.statistiken.bundesbank.de/rest/data/BBIG1/D.D0.EUR.MMKT.EURIBOR.{M01,M03,M06,M12}.BID._Z?format=csv&startPeriod=2026-04-20&endPeriod=2026-06-05 ("Stand vom 26.11.2026 13:24"). 1 May = "Kein Wert". 25 May has a value.
- PRIBOR: CNB year.txt?year=2026 (idx 12/14/18). There are no rows on 1 and 8 May (CZ holidays).
- BUBOR: https://www.mnb.hu/letoltes/bubor2.xls sheet "2026" (cols 6/9/15). There are no rows on 1 and 25 May (HU holidays).
- NBP: https://api.nbp.pl/api/exchangerates/tables/A/2026-04-27/2026-05-29/?format=json. Tables 083..102/A cover the C dates; there is no 1 May table.
- Catalyst PRIMARY: gpwcatalyst.pl/pub/CATALYST/statystyki/statystyki_dzienne/catalyst_YYYYMMDD.xls. Month list: POST year=2026&month=05 to /ajaxindex.php?action=BSDailyStatistics&start=list&format=html&ajax2=1&lang=PL.
  It lists 20 sessions, 4-29 May; catalyst_20260501.xls returns 302 -> page-404. May files are still .xls with an unchanged layout and one GPW RR row per FPC bond. There are no block or off-session FPC trades. Header date = C in all files.
  HTTP Last-Modified is on C for all 20 files (16:43-20:15 UTC). The latest postings were 8 May 20:15 UTC (22:15 Warsaw), 30 Apr 18:45 and 6 May 18:03.
  Internal last-saved is on C 16:25-16:41 UTC, except 30 Apr, which reads "Tue Mar 31 16:26:12". This is the same month-end artefact as in April; the content is 30 Apr.
  The April files were re-downloaded for lookback. They reproduce the April output (0 mismatches on 114 bond-days).
- Catalyst cross-check: biznesradar notowania-historyczne pages 1-6. OHLC+vol are identical on all 94 traded bond-days, and none of the 26 no-trade bond-days has a row. Last-trade dates and closes agree.
- Re-check of the April output with today's downloads: WIBOR/WIBID (20), PRIBOR (20), BUBOR (20), EURIBOR (8 in range), NBP (3), POLSTR (23), Catalyst (114 bond-days) are all identical. There are no source revisions.
- GPWB operational communiques (POST ajaxindex.php action=GPWKomunikat): nothing is dated 3 Apr-29 May.
- GPWB Q2 2026 error-impact reports (post-window; read only to confirm that nothing was restated):
  - WIBOR: fixings are never re-set. Two Q2 WIBOR fixings would have differed with corrected inputs (6M -1bp, 1Y -2bp, published minus hypothetical), with no dates given.
  - WIRON: index dates 12 May (0.010-0.020pp) and 18 May (0.001-0.005pp) are listed.
  - POLSTR: no May date is listed.
  - Both reports say the history is not revised. The stored values are the published ones.

## Access
- Plain curl with the default UA worked everywhere (gpwbenchmark, erste -L, bundesbank, cnb, mnb, nbp, gpwcatalyst POST + files, biznesradar at 0.5 s spacing). There were no errors and no retries.

## 1 May (Labour Day) and other holidays (what the data show)
- GPWB did NOT fix on 1 May: there is no WIBOR/WIBID row and no POLSTR/WIRON index date.
  The POLSTR CI accrues 4 days from 30 Apr to 4 May at the 30 Apr rate (implied 3.0660 vs 3.066).
  published_by_convention: 30 Apr -> 4 May.
- On 1 May there was also no NBP table, EURIBOR, PRIBOR, BUBOR or Catalyst session. The only "01.05" anywhere is the header of the Erste issue of 4 May (below).
- Fri 8 May: no PRIBOR (CZ). by_date['2026-05-08'].pribor = 7 May fixing (3.56/3.65/3.75). The src string says so. Everything else fixed.
- Mon 25 May (Whit Monday): GPWB WIBOR and POLSTR fixed, EURIBOR (TARGET open), PRIBOR, NBP 099/A and a Catalyst session all exist.
  BUBOR has no fixing (HU holiday), so by_date['2026-05-25'].bubor.date = 2026-05-22 (6.04/5.99/5.89).
  London and US were closed (Erste 26 May text).
- Mon 4 May was the UK Early May bank holiday. Polish markets were open; see the Erste IRS flag.

## Erste Codziennik flags (C+1 cross-check)
- 169396 (issued 4 May, for C=30 Apr) is MISLABELLED: both market headers say 01.05.2026.
  - WIBOR = 30 Apr fixing, with changes vs 29 Apr (ON 3.47 -10, SW 3.82 +1, 1M 3.76 -2, 3M 3.84 -1, 6M 3.88 -1). The fixing column = NBP 30 Apr (4.2589/3.6460).
  - The FX session row is 1 May offshore trading (EURPLN 4.2406-4.2573, close 4.2436).
  - All PL IRS, FRA and bond changes are 0 because they are measured against 30 Apr. The levels are the 30 Apr close.
    Against 169390 (headed 29.04): IRS +3/+1/-1/-2/-2/-4/-5bp (1L..10L), FRA 3x6..6x12 +2..+5, DS1035 -3, PS0131 -1, OK0128 0. This matches the text ("before the long weekend ... longer 1-3bp lower, likewise IRS").
  - US IRS changes (+0..+3) are 1 May moves; EZ +0/+1.
  - For curves: levels OK for C=30 Apr; the zero changes are NOT 29->30 Apr moves.
- 169401 (issued 5 May, for C=4 May): the PL IRS table is STALE.
  - All 7 tenors (4.27/4.44/4.47/4.51/4.55/4.68/4.76) equal the 30 Apr close with 0 change, and 169402 measures its changes from those same values. 4 May was the UK bank holiday; the text says IRS/FRA were stable on limited activity.
  - WIBOR, the fixing column, the FX session, FRA and bonds are updated.
  - The 2L row is labelled OK0128 at 4.67 (+13), against the text "2Y yields fell slightly on Monday". The next issue switches to WS0428 4.68 (+1) and PS0731 5.50 (+1), so the 2L/5L rows probably carry the new benchmarks under the old labels.
  - NOTE FOR CURVE AGENTS: the Erste PL IRS table of R=5 May is the 30 Apr close.
- 169452 (26 May, C=25 May): IRS 0..+1 and FRA ~0 while bonds fell up to 10bp. The text says London/US investors were absent and FRA/IRS practically unchanged. The quotes are thin, not stale (the values are not identical).
- 169438 (19 May, C=18 May): the bond table (WS0428 -6, DS1035 +8) conflicts with the text ("curve up 1-2bp"); IRS +0..+3 fits the text. The WIBOR and fixing tables are correct.
- Chain check (erste_chain.txt): from issue to issue, IRS/FRA/bond/US/EZ value minus change = previous value within 1bp on all 19 May issues except 169396 (changes vs 30 Apr, above).
- None stale in WIBOR/fixing tables, none missing, and no duplicate issue.

## WIBOR
- RPP held 3.75% on 6 May (Codziennik 7 May, 169407). Glapinski said on 7 May that a hike was more likely than a month earlier (169409).
- Ranges over the 20 C: ON 3.45 (6 May)-3.85 (22 May), SW 3.77-3.82, 1M 3.76-3.82, 3M 3.84-3.86, 6M 3.88-3.97, 1Y 3.91-4.06.
- 18 May step: 6M 3.90 -> 3.97, 1Y 3.93 -> 4.06 (3M -1, SW -4). It is confirmed by Erste 19 May (6M 3.97 +7) and followed the 15 May IRS jump of +11..+16bp (169434).
- WIBOR 6M 15-22 May (the 25 May-25 Nov WZ coupon = average of three fixings before the MoF notice): 15: 3.90, 18: 3.97, 19: 3.96, 20: 3.96, 21: 3.96, 22: 3.95.
  1Y on the same dates: 3.93, 4.06, 4.04, 4.04, 4.04, 4.01.
  Three-day averages: 15/18/19 3.943; 18/19/20 3.963; 19/20/21 3.960; 20/21/22 3.957. The window depends on the MoF notice date, which was not determined here.

## POLSTR publication (d+1 convention on the GPWB calendar, timestamps not verified)
28.04->29.04, 29->30.04, 30.04->04.05 (no GPWB fixing on 1 May), 04->05, 05->06, 06->07, 07->08, 08->11, 11->12, 12->13, 13->14, 14->15, 15->18, 18->19, 19->20, 20->21,
21->22, 22->25 (GPWB open on Whit Monday), 25->26, 26->27, 27->28, 28->29 May (29 May is after the last C).
CI accrual: the multi-day steps are 30.04->04.05 (4d) and 08->11, 15->18, 22->25 (3d). Every step matches POLSTR x days/365 to 0.01.
Month-end dip: index 30 Apr POLSTR 3.066 / WIRON 2.254 (29 Apr 3.327/2.941; 4 May 3.473/3.019). Low WIRON prints, all in the source: 6-8 May 2.884/2.816/2.855, 21 May 2.966, 27 May 2.721, 28 May 2.799. POLSTR high 3.690 (22 May).

## Other fixings
- EURIBOR 12M: 2.848 (30 Apr) -> 2.883 (4 May) -> 2.708 (8 May) -> 2.860 (13 May) -> 2.722 (26 May) -> 2.761 (28 May). 3M: 2.199 -> 2.283 (13 May) -> 2.181 (20 May) -> 2.231. Single source.
- PRIBOR: 3M 3.56-3.57; 6M 3.65-3.70; 1Y 3.77 -> 3.75 (7/8 May) -> 3.86 (19-20 May) -> 3.83.
- BUBOR fell from 13 May: 3M/6M/12M 6.25/6.25/6.31 (30 Apr) -> 6.25/6.23/6.20 (12 May) -> 6.19/6.16/6.12 (13 May) -> 6.08/6.04/5.96 (15 May) -> 6.04/5.99/5.89 (21-22, 26 May) -> 6.00/5.94/5.83 (28 May).
  The cause was not researched; no MNB item appears in the May Codziennik issues.
- NBP: EUR mid is 4.2352 in both 099/A (25 May) and 100/A (26 May). USD (3.6374/3.6394) and CHF (4.6530/4.6388) differ, so this is a coincidence, not a duplicate. EUR 4.2284-4.2589, USD 3.5921-3.6709. CHF is single source.

## Catalyst findings
- Units unchanged. turnover_pln = official value (thous.) x 1000. The biznesradar Obrot ratio is 10.00-10.25 (exactly 10.00 for FPC0630 from 26 May: ex-coupon, accrued 0).
- No-trade days (26 bond-days; official #trades=0; close = reference = last trade close):
  - FPC0231 traded only 30 Apr (31 bonds, 102.50), 7 May (15, 103.00), 13 May (10, 102.20) and 19 May (1,902 in 7 trades, 101.80-102.20).
    No trade 4-6 May (last 30 Apr), 8/11/12 May (last 7 May), 14/15/18 May (last 13 May), 20-28 May (last 19 May): 16 bond-days.
  - FPC0229: 5-6 May (last 4 May, 102.25, 204) and 25 May (last 22 May, 102.05, 999).
  - FPC0733: 5 May (last 4 May, 80.78, 142), 8 May (last 7 May, 81.23, 6), 15 May (last 14 May, 81.24, 2), 19-21 May (last 18 May, 81.24, ONE bond), 28 May (last 27 May, 81.50, 167).
  - FPC0630, FPC0235 and FPC0332 traded every C.
- Thin/suspicious (median vol over traded C: 0229 108, 0630 321, 0231 23, 0733 19, 0235 2,104.5, 0332 84.5):
  - FPC0630: 4 May open/high 93.50 vs close 90.34 (outlier print); 6 May 1 bond (-0.92); 11 May +1.00; 12 May 2 bonds; 18 May -1.00; 28 May 12,456 bonds in 22 trades (~39x median).
  - FPC0229: 20 May range 101.51-103.45 (10 trades, 1,501 bonds); one-trade blocks of 962 (18 May) and 999 (22 May); 1,423 on 30 Apr; 27 May 2 bonds.
  - FPC0733: 27 May open/low 78.22 vs close 81.50 (outlier print); 26 May +0.90 on one 358-bond trade. The close stayed at 81.24 from 12 to 21 May; after 13 May it was held only by 2- and 1-bond prints.
  - FPC0231: 19 May 1,902 bonds (~83x median).
  - FPC0235: 6 May +1.29 to 101.39 on 11,935 bonds (RPP day, IRS -14..-16bp per 169407); heavy volume 30 Apr 15,108 and 14 May 14,720; closed below par 15-19 May (low 99.60 on 18 May).
  - FPC0332: whipsaw on small prints: 4 May -0.89 (50), 5 May +0.65 (4), 7 May -0.64 (6), 8 May +0.72.
- Coupons: FPC0630 (2.125%, coupon 5 Jun) is ex-coupon from 26 May. Accrued is 20.73 on 25 May and 0.00 on 26-29 May, and turnover = vol x price. Prices are clean.
  No other bond has a coupon or record date in the window. Accrued rises monotonically, and FPC0332 stays at 3.72%.
- New lines: NONE for BGK/FWSZ/PFR in May. The BGK (PL00005...) and PFR sets are identical to 30 Apr in every file.
  BGK: FPC0229/0231/0235/0328/0332/0342/0427/0630/0631/0733/1140, BGK1127, FPU1130, FWA0931, IWS0645. PFR: PFR0330/0627/0827/0927, PF10927. No FWSZ-named line exists.
  Treasury: OK0129 (PL0000119178, zero-coupon, matures 2029-01-25) is listed on GPW RR and BS RR from the 18 May file. DS0436 (from 28 Apr) continues. No Treasury line was removed in May.

## Gaps
None. Every field for every C has a value.
Holiday fallbacks are explicit: PRIBOR for C=8 May = the 7 May fixing (in the src string and the notes); BUBOR for C=25 May = 22 May (bubor.date).
Single-source fields: WIBOR 1Y, WIBID, NBP CHF, EURIBOR, PRIBOR, BUBOR, POLSTR/WIRON.
