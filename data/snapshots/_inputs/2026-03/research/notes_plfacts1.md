# PIT facts 27 Feb - 15 Mar 2026 (report dates 2-16 Mar) - working notes
Output: facts.json (same folder; keys mof_ops, new_series, bgk, facts, gpwb, meta - same schema as the Feb runs). Builder: scripts/build.py.
Raw downloads: dl/list (strefainwestorow p438-472), dl/art + dl/txt (801 PAP items 27 Feb-15 Mar), dl/gov (MoF March plan page + PDF, MoF Fitch page, XYZ Fitch article), dl/gpwb (index calendar), dl/res/{pko,mil,erste,db,bps}.
Windows: R2Mar=27 Feb-1 Mar, R3=2, R4=3, R5=4, R6=5, R9=6-8, R10=9, R11=10, R12=11, R13=12, R16=13-15 Mar.
Timestamps: PAP article times exact; PAP "Skrot" 17:01/21:xx = upper bound; PDF CreationDate UTC +1h; Erste = upload time in URL; ING Think = date only.

## Access tips (27 Nov 2026)
- strefainwestorow listing: 27 Feb = p468-470, 6 Mar = p456-458, 13 Mar = p444-446 (about 2.3 pages/day). All 801 slugs fetched (xargs -P 12 is fine).
- MoF debt communiques: gov.pl/web/finanse/komunikaty-dlug?page=4&size=10 holds 27 Feb (March plan); next item is 16 Mar. March plan PDF = attachment 1cbd6f02.
- Fitch: fitchratings.com not reachable. Use the MoF English page gov.pl/web/finance/fitch-rating-agency-affirmed-polands-credit-rating11 (dated 27.02.2026) and xyz.pl/?p=175287 (27.02.2026 23:42).
- PKO Dziennik: centrumanaliz.pkobp.pl/aktualnosci?offset=180-190 covers 27 Feb-13 Mar. cdn-netpr now 302-redirects, so use curl -L.
- Millennium dailyYYMMDD works. Erste: the archive page from the Feb run already lists ids 169122-169159.
- DB: only wa260303pol and wa260310pol (folder 2026/03); both were re-saved 19 Mar. BPS: 20260302, 20260309.
- Credit Agricole: static files return 403 to HEAD requests; brute-force id probing was denied, so MAKROmapa was not retrieved.
- ING Think snaps (4 and 5 Mar) via WebFetch.
- Blocked: bgk.pl, fitchratings.com.
- WARNING: web searches leaked post-window items (later Fitch/S&P actions; PS0731 coupon and size from cbonds). None were used.

## Key findings
- Fitch, Fri 27 Feb: affirmed A-/F1, Outlook Negative.
  - Timing: pre-announced for after 22:00. The XYZ/PAP report is stamped 23:42, the upper bound. The exact Fitch time was not found.
  - Numbers via MoF: GG deficit 7.0% (2025), 6.5% (2026), 6.2% (2027). Debt ~59% rising to ~70% of GDP by 2027. GDP 3.6% (2026, revised up), 2.9% (2027).
  - Calendar (DB 3 Mar): Moody's 20 Mar, S&P 8 May.
- MoF March plan (27 Feb; PDF created 08:41 CET; first PAP mention 15:06):
  - Sale auctions 18 and 25 Mar, each PLN 7-13bn: OK0128, NZ0331, PS0731 (new), DS1035, NZ0936 (new), plus possible IZ.
  - Switch on 11 Mar buying back OK0426, DS0726, PS1026, WZ1126, OK0127. No T-bills. No WZ line.
  - Retail offer unchanged.
- Switch auction cancelled on 9 Mar (Czarnecki: SPW volatility). No MoF auction, offer, T-bill or foreign issue fell in the windows.
  - Budget accounts: ~170bn estimate (27 Feb); 171.6bn actual (6 Mar).
  - Domanski (13 Mar): supply will be adjusted to market conditions.
  - Non-residents +13.7bn to 188.0bn in January (12.5% share).
  - State Treasury debt at end-January: 1,998.3bn.
- New series PS0731 and NZ0936: ISIN, coupon and exact maturity were NOT published in the windows.
- MPC, 4 Mar: cut of 25bp, released by 14:58.
  - New rates: ref 3.75, lombard 4.25, deposit 3.25, rediscount 3.80, discount 3.85; effective 5 Mar.
  - PAP consensus: a cut, with a risk of a hold.
  - Statement (16:00): the adjustment was justified by inflation and its prospects. Risks now include commodity prices "w kontekscie napiec geopolitycznych".
  - Projection bands (16:16): CPI 1.6-2.9 / 1.1-3.7 / 0.9-4.0; GDP 3.1-4.7 / 2.0-3.8 / 1.8-4.1.
  - Full report (6 Mar 09:00): CPI 2.3 / 2.4 / 2.3; core 2.5 / 2.4 / 2.4; GDP 3.9 / 2.9 / 2.9. It excludes the war.
- Glapinski, 5 Mar:
  - If things calm within two months (4-8 weeks), "wracamy do starego scenariusza... bedzie jeszcze obnizka".
  - On the real rate, members range from 1pp to 1.5pp; he sits in the 1pp camp.
  - "Rada nie zapowiada... zadnych kolejnych decyzji" and "ciemne chmury nad naszym optymizmem".
  - 11 Mar: NBP is ready for active gold management (~197bn unrealised gain), but the government showed zero interest.
- MPC members after the meeting:
  - Wnorowski (6 Mar 07:16, Bloomberg): forget cuts while the war lasts; 3.25-3.5% is now much less likely.
  - Kotecki: room is "much smaller" (6 Mar); "raczej koniec" (11 Mar); "not April, probably not May; maybe no more cuts" (12 Mar).
  - Zarzecki: be cautious (6 Mar); wait-and-see, market hike pricing premature (10 Mar).
  - Janczyk (12 Mar): rates are adequate for several quarters.
  - Tyrowicz (12 Mar): inflation is too high to ignore shocks.
  - Maslowska (13 Mar): a hike needs a durable upward inflation trend of more than 1-2 quarters.
- Data:
  - PMI Feb 47.1 vs consensus 49.4 (PKO quotes 49.6).
  - Q4 GDP 4.0% confirmed: consumption 4.2, investment 4.7.
  - Unemployment Feb 6.1% (MRPiPS flash).
  - CPI Feb 2.1% y/y / 0.3% m/m, in line with consensus. Jan revised to 2.1 / 0.7 from 2.2 / 0.6.
  - There was no Feb flash. Core CPI falls on 16 Mar (outside); only the MoF estimate is available.
  - Reserves EUR 259.2bn. Trade surplus Jan EUR 0.7bn.
- Market: the 10Y moved from ~4.93% (27 Feb) to ~5.60% (6 Mar), peaked above 5.90% intraday on 9 Mar, then ~5.62% (12 Mar close).
  - FRA priced 2 hikes (9 and 12 Mar). Curve +80-90bp since 2 Mar.
  - BGK FX activity reported on 2 Mar.
- Fiscal and BGK:
  - SAFE law to the President (27 Feb). Veto announced 12 Mar evening. Cabinet "plan B" (13 Mar): SAFE loan via BGK for FWSZ.
  - Presidential PFIO bill (10 Mar).
  - BGK FPC auction of 12 Mar cancelled (first dated mention: Santander 11 Mar 08:51). BGK: ~60% of the 2026 FPC plan is already raised.
- GPWB: no new communique. The 25 Feb change took effect 27 Feb (window R2). Next: announcement 27 Mar, change 31 Mar.

## Not used / outside the windows (do not use)
- 18/25 Mar auction offers and results; MoF FX communique (16 Mar); NZ/WZ/PP0931 coupon communiques (19-20 Mar); Q2 plan; April supply.
- Moody's review (~20 Mar); NBP Jan BoP and core CPI (16 Mar).
- Any later rating actions or PS0731/NZ0936 terms seen in web search results.
