# PIT facts 16-30 Mar 2026 (report dates 17-31 Mar) - working notes
Output: facts.json (same folder). Keys: mof_ops, new_series, bgk, facts, gpwb, wz_coupons, meta. Same schema as the 2026-02 run (facts_poland_2.json), plus wz_coupons.
Builder: scripts/build3.py (runs build2.py -> build1.py). Also scripts/gpwb_parse.py, sumpdf.py, gov.py, fetch.sh, h2t.py, dump.py, skrot.py.
Raw downloads: dl/list, dl/list2 (PAP listing), dl/art, dl/txt (PAP via strefainwestorow), dl/pre*, dl/gov (+db), dl/gpwb, dl/res/{pko,mil,erste,db,bps}.
Windows: R17=16 Mar, R18=17, R19=18, R20=19, R23=20-22, R24=23, R25=24, R26=25, R27=26, R30=27-29, R31=30 Mar.
Timestamps: PAP article times are exact. PAP "Skrot" 17:0x/21:xx times are upper bounds. PDF CreationDate is local time and an upper bound. Erste = the upload time in the URL. gov.pl gives a date only.
DST: CEST starts 29 Mar.

## Access tips (27 Nov 2026)
- strefainwestorow listing pages: 16 Mar = p441-444, 20 Mar = p431-433, 26 Mar = p417-423, 30 Mar = p413-415.
  - Fetch pages in ascending order to avoid gaps. 913 slugs; 196 articles fetched.
  - There is no PAP Skrot for Fri 20 Mar in the feed.
- MoF debt communiques: https://www.gov.pl/web/finanse/komunikaty-dlug?page=4&size=10 holds the WZ, NZ and PP0931 coupon notices, the Feb FX account, and the March, April and Q2 plans.
- MoF DB (OH.xlsm) was copied from the Feb run (downloaded 26 Nov) and already contains the March rows. Only the 18 and 25 Mar rows are used. Their totals and series lists match PAP same-day exactly.
- GPWB: use a browser UA plus Accept headers. The file exists only for _2026_03_27; the 24-26, 30 and 31 variants return 404.
- PKO PDFs: cdn-netpr now redirects, so use curl -L. Listing offsets 165-175 cover 16-30 Mar.
- Erste archive works. Millennium daily2603DD works.
- DB: only wa260316pol and wa260323pol exist.
- BPS: 20260316 and 20260330 exist; there is no 23 Mar file.
- Blocked: bgk.pl (403). No Wayback captures of the GPWB file.
- Web search leaked later rating outcomes (after Sep 2026). These were ignored and are NOT used.

## Key findings
- MoF March calendar was disrupted by the Iran war (from 28 Feb) and an SPW sell-off. The 10Y rose ~110bp in March.
  - The 11 Mar switch was cancelled (pre-window).
  - The 18 Mar SALE was converted into a SWITCH (announced 16 Mar).
  - The 25 Mar sale offer was cut to 3-8bn, against 7-13bn in the plan.
- 18 Mar switch:
  - Sold 9,476.229m against 13,705.2m demand.
    - OK0128 1,790.8 @92.570 (4.257%); NZ0928 728.5 @98.70; NZ0331 2,154.8 @95.573.
    - PS0731 3,928.7 @95.323 (5.011%, NEW); NZ0936 873.4 @89.855 (NEW).
  - Bought back 9,170.660m.
    - OK0426: 0 @99.654. DS0726: 1,834.4 @99.672. PS1026: 954.0 @98.153.
    - WZ1126: 3,117.2 @100.482. OK0127: 3,265.2 @97.139.
- 25 Mar sale: 7,290.35m sold against 8,523.6m demand (cover 1.17). Additional sale 401.833m (offer 1,649). Financing reached ~41%.
  - OK0128 872 @92.255 (4.496%); NZ0928 925 @98.60; NZ0331 1,589 @95.45.
  - PS0731 2,019.3 @93.631 (5.399%); DS1035 1,610.05 @94.71 (5.725%); NZ0936 275 @89.91.
- New series:
  - PS0731 (PL0000118998): 4.00% coupon, matures 25 Jul 2031.
  - NZ0936 (PL0000118980): POLSTR floater, matures 25 Sep 2036.
  - Both were first issued 18 Mar (settled 20 Mar). GPW Catalyst communiques at 18 Mar 19:13.
- No WZ was offered in the windows. No T-bills. No foreign issue, mandate or prefinancing in the windows.
- April and Q2 supply plans were published 31 Mar 15:00, OUTSIDE the windows, and are not used.
- WZ coupons:
  - WZ0330 and WZ0930: 3.86% for 25 Mar-25 Sep 2026 (PLN 19.30). Based on WIBOR6M 3.85/3.86/3.87 (18/19/20 Mar). Published 20 Mar (PDF 11:52), so R23.
  - PP0931: 3.85%, published 19 Mar.
  - NZ compounded rate for 25.09.25-25.03.26: 3.98239% (19.75 PLN), published 19 Mar.
- GPWB (calendar date 27 Mar, effective 31 Mar, as of 26 Mar):
  - PS1026 leaves TBSP (18 -> 17). There are no other entries or exits.
  - B1Y3Y: YTM 3.37 -> 4.30%, mod dur 1.64%.
  - B1Y4Y: YTM 3.65 -> 4.64%, mod dur 2.37%.
  - TBSP: YTM 4.00 -> 4.99%, mod dur 3.75%, value 861.4bn.
  - Units reconcile with trades through 25 Mar.
  - CAUTION: the served file was re-generated on 30 Mar 11:22 CEST and is titled "..._3_...". Last-Modified is 30 Mar 13:49 CEST. The original is not archived.
- Moody's (Fri 20 Mar, evening, after 22:00): no action; A2 with a negative outlook. 2026 GDP forecast raised to 3.7%. First PAP report came 22 Mar 20:02.
- Data, actual vs PAP consensus:
  - Core CPI: Jan 2.7, Feb 2.5 (expected 2.6-2.7). Headline Jan and Feb 2.1.
  - Wages 6.1 vs 6.6; employment -0.8 vs -0.8. Industry 1.5 vs 1.3. PPI -2.3 vs -2.4. Construction -13.7 vs -7.7.
  - Retail 5.0 vs 6.1 (nominal 4.3 vs 5.5). Unemployment 6.1. M3 10.6 (~10.0 expected).
  - C/A Jan +1,153 vs -300. HICP 2.5.
  - Sentiment: BWUK -12.2; GUS price expectations 33.3; ESI 100.8; EC inflation expectations 39.4.
  - Budget deficit after Feb: 48.5bn.
- MPC (April meeting 8-9 Apr):
  - Dabrowski (19 Mar): wait for the war to end. On 26 Mar: hold; a hike only in an extreme case; no decision in April.
  - Feb voting record (19 Mar): Tyrowicz's +75bp motion rejected.
  - Glapinski (WSJ, 23 Mar): no pre-commitment.
  - Kotecki (23 Mar): the March cut was the last of 2026; wait-and-see.
  - Tyrowicz (24 Mar): 4.75% is appropriate.
  - There were no MPC minutes in the windows.
- Banks all expect April on hold. FRA markets price 50-75bp+ of hikes.
  - CA (23 Mar): next cut in Q2 2027.
  - PKO (30 Mar): stable for ≥1 year.
  - Santander: no change before July.
  - mBank: CPI 3.8%.
  - ING: March CPI up to 3.5%; the fuel cut is worth -0.9pp.
  - Millennium: April CPI ~2%.
- Fiscal:
  - Fuel package (26-27 Mar): VAT 8%, excise at the minimum, a maximum price. Cost 1.6bn/month. VAT cut runs 31 Mar-30 Apr; excise cut 30 Mar-15 Apr.
  - Fitch report on the SAFE veto (17 Mar).
  - The SAFE signing slipped to mid-April (PKO 30 Mar).
  - Debt-management bill (24 Mar). Domanski (30 Mar): no budget revision.
  - BGK FPC (26 Mar): 873.7m vs 1.06bn, plus 199m additional.

## Not used / outside the windows
- Feb CPI final (13 Mar) and the SAFE veto (13 Mar).
- MPC remarks of 12-13 Mar by Masłowska, Janczyk and Kotecki.
- Cancellation of the 11 Mar switch.
- March plan (27 Feb).
- April/Q2 plans (31 Mar), the March CPI flash (31 Mar), and anything later.
