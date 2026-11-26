# PIT facts 15-29 Jan 2026 (report dates 16-30 Jan) - working notes
Output: facts.json (same folder; keys mof_ops, new_series, bgk, facts, gpwb, meta). Builder: scripts/build.py (+ scripts/gpwb_parse.py).
Raw downloads: dl/ (list, art, txt = PAP via strefainwestorow; gov; gpwb; res/{pko,mil,erste,ca,db,bps}).
Windows: R16=15 Jan, R19=16-18, R20=19, R21=20, R22=21, R23=22, R26=23-25, R27=26, R28=27, R29=28, R30=29 Jan.
Timestamps: PAP article times exact; PAP "Skrot wiadomosci" 17:0x/21:0x = upper bounds; PDF CreationDate UTC +1h; Erste = upload time in URL.

## Access tips (26 Nov 2026)
- strefainwestorow listing: 15 Jan = p528-531, 22 Jan = p519-521, 29 Jan = p510-511 (about 2 pages/day). 633 slugs 15-29 Jan, 284 macro ones fetched.
- MoF PL debt communiques list: https://www.gov.pl/web/finanse/komunikaty-dlug?page=5&size=10 (Jan 2026). Only 15 Jan (FX funds Dec) in window; Feb plan 30 Jan, JPY 2 Feb (outside).
- MoF db (Obligacje_Hurtowe.xlsm, T-bill xls) copied from the earlier run (downloaded 26 Nov). Used only 22/28 Jan + 16 Jan AS rows; totals match PAP exactly.
- PKO Dziennik: list offsets 210-220 at centrumanaliz.pkobp.pl/aktualnosci?offset=N; cdn-netpr PDFs need curl -L (302).
- Erste archive (5 MB page) lists ids 168985-169015 for 15-29 Jan.
- Credit Agricole: makromapa-19012026_34737.pdf found; 26 Jan id not found in 34738-34900.
- DB: wa260119pol, wa260126pol OK. BPS: komentarz_tygodnia/20260126.pdf OK (20260119 404).
- GPWB: communique search is ajaxindex.php (operational notices only); the index calendar (gpwbenchmark.pl/kalendarium-indeksow) gives 28 Jan = announcement, 30 Jan = change.
- Blocked: bgk.pl (403), bosbank.pl.

## Key findings
- 16 Jan T-bill: 36W PL0000006201 (mat 29 Sep 2026) sold 3,800.1m vs 5,845m, 3.645%. The db has an additional sale of 170m, but no dated source confirms it, so it is not used.
- 22 Jan auction (offer on 20 Jan at the 15:00 slot: 6 series, 8-12bn vs plan 8-13bn): sold 12,011.9 vs 17,149.0 (cover 1.43); additional sale 1,754.5.
  OK0128 300/780 @93.381 (3.488%); WZ0930 916/3306 @97.741; PS0131 4453.9/5389 @100.491 (4.386%); NZ0331 2150/2701 @95.311; DS0432 1319/1535 @84.750 (4.611%); DS1035 2873/3438 @99.150 (5.107%).
  Additional sale: WZ0930 587.5, NZ0331 1037, DS1035 130.
- 28 Jan auction (offer 26 Jan, 8-12bn vs plan 7-12bn): sold 12,001.0 vs 21,370.0 (cover 1.78); additional sale 2,112.0.
  OK0128 250/1373 @93.343 (3.529%); WZ0930 469/1189 @97.833; PS0131 2890/4310 @100.461 (4.392%); NZ0331 4161/8582 @95.446; DS1034 1029/1624 @100.161 (4.970%); DS1035 3202/4292 @99.250 (5.093%).
  Additional sale: PS0131 4, NZ0331 771.5, DS1034 59, DS1035 1277.5.
- No new MoF series. DS0432 and DS1034 were re-openings. No switch or buyback. Financing: 28% (26 Jan), 30% (29 Jan). Q1 status: 41.6bn sold in 3 of 8 auctions vs the 75-100bn Q1 plan.
- SEC USD 10bn shelf filed 20 Jan (PAP 21 Jan). MoF said a USD issue is possible. EUR bond ISINs were confirmed by GPW on 21 Jan. Budget FX account was EUR 9.336bn at end-Dec. State Treasury debt was 1,952bn at end-Dec.
- GPWB, 30 Jan change (published 28 Jan, holdings as of 27 Jan):
  - B1Y3Y: OK0127 leaves; 5 bonds; mod dur 1.81%; YTM 3.47%.
  - B1Y4Y: PS0130 enters and OK0127 leaves; 9 bonds; mod dur 2.56%; YTM 3.76%.
  - TBSP: no change in constituents (18 bonds); mod dur 3.76%; YTM 4.11%; value 868,981m.
  - The PDF was regenerated 2 Feb 2026, but its units reconcile exactly with MoF settlements up to 26 Jan.
- Glapinski (15 Jan): terminal rate 3.5%; does not exclude February or March (or even April); 25bp steps; dovish board; CPI within the target band through 2026; gold to 700t.
- MPC comments:
  - Kotecki (16 Jan): Feb cut.
  - Wnorowski (16 Jan): March more logical; rate below 3.5% possible.
  - Tyrowicz (19 Jan): no room to cut.
  - Zarzecki (21 Jan): wait for the March projection; Feb premature.
  - Duda (23 Jan): Feb or March both likely.
  - Sobon, NBP board (28 Jan): room for cuts, decided month by month.
  - Dec minutes (16 Jan); Dec vote 9-1 with Tyrowicz against; her 150bp hike motion was rejected (27 Jan).
- Data, actual vs consensus:
  - CPI 2.4 vs 2.4; core 2.7 vs 2.8.
  - Wages 8.6 vs 6.9; employment -0.7 vs -0.7.
  - Industrial output 7.3 vs 2.9; PPI -2.5 vs -2.2; construction 4.5 vs -0.5.
  - Retail 5.3 vs 5.6 (PAP); unemployment 5.7 vs 5.7.
  - Consumer confidence (BWUK) -9.6; ESI 103.2; M3 10.4.
- Bank calls shifted: PKO moved to a Feb cut after the 15 Jan conference. After the strong 22 Jan data, most (ING, Erste, Millennium, BPS, Noble, BNP TFI) see a Feb hold and a March cut. Terminal-rate views: Pekao and ING 3.25%; DB, Erste, BNP and Millennium 3.50%; CA sees March as the last cut.
- Fiscal: President signed the 2026 budget and sent it to the Constitutional Tribunal for follow-up review (19 Jan). Eurostat: debt 58.1% of GDP in Q3, s.a. deficit 5.8% of GDP. SAFE: first 8 country plans approved by the EC without Poland (16 Jan); >80% of funds go to domestic industry (27 Jan). KPO inflows EUR 9.5bn. BGK sold 1bn of FWA0931 on 29 Jan (terms unknown).

## Not used / outside the window (do not use)
- February supply plan (30 Jan), 2025 GDP flash (30 Jan), JPY issue (2 Feb), PKO/Erste dailies of 30 Jan and later.
- Later rows in the MoF db (Feb-Nov 2026) were seen but not used.
- PKO macro outlook PDF (19 Jan) was not read.
