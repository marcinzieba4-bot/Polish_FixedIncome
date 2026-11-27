# PIT facts 15-29 Apr 2026 (report dates 16-30 Apr) - working notes
Output: facts.json (keys mof_ops, new_series, bgk, facts, gpwb, wz_coupons, digest, mpc, data, meta; same schema as the March run plus digest/mpc/data) and gpwb_portfolios_2026-04-30.json (format of index_portfolios_2026-02-27.json).
Builder: scripts/build.py. Helpers: scripts/h2t.py (strefainwestorow HTML -> text), skrot.py (PAP Skrot sections), govlist.py / govpage.py (gov.pl lists/pages), oh_inspect.py / oh_rows.py (MoF DB -> oh_apr.json), pdfmeta.py, pko_ext.py, mil_ext.py, gpwb_parse.py (-> gpwb_parsed.json).
Raw downloads: dl/list (listing p350-402), dl/art + dl/txt (1,011 PAP items 13-30 Apr), dl/gov (MoF pages + OH.xlsm), dl/gpwb (PDF, headers, calendar), dl/res/{pko,mil,erste,db,bps}, dl/web (date checks only).
Windows: R16=15 Apr, R17=16, R20=17-19, R21=20, R22=21, R23=22, R24=23, R27=24-26, R28=27, R29=28, R30=29 Apr.
Timestamps: PAP article times are exact. PAP "Skrot" 17:0x/21:xx = upper bound. PDF CreationDate (local, +02) = upper bound. gov.pl = date only. CEST throughout.

## Access tips (27 Nov 2026)
- strefainwestorow listing `https://strefainwestorow.pl/wiadomosci?page=N`.
  - 15 Apr = p388-391; 20 Apr = p382-384; 24 Apr = p372-374; 29 Apr = p363-366; 30 Apr = p359-363.
  - Each item appears twice per page (30 items/page). Plain curl works; xargs -P 12 is fine. Re-fetch empty files once.
  - 18 Apr (Sat) has no items.
- MoF debt communiques: `gov.pl/web/finanse/komunikaty-dlug?page=3/4&size=10`.
  - page 4: 7 Apr USD issue, April and Q2 plans (31 Mar).
  - page 3: 15 Apr FX account; May plan dated 30 Apr (OUTSIDE).
  - The list `<a href>` sits inside `div.title` (see govlist.py).
- MoF DB: same attachment id d12c559c... (Last-Modified 25 Nov 2026).
  - Rows for 15/23/28 Apr. TypOperacji AS = auction, SD = additional sale.
  - PodażMin/Max on the first AS row = final offer; on the first SD row = additional-sale offer.
  - All three totals and additional sales match PAP same-day exactly.
  - No T-bill rows: bills are not in this file.
- GPWB: browser UA + Accept headers; file `Portfele_obligacji_2026_04_28.pdf` (the _24/_27/_29/_30 variants return 404). The calendar page gives the 28 Apr announcement / 30 Apr change.
- PKO: `centrumanaliz.pkobp.pl/aktualnosci?offset=155` (14-20 Apr), 150 (21-27 Apr), 145 (28-30 Apr).
  - Each item page holds the cdn-netpr PDF link; use curl -L.
- Millennium: `daily2604DD` works for all days. DB: only wa260421pol (no 13/27 Apr files). BPS: 20260420, 20260427.
- Erste archive: ids 169248 (15 Apr) ... 169385 (29 Apr).
  - The slot uploaded 23 Apr 15:05 (id 169225) is the 13 Apr file, so the 23 Apr daily is missing.
  - From 27 Apr the daily is Erste-branded and 4 pages.
- Blocked: bgk.pl (403), nbp.pl (403).
- WARNING: web searches leaked post-window items: May/July MPC meetings and the July projection, a Litwiniuk interview of 13 May, a Parkiet piece of 14 Jul. None were used. Searches were used only to date candidate articles; no in-window hits.

## Key findings
- MoF April supply: three sale auctions, no switch and no bills in the windows. All rows come from the MoF DB, confirmed same day by PAP.
  - 15 Apr (plan 4-12bn; offer 6-12bn published 13 Apr, pre-window): sold 10,713.35m against 12,130.35m demand (cover 1.13); additional sale 350.5m.
    - PS0731 5,308.65 @95.33 (5.023%); DS1035 2,460 @96.21 (5.514%); WS0428 1,340 @97.10 (4.271%).
    - OK0128 501 (4.267%); NZ0331 985.7 @95.41; NZ0936 118 @89.70.
  - 23 Apr (plan 6-14bn; offer 7-12bn on 21 Apr, R22): sold 8,980.73m against 11,187.53m demand (cover 1.25); additional sale 1,186.2m.
    - New DS0436 1,364.03 @96.75 (5.680%); PS0731 4,618.7 @94.81 (5.147%).
    - OK0128 1,342 (4.368%); NZ0331 1,206; NZ0936 450.
  - 28 Apr (plan 5-13bn; offer 5-10bn): sold 9,004.875m against 11,101.875m demand (cover 1.23); additional sale 111m.
    - PS0731 4,790.875 @94.06 (5.323%); DS0436 1,312 @95.681 (5.828%); DS1034 402 (5.608%); NZ0936 had zero bids.
    - The offer was scheduled for 24 Apr 15:00, but the first dated mention is 27 Apr 06:34, so it is put in R28 (strict).
  - April total 30.35bn including additional sales.
  - Financing of 2026 gross needs: 41% (end-March) -> ~48% (Erste est., 24 Apr) -> ~49% (MoF, 28 Apr).
- New series DS0436 (PL0000119087), 5.25% coupon (MoF DB), matures 25 Apr 2036.
  - Issue letter 37/2026 of 9 Apr. GPW listing on 24 Apr (17:27/18:06); trading from 28 Apr.
  - Outstanding 2,998.23m after 28 Apr. The coupon is not seen in any in-window PAP item.
- MoF other items:
  - Budget deficit after March 69.56bn (15 Apr): revenue 125.18bn, expenditure 194.75bn.
  - FX on budget accounts end-March EUR 13,472.2m (15 Apr).
  - State Treasury debt end-March 2,050.6bn (+13.1bn m/m; FX share 20.1%) (20 Apr).
  - No foreign issue in the windows; the USD issue was on 7 Apr (pre-window). May plan: 30 Apr (outside).
  - No WZ/NZ/PP coupon notices in the windows.
- GPWB (published 28 Apr, R29; effective 30 Apr; as of 27 Apr). Integrity OK: CreationDate 28 Apr 15:38 CEST, Last-Modified 17:47 CEST.
  - PS0731 enters TBSP (17 -> 18 bonds) and B5Y.
  - WS0429 enters B1Y3Y (5 -> 6 bonds) and leaves B3Y5Y. WZ1126 leaves BWZ.
  - TBSP: YTM 4.87%, mod dur 3.71%, value 885.8bn. B1Y3Y: 4.36% / 1.81% / 268.1bn. B1Y4Y: 4.52% / 2.31% / 438.0bn (same 9 bonds).
  - Units reconcile with sales through 23 Apr; DS0436 is in no index.
- MPC:
  - Wnorowski (PAP interview, first dated 17 Apr 07:59): stable rates for longer, decided after the July projection; signal the risk of hikes given loose fiscal policy.
  - Zarzecki (Bloomberg, 23 Apr): rates unchanged for long, any move up.
  - Tyrowicz (23 Apr 18:06): wages are still a risk.
  - March voting record (27 Apr): the cut passed 8:2 (Wnorowski and Tyrowicz against); Tyrowicz's +75bp motion was rejected for the 3rd month.
  - Glapinski: G20 communique only (17 Apr).
  - No April minutes in the windows: the March minutes came out 13 Apr, pre-window. Next MPC 5-6 May.
- Data, actual vs PAP consensus:
  - CPI final March 3.0% (m/m 1.1 vs flash 1.0); core 2.7 vs 2.6; HICP 3.2; Q4 GDP revised to 4.1.
  - Wages 6.6 vs 6.3; employment -0.9 vs -0.8; industry 9.4 vs 4.2; PPI -0.8 vs -0.1; construction 0.4 vs -1.3.
  - Retail 8.7 vs 5.9 (nominal 9.8 vs 6.2); M3 11.5 vs ~10.6; unemployment 6.1.
  - BWUK -14.1; GUS consumer price expectations 29.4 (from 33.3); EC inflation expectations 39.3; ESI 100.2; GUS composite 99.0; new orders -7.3%.
  - GG 2025: deficit 7.3% and debt 59.7%. Notification for 2026: deficit 6.8%, debt 65.1%.
- Fiscal:
  - Fuel package: Motyka (17 Apr) - no phase-out in the coming weeks. Domanski (20 Apr) - ending in early May premature. PKO (22 Apr) - high chance of an extension into May.
  - VAT and excise cuts extended to 15 May (Dz.U. 27 Apr; cost 1-15 May 496m + 350m per OSR, 29 Apr).
  - WZM 2026-30 (28 Apr): deficit 6.8%, GDP 3.6%, CPI 2.5% on pre-war assumptions; shock scenario CPI 3.2%. The windfall tax is to offset CPN; Domanski (29 Apr): >4bn.
  - SAFE: the EC sent the loan agreement on 23 Apr; ~PLN 20bn advance after signing; Tusk wants it outside the deficit (24 Apr). Not signed by 29 Apr.
  - KPO: 30bn on 1 June. The Fiscal Council and MoF clashed on the SRW defence clause (15/21 Apr). No rating action in the windows (S&P 8 May).
- BGK FPC:
  - 16 Apr: 1,061.52m against 1,886.52m demand, plus 206m additional.
  - 29 Apr (offer 27 Apr): 694m against 940m demand.
  - FWSZ 2026 bond plan raised +2.9bn to 76.6bn (27 Apr). BGK to pay a 1.5bn dividend (21 Apr).
- Market pricing:
  - Millennium (20 Apr): ~1 NBP hike priced by year-end.
  - Erste (28 Apr): two 25bp hikes priced for 2026; FRA 9M+ +35bp w/w.
  - Banks almost uniformly expect a hold to year-end. DB: 3.75% through December, CPI to 4.3%. Citi (29 Apr): CPI ~4% by end-2026.
  - 10Y: ~5.53 (14 Apr) -> 5.38 (17 Apr) -> 5.48 (21) -> 5.58-5.62 (23-24) -> 5.68 (27) -> 5.72 (28) -> ~5.76 (29 Apr, PAP 16:56).

## Not used / outside the windows
- 30 Apr items:
  - May supply plan (13/21/27 May, 6-12 / 7-13 / 6-12bn) and Drop's ~184bn end-April liquidity estimate.
  - April CPI flash 3.2% y/y and 0.6% m/m; Dabrowski (Bloomberg) on fading cut chances.
  - March foreign holdings of SPW (-5.0bn to 190.0bn) and SPW secondary turnover.
  - NBP Szybki Monitoring; Eurostat unemployment 3.3%; WIIW forecast; Pekao "fuel crisis base case".
- Pre-window items, context only:
  - April and Q2 plans (31 Mar); 15 Apr offer (13 Apr); T-bill 10 Apr; USD issue 7 Apr.
  - April MPC decision; March minutes (13 Apr); Feb BoP (13 Apr); IMF WEO (14 Apr); Napiorkowska estimate (14 Apr).
  - Kotecki (Parkiet, 14 Apr 06:00); excise extension to 30 Apr (week of 6-10 Apr).
- PKO items listed at offset 140 and later (May); any S&P review outcome; later MPC decisions or projections leaked by web search.

## Gaps
- Original times of the Wnorowski (PAP Biznes) and Zarzecki (Bloomberg) interviews were not found. Wnorowski may have run on 16 Apr evening; it is kept in R20 (conservative).
- The MoF 24 Apr communique (28 Apr offer) was not retrieved. If a dated 24 Apr copy exists, the offer can move to R27.
- DS0436 coupon: from the MoF DB only.
- BGK per-series results, and the 29 Apr additional sale, were not found (bgk.pl 403). nbp.pl blocked.
- The PAP feed on strefainwestorow is a subset, so other MPC remarks may be missing (no Kotecki/Litwiniuk/Janczyk/Dabrowski/Kropiwnicki/Maslowska items in the windows).
- The Erste 23 Apr daily is missing.
- DB weekly 21 Apr was re-saved 22 Apr 13:16 (flagged).
- ING Think, Pekao and Credit Agricole were not fetched directly; their views come via PAP only.
- No PAP consensus for HICP, ESI, GUS business climate or BWUK; core and M3 consensus come from the Millennium/DB calendars.
- The source for the GG debt year is inconsistent: one PAP text says 65.1% in 2027, while Erste and the Skrot say 2026. Kept as 2026 per the notification.
