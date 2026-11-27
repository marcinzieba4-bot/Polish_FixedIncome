# PIT facts 14-28 May 2026 (report dates 15-29 May) - working notes
Output: facts.json (keys mof_ops, new_series, bgk, facts, gpwb, wz_coupons, digest, mpc, data, meta; same schema as the April run) and gpwb_portfolios_2026-05-29.json (format of index_portfolios_2026-04-30.json).
Builder: scripts/build.py. Helpers: scripts/listparse.py (listing -> dl/index_all.json), fetch.sh, h2t.py, rd.py (article body), skrot.py (Skrot sections -> skrot_pl.txt), govlist.py / govpage.py, oh_rows.py (MoF DB -> oh_may.json), pdfmeta.py, pko_ext.py, mil_ext.py, gpwb_parse_may.py (-> gpwb_parsed.json).
Raw downloads: dl/list (listing p300-346), dl/art + dl/txt (925 PAP items 14-28 May), dl/gov (MoF pages, WZ PDF), dl/db (OH.xlsm), dl/gpwb (PDF, calendar, communique pages), dl/res/{pko,mil,erste,db,bps}, dl/web (Scope page).
Windows: R15=14 May, R18=15-17, R19=18, R20=19, R21=20, R22=21, R25=22-24, R26=25, R27=26, R28=27, R29=28 May.
Timestamps: PAP article times are exact. PAP "Skrot" 17:0x/21:xx = upper bound. PDF CreationDate (local, +02) = upper bound. gov.pl and Scope = date only (time written as 00:00). CEST throughout.

## Access tips (27 Nov 2026)
- strefainwestorow listing `https://strefainwestorow.pl/wiadomosci?page=N`.
  - 14 May = p337-340; 15 May = p335-337; 18 May = p332-335; 20 May = p326-330; 22 May = p320-322; 25 May = p317-319; 28 May = p309-312; 29 May starts p309.
  - 16 May and 23 May have no items; weekend Skrot digests on 17 and 24 May.
  - Plain curl works; xargs -P 16 is fine. Re-fetch empty pages once (p330 and p334 failed the first time).
- The feed has no MoF auction headline articles. Offers and results come from the Skrot digests and the FX/FI pieces.
- MoF: `gov.pl/web/finanse/komunikaty-dlug?page=3&size=10`. In-window entries:
  - 15.05: FX account for April; 2025 market transactions.
  - 20.05: WZ coupon notice; CHF mandate.
  - 21.05: CHF pricing. 22.05: CHF details.
  - 29.05: June plan (OUTSIDE). Pages 1-2 hold later notices: only their titles were seen.
  - WZ PDF attachment 3e179d47-...: CreationDate 20 May 11:23, Last-Modified 11:50 CEST.
- MoF DB: same attachment d12c559c... (Last-Modified 25 Nov 2026). Rows for 21 and 27 May match PAP exactly.
  - SD PodażMin = additional-sale offer: 1,622m on 21 May, 1,476m on 27 May.
  - The 13 May rows were read only to reconcile GPWB units and to date OK0129's first issue.
- GPWB: the calendar works with a browser UA plus `Accept: text/html...` and `Accept-Language` headers.
  - PDF: `Portfele_obligacji_2026_05_27.pdf`; the _26/_28 variants return 404.
  - Bond-index communique pages: `komunikaty-i-uchwaly-gpw_czytaj?cmn_id=2843` (27.05). They need a Referer header and the full title parameter.
- PKO: the listing `centrumanaliz.pkobp.pl/aktualnosci?offset=110-140` now spans 6 May-24 Jun (later titles seen but not used). Item pages link the cdn-netpr PDFs.
- Millennium `daily2605DD`: all 11 days exist. The daily's LSEG table gives the previous day's 16:30 close.
- Erste archive ids 169425 (14 May) to 169462 (28 May).
- DB: only wa260519pol and wa260526pol exist, and both were re-saved after the window. BPS: 20260518 and 20260525.
- Blocked: bgk.pl (403); nbp.pl (Imperva challenge page). Scope (scoperatings.com) reachable; its announcement page carries the date only.
- WARNING: the one web search (to date the Scope action) returned snippets about a later Scope review. It also showed an unidentified 22 May instrument downgrade. Neither was used.

## Key findings
- MoF supply in the windows: two sales, no switch, buyback or T-bill. Lines come from the MoF DB, confirmed by PAP the same day.
  - 21 May (plan 7-13bn; offer 6-10bn published 19 May, R20): 10,001.75m sold against 13,283.75m demand (cover 1.33); additional sale 40m (NZ0936).
    - PS0731 4,597m @93.661 (5.433%); DS0436 1,845.1m @95.30 (5.883%); DS1034 894.65m (5.718%).
    - NZ0331 2,030m @94.73; OK0129 480m (4.887%); NZ0936 155m @87.63.
  - 27 May (plan 6-12bn; offer 7-11bn published 25 May, R26): 10,117.205m sold against 12,661.405m demand (cover 1.25); additional sale 140m (OK0129 5m, NZ0936 135m).
    - PS0731 4,092.6m @94.297 (5.287%); DS0436 3,061.9m @96.361 (5.735%); DS1033 1,632.405m @103.221 (5.449%).
    - NZ0331 785.3m; NZ0936 355m; OK0129 190m (4.757%).
  - Financing of 2026 needs: ~51% after 13 May (Millennium 14 May) -> ~54% (MoF, 25 May) -> ">50% of domestic SPW" (Millennium 28 May).
  - The June plan was not out by 28 May (it was due 29 May 15:00).
- New series OK0129 (PL0000119178): zero coupon, matures 25 Jan 2029, issue letter 49/2026 of 4 May.
  - First issued 13 May (pre-window, other agent). GPW admission came 14 May 17:20 (R15); trading from 18 May.
  - In no GPWB index on 29 May.
- MoF other items:
  - Budget deficit after April 89.29bn (15 May): 30.1% of the limit; the 12-month deficit is 273bn against the 272bn limit (PKO).
  - FX on budget accounts EUR 16.5bn at end-April.
  - State Treasury debt 2,088.8bn (+38.1bn m/m).
  - CHF 885m priced 21 May (3Y/7Y/10Y green at MS+50/80/90bp; 0.835% / 1.382% / 1.643%). Mandate 20 May; investor details 22 May.
- WZ coupon for 25 May-25 Nov 2026: 3.96% (19.80 PLN), from WIBOR 6M 3.97/3.96/3.96 on 18-20 May. Published 20 May 11:23 (R21).
  - Applies to WZ1126, WZ1127, WZ0528, WZ1128, WZ1129, WZ1131 and WZ0533.
- GPWB (published 27 May, R28; effective 29 May; holdings as of 26 May). Integrity OK: CreationDate 27 May 11:59, Last-Modified 17:27 CEST, and the HTML communique matches.
  - DS0436 enters TBSP (18 -> 19 bonds) and B5Y.
  - PS0527 leaves B1Y3Y (now 5 bonds), B1Y4Y (8) and B1Y5Y (11).
  - NZ0331 and NZ0928 enter BWZ (9 bonds). This is the first time floaters (NZ) are in BWZ; no methodology notice was seen.
  - TBSP: YTM 4.97%, mod dur 3.68%, value 908.9bn. B1Y3Y: 4.52% / 1.85% / 235.7bn. B1Y4Y: 4.67% / 2.35% / 407.1bn.
  - Units reconcile exactly with sales settled by 26 May (28 Apr, 13 May, 21 May).
- MPC:
  - Wnorowski (Bloomberg, PAP 14 May 06:47): hold at least to July; CPI above 3.5% would not trigger an automatic move.
  - 15 May: the PM refused to countersign the NBP board appointments of Kightley, Kotecki, Litwiniuk and Zarzecki.
  - Glapinski (Bloomberg, 18 May): no commitments; economy resilient.
  - Tyrowicz (Rzeczpospolita, first dated 20 May): 3.75% is too low.
  - April voting record (22 May 14:06): Tyrowicz's +100bp motion was rejected.
  - No minutes in the windows. Next MPC 1-2 June.
- Data, actual vs consensus:
  - Q1 GDP 3.4 vs 3.6. April CPI 3.2 (= flash). Core 3.0 (as expected). HICP 3.4.
  - March C/A -234m vs -1,262.5m.
  - Wages 5.4 vs 6.0; employment -0.9 (as expected); industry 3.1 vs 4.1; construction 4.5 vs 1.2; PPI 1.9 vs -0.1 (March revised to +1.2).
  - Retail 1.3 vs 3.5; M3 11.3 vs ~11.2; unemployment 6.0 (as expected).
  - BWUK -11.3; GUS price expectations 24.7; ESI 100.1; GUS composite 98.5.
- Fiscal and ratings:
  - Fuel package: Motyka (22 May) said the decision comes next week; Domanski (25 May): probably extended. VAT/excise cuts extended to 15 June (Dz.U. 28 May 16:41).
  - Windfall-tax bill on the Q2 list (19 May): 75% of margin above the 2025 level +20%.
  - EC spring forecast (21 May): deficit 6.5% / 6.3% of GDP, debt 64.5% / 68.3%, GDP 3.5%.
  - Scope affirmed A and moved the outlook to Negative (15 May, R18). S&P's Vartapetov (26 May): fiscal position is the key rating risk.
  - SAFE: first 40 contracts worth PLN 100bn by 30 May (28 May). KPO: EUR 7.2bn tranche next week (27 May).
- BGK FPC:
  - 14 May: 835m against 1,102m demand, plus 153m additional.
  - 28 May (offer 26 May): 938.75m against 1,617.75m demand, plus 50m additional.
  - BGK MTN prospectus EUR 35bn (19 May); FPC switches from June and a POLSTR FPC floater in Q3 (25 May).
- Market pricing:
  - ING (14 May): 75bp of hikes within 12M.
  - Erste (18 May): up to 100bp within a year, "exaggerated".
  - Erste (25 May): FRA 9x12 -27bp w/w, one hike priced out. Millennium (25 May): ~2 hikes by year-end.
  - 10Y (DS0436, PAP/BBG): 5.85 (14 May) -> 5.99 (15) -> 6.00 (19) -> 5.93 (20) -> 5.84 (22) -> 5.75 (25) -> 5.74 (27) -> 5.76 (28 May).

## Not used / outside the windows
- 29 May and later items:
  - May CPI flash and the June supply plan (both 29 May).
  - PKO/Erste/Millennium dailies of 29 May.
  - Full Q1 GDP (1 Jun) and MPC 1-2 June.
  - gov.pl list titles (June-November) and PKO listing titles (to 24 Jun), seen while paging.
- Pre-window items, context only:
  - May plan (30 Apr); 13 May sale and its 11 May offer; 8 May T-bill.
  - 5-6 May MPC decision and Glapinski's 6 May remark that hike odds have risen.
  - Litwiniuk and Kotecki remarks of 13 May (recapped 14 May).
  - CPN extension to 31 May (~13 May); BGK 12 May FPC offer.
- Web search: snippets on a later Scope monitoring review and an unidentified 22 May A- instrument downgrade were ignored.

## Gaps
- BGK per-series FPC results were not found (bgk.pl 403). nbp.pl blocked, so there are no NBP primary documents (minutes, voting PDFs).
- Original publication times not found (upper bounds used):
  - Wnorowski (Bloomberg; probably 13 May evening).
  - Tyrowicz (Rzeczpospolita; probably 19 May; kept in R21).
  - Domanski windfall remark (14 May 06:35).
  - Scope (date only, 15 May).
  - BGK 28 May offer (26 May per Millennium; strict reading R28).
- MoF offer/result communiques for 21 and 27 May were not retrieved; PAP and the DB were used. CHF communiques have no time.
- DB weeklies were re-saved after the window (ModDate 25 May / 15 Jun).
- No PAP consensus for core, M3 or unemployment; bank calendars and the MRPiPS estimate were used.
- Industry m/m consensus is inconsistent in PAP: -8.0 in the release text, -0.8 in the weekly table.
- The 28 May Skrot "EC consumer inflation expectations 24.7 from 29.4" repeats the GUS numbers; it is likely a PAP mix-up and is flagged.
- The PAP feed on strefainwestorow is a subset of PAP Biznes. Other MPC remarks, if any, may be missing.
