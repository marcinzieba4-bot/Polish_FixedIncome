# PIT facts 31 Mar - 14 Apr 2026 (report dates 1-15 Apr) - working notes
Output: facts.json (same folder). Keys: mof_ops, new_series, bgk, facts, gpwb, wz_coupons, meta (as in 2026-03 facts_poland_2.json) plus mpc, data, digest (keyed by R).
Builder: scripts/build2.py (runs build.py). Helpers: scripts/listparse.py, fetch.sh, h2t.py, skrot.py, rd.py, fxfi.py, pko.py, mil.py, govlist.py, govpage.py, db_rows.py, bony.py.
Raw downloads: dl/list (strefainwestorow p386-416), dl/art + dl/txt (673 PAP items 31 Mar-14 Apr), dl/index.json, dl/day_MMDD.txt (relevant items per day), dl/gov (April plan + PDF, Q2 plan + PDF, USD mandate/pricing pages, komunikaty-dlug p1-5), dl/db (Obligacje_Hurtowe.xlsm, Bony_Skarbowe.xls), dl/gpwb (index calendar), dl/res/{pko,mil,erste,db,bps}.
Windows: R1 Apr=31 Mar, R2=1 Apr, R7=2-6 Apr, R8=7 Apr, R9=8 Apr, R10=9 Apr, R13=10-12 Apr, R14=13 Apr, R15=14 Apr.
Timestamps: PAP article times exact; PAP Skrot 17:0x/19:0x/21:xx = upper bounds; PDF CreationDate is UTC in these files, converted to CEST (+2h) = upper bound; Erste = upload time in the URL; gov.pl gives a date only (no time in the page HTML).

## Access tips (27 Nov 2026)
- strefainwestorow listing: https://strefainwestorow.pl/wiadomosci?page=N (not /wiadomosci/pap). ~1.5-2 pages/day in April (thinner than March):
  31 Mar = p411-413, 1 Apr = p408-411, 2 Apr = p405-408, 3-7 Apr = p402-405, 8 Apr = p399-402, 9 Apr = p397-399, 10-12 Apr = p395-397, 13 Apr = p393-395, 14 Apr = p391-393.
  Fetch ascending; a few pages fail on the first try (curl --retry). Article time sits in `<time class="pr-1" datetime="HH:MM">`; body ends at the first `...block-d-newsroom` div (some pages have the `see-also-link` variant).
  The 31 Mar 17:10 FX/FI close has an empty body on the site (use Skrot 21:06).
- The feed lacks some PAP Biznes items seen in March (no MoF April-plan article, no PMI release article, no PAP MPC-consensus article, no NBP C/A headline, no T-bill offer); the Skrot digests carry most of them.
- MoF debt communiques: gov.pl/web/finanse/komunikaty-dlug?page=4&size=10 holds the 31 Mar plans and the 7 Apr USD pages; page 3 starts with 15 Apr (outside). Only list titles of later pages were seen, no content used.
- MoF DBs: Obligacje_Hurtowe.xlsm (attachment d12c559c..., last-modified 25 Nov 2026) and Bony_Skarbowe.xls (attachment 31ac439a..., last-modified 18 Nov 2026; read with xlrd). Both linked from gov.pl/web/finanse/bony-i-obligacje-hurtowe1.
- PKO: centrumanaliz.pkobp.pl/aktualnosci?offset=155-170 lists 23 Mar-20 Apr dailies; each article page links the cdn-netpr PDF (curl -L).
- Millennium dailyYYMMDD: all window days exist except 260407 (404).
- Erste archive https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum: 31.03 169188, 01.04 169190 (uploaded 15:06), 02.04 169191, 03.04 169192, 07.04 169195 (13:39), 08.04 169198, 09.04 169208, 10.04 169219 (12:57), 14.04 169244. No 13 Apr file.
- DB: only wa260408pol (folder 2026/04; ModDate 22 Apr). BPS: only 20260407.
- gpwbenchmark.pl: calendar fetched with a browser UA after a retry; later requests returned empty replies (curl 52). bgk.pl 403. nbp.pl reachable (not needed).
- WARNING: the MoF bond DB already contains the 15 Apr auction rows and the komunikaty pages list later notices. Neither was used.

## Key findings
- MoF April plan and Q2 plan (31 Mar, slot 15:00; R1 Apr):
  - Sales on 15 Apr (4-12bn; OK0128/NZ0331/PS0731/DS1035/NZ0936), 23 Apr (6-14bn) and 28 Apr (5-13bn). DS0436 replaces DS1035 from 23 Apr.
  - No switch in April. T-bill 10 Apr: 50-week, 3-6bn.
  - Q2: 7-8 sales for PLN 50-90bn; 1-2 switches buying back 2026/27 maturities.
  - Drop (MoF): budget accounts ~167bn end-March. Actual 169.5bn (9 Apr). Liquidity consolidation 136.0bn.
  - Financing ~41% at end-Q1 (PAP 6 Apr). No newer ratio found.
- USD issue, 7 Apr (gov.pl date only; R8 Apr):
  - Mandate to Citi/GS/JPM/SG, then USD 6bn priced the same day.
  - 5Y 1bn, 4.625% coupon, 4.645% (UST+65). 10Y 2.5bn, 5.375%, 5.405% (+105). 30Y 2.5bn, 6.125%, 6.233% (+130). Maturities 14 Apr 2031/2036/2056.
  - First PAP mention: Skrot 8 Apr 17:02.
- T-bill 10 Apr (R13 Apr): new 50-week line PL0000006227 (maturity 30 Mar 2027, settles 14 Apr).
  - Sold 3,005m on 3,605m demand (offer 3-6bn) at 96.3018 = 3.95%. Additional sale 394.0m (offer 534m).
  - DB rows match PAP Skrot 17:02 exactly. ING (14 Apr) called it disappointing.
- 15 Apr sale OFFER (13 Apr, R14): 6-12bn in OK0128, WS0428 (added), NZ0331, PS0731, DS1035, NZ0936. Results are outside the windows.
- No switch/buyback, no WZ/NZ/PP coupon notice, no FX-account communique in the windows.
- MPC 8-9 Apr (R10 Apr): hold, ref 3.75 / lombard 4.25 / deposit 3.25 / rediscount 3.80 / discount 3.85 (PAP 14:06).
  - Statement (15:00): CPI risks are commodity prices and global inflation, fiscal policy, fuel-price regulation, activity and wages. FX intervention possible.
  - Glapinski (conference 9 Apr 15:00): no change soon either way; "o podwyzce nie ma mowy", but would hike quickly in a black scenario; question mark over cuts; fears second-round effects; NBP 2025 loss 35.7bn; gold 580t (target 700t).
  - PAP survey (8 Apr): hold through H1 2027, one cut H2 2027.
- MPC members:
  - Litwiniuk (2 Apr): no near-term cuts, hike possible.
  - Kotecki (2 Apr): the March cut was the last of 2026. Kotecki (14 Apr, PAP Biznes): hold at least to the July projection; ready to act either way.
  - Janczyk (13 Apr, Bloomberg via Skrot; details in PKO 14 Apr): flat for quarters; hike only if CPI > 3.75% for three months.
  - March minutes (13 Apr 14:00): probability of further cuts fell significantly; one "rates too low" opinion.
  - NBP X post (11 Apr): unrealised gold gain 169bn.
- Data (actual vs consensus):
  - March CPI flash 3.0% y/y / 1.0% m/m vs PAP 3.3 / 1.4. Fuels +15.4% m/m, food 0.0% m/m.
  - PMI 48.7. GG deficit 2025 7.2% of GDP, debt 59.7%.
  - Unemployment March 6.1% vs 6.0%. Feb C/A -990m EUR vs +433.5m (exports 1.9 vs 1.0; imports 3.3 vs -0.1).
  - Reserves 253.53bn EUR. Retail bonds March 7,274m. Non-residents Feb 194.9bn (12.7%). ST debt end-Feb 2,037.5bn.
  - Budget deficit after March ~69.5bn (Napiorkowska, 14 Apr; official data 15 Apr = outside).
  - NBP survey: CPI 2026 2.9%. World Bank GDP 3.1%. IMF GDP 3.3%, CPI 3.3%.
- Fiscal and ratings:
  - CPN fuel package: excise cut extended to 30 Apr (13 Apr); VAT 8% to 30 Apr; cost ~930m + ~750m for 30 Mar-30 Apr.
  - Domanski (10 Apr): no budget amendment; windfall-tax bill in April (8 Apr).
  - Fiscal Council (1 Apr): CPN to end-2026 = +0.37% of GDP deficit, probably a budget amendment.
  - S&P report (2 Apr): deficit f/c 7.0% (2026), 6.0% (2027); 8.0/7.0 in an oil-shock case. No rating action; S&P review 8 May.
  - KPO EUR 7.2bn approval expected in April; BGK 'Chrobry' SPV for the defence fund.
- Market (PAP same-day): 10Y neared 6% on 30 Mar.
  - 31 Mar -6-8bp intraday. 1 Apr double-digit falls. 2 Apr +2-3bp. 3 and 6 Apr no session. 7 Apr small rises (PKO next day: +16-23bp).
  - 8 Apr ~-40bp on the ceasefire. 9 Apr slightly higher. 10 Apr lower. 13 Apr slightly higher. 14 Apr 10Y ~5.52%.
  - FRA: up to three 2026 hikes "a few days ago" (PKO, 8 Apr); ~50bp (PKO 2 Apr); two hikes/50bp within a year (Millennium 7 Apr); at most one (8 Apr); ~one by year-end (13 Apr).
- BGK: Q2 FPC calendar 16/29 Apr, 14/28 May, 18 Jun (31 Mar). 16 Apr offer FPC0229/0231/0332/0235, min 500m (14 Apr). No BGK auction and no FWSZ activity in the windows.
- GPWB: no new bond-index communique. The 31 Mar periodic change took effect (PS1026 out of TBSP, 17 bonds). Next 28/30 Apr.

## Not used / outside the windows
- 15 Apr: MoF sale results (DB rows exist), CPI final, budget data and FX-account communique. 16 Apr: core CPI and BGK FPC results. 23/28 Apr auctions and DS0436 terms. Later MoF communiques (only titles seen while paging).
- Pre-window re-quotes: Dabrowski DGP (26 Mar), Janczyk PAP (12 Mar), Domanski 30 Mar remarks in PKO 31 Mar, the 27 Mar GPWB communique content.
- Web search was not used. No post-window rating outcomes were consulted.

## Gaps
- USD communiques have no time (gov.pl date only). Order book and ISINs were not published.
- The T-bill offer text (9 Apr) is missing from the feed. The offer range comes from the plan and the DB row.
- No PAP C/A headline article (NBP slot 14:00; Skrot 17:02 used). PMI consensus only from Santander 2 Apr.
- Times are first-dated-mention upper bounds for: Janczyk Bloomberg (13 Apr), Domanski windfall-tax remark (Polsat News; PAP 8 Apr 08:29), Domanski excise remark (PAP 10 Apr 15:48).
- No financing ratio after the USD issue (41% at end-Q1 is the latest).
- Bank research is incomplete:
  - ING Think, Pekao and mBank own notes were not downloaded; their views come via PAP.
  - No Erste 13 Apr daily; no Millennium 7 Apr daily; DB has only 8 Apr (re-saved 22 Apr); BPS has only 7 Apr.
- bgk.pl returns 403 (BGK via PAP only). gpwbenchmark communique pages were unreachable after the calendar fetch.
- March MPC voting record not seen in the windows. NBP core CPI and M3 for March fall outside.
