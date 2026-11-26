# PIT facts 5-14 Jan 2026 (report dates 7-15 Jan) - working notes
Output: facts.json (same folder). Builder: scripts/build.py. Raw downloads: dl/ (list, art, txt, gov, res, ing, pko, mb).
Windows: R0107=5-6 Jan, R0108=7, R0109=8, R0112=9-11, R0113=12, R0114=13, R0115=14 Jan (Polish time).
Timestamps: PAP article times are exact; PAP "Skrot wiadomosci" times (17:0x/21:0x) are UPPER BOUNDS; PDF CreationDate is UTC (+1h added);
Erste uses upload time embedded in URL (later than PDF creation, so conservative).

## Access tips (26 Nov 2026)
- strefainwestorow listing: 5 Jan = p544-545, 7 Jan = p541-543, 8 Jan = p538-541, 9 Jan = p536-538, 12 Jan = p534-536, 13 Jan = p532-534, 14 Jan = p531-532, 15 Jan = p528-530. ~30 articles/page; parallel curl sometimes fails with exit 35 -> retry.
  The mirror is a SUBSET of PAP: no standalone MoF/BGK auction articles; use "Skrot wiadomosci" 17:00/21:00 and "DZIEN NA FX/FI".
- gov.pl reachable now (was not on 10 Nov). EN debt news list: https://www.gov.pl/web/finance/news-public-debt?page=5 (Jan 2026). Auction offers/results are NOT posted as news pages;
  per-series results come from the MoF transaction database Obligacje_Hurtowe.xlsm = https://www.gov.pl/attachment/d12c559c-9773-4563-905e-c1d6bbcc1c75 (sheet "Operacje"; T-bills db = attachment 31ac439a-...). Later document: use only rows whose publication date is confirmed by PAP.
- PKO Dziennik: list at https://centrumanaliz.pkobp.pl/aktualnosci?offset=220 (5-14 Jan = offsets 220-225); each article page links cdn-netpr PDF.
- Millennium daily: bankmillennium.pl/documents/d/guest/dailyYYMMDD (260105, 260107 = 404; 260108-260114 OK); weekly260112 OK.
- Erste/Santander Codziennik archive: https://www.erste.pl/serwis-ekonomiczny/codziennik/archiwum (Jan files: ids 168959,168963,168966,168968,168976,168983,168984).
- Credit Agricole MAKROmapa: makromapa-05012026_34681.pdf, makromapa-12012026_34715.pdf (server returns empty 200 for wrong ids; probe by size).
- DB Polska: weekly wa260107pol.pdf, wa260113pol.pdf; daily only daily260108pol.pdf found (others 404).
- ING Think: preview 13 Jan, post-decision 14 Jan (datePublished in HTML; no time).
- MNI NBP preview PDF created 13 Jan 11:25 UTC: compiles sell-side views (BOS, CA, Pekao, Santander, JPM, GS, SocGen, Velo, BNY, Bank Pocztowy, BGK, PKO, ING, Millennium).
- Blocked: bgk.pl (403), nbp.pl PDFs (403), isbnews.pl (no response), bosbank.pl (Cloudflare per earlier note).

## Key findings
- 9 Jan auction (announced 7 Jan, 8-12bn; monthly plan 31 Dec said 7-12bn): 7 series. Sold 12,002.318m vs demand 22,276.318m; additional sale 1,686m same day; settlement 13 Jan.
  Per series (uniform price): OK0128 730/3125 @92.920 (3.678%); PS0130 1567.318/3385.318 @102.683 (4.258%); WZ0930 872/4212 @97.130; PS0131 4836/5556 @99.970 (4.504%);
  NZ0331 1255/2070 @95.200; DS1033 1050/1678 @107.256 (4.851%); DS1035 1692/2250 @99.040 (5.121%). Add. sale: PS0130 240, WZ0930 212, PS0131 50, DS1033 13, DS1035 1171.
- NEW: NZ0331 (PL0000118774), POLSTR-compounded floater, mat 25 Mar 2031, semi-annual 25 Mar/25 Sep, accrual from 25 Sep 2025, issue letter 157/2025 dated 22 Dec 2025, first sale 9 Jan 2026.
  Not offered in window: PS1031, DS0436, WZ0532, WZ0931 (none seen). FPC0332 is not new (sold May 2025).
- EUR syndication: mandate 8 Jan; priced 8 Jan EUR 2bn 2.875% Jan-2031 (2.964%, MS+43) + EUR 1.25bn 3.625% Jun-2036 (3.739%, MS+83), book >12bn.
- Financing: prefinancing end-2025 ~21% (MoF 9 Jan 14:27); ~26% after 9 Jan ops (MoF 12 Jan 09:58). Millennium: ~23% of ~690bn.
- No switch/buyback in window; T-bill 36W 2-4bn on 16 Jan (plan 31 Dec; offer 15 Jan, outside window); 22 Jan offer not published by 14 Jan.
- BGK FPC 12 Jan: FPC0229/0231/0332/0235, min 1.0bn (announced 8 Jan evening); sold 3.734bn vs 7.05bn demand, +709m additional sale. Per-series NOT FOUND. No FWSZ auction found.
- MPC: Dabrowski (Bloomberg, 8 Jan) 50% odds of Jan cut, leans pause, 50bp room by mid-2026; Tyrowicz LinkedIn 8 & 9 Jan dovish-ish; Nov vote 9-1 + rejected 125bp hike motion (8 Jan).
  Glapinski: no comments found 5-13 Jan (press conf 15 Jan, outside). Zarzecki wPolsce24 comment via MNI 13 Jan (original date unknown, possibly pre-window).
  Millennium 12 Jan weekly mentions I. Duda suggesting next cut in March - date of her comment not established; NOT put in facts.
- Polls: Parkiet 13 Jan 06:00: 3 of 19 expect cut. MNI 13 Jan: clear majority hold; GS cut; PKO cut on cards; ING 35%; DB 15%.
- 14 Jan decision (PAP 14:37): hold, ref 4.00/lombard 4.50/deposit 3.50/rediscount 4.05/discount 4.10; statement 16:00: data-dependent; risks fiscal policy, "expected" demand recovery, wages, foreign macro incl. commodity prices; energy prices dropped from risk list.
  Unusual: mid-month meeting (first after New Year), first meeting of M. Zarzecki; statement estimated core ~Nov level; risk list change. No vote info until later.
- GUS in window: only minor (median wage July 7 Jan; housing prices Q3 8 Jan; GG non-financial accounts Q3 9 Jan; REGON/barriers 12 Jan; foreigners 13 Jan). Dec final CPI due 15 Jan 10:00: consensus 2.4% y/y, 0.0% m/m (Erste/market and DB/Bloomberg); core 16 Jan consensus 2.8%.
- NBP data: reserves Dec 231.02bn EUR (7 Jan 14:01); BoP Nov C/A -460m vs +500m PAP consensus (13 Jan 14:00); gold 27.5% / 543.4t (13 Jan).
- Ratings: no sovereign action found 5-14 Jan (status as of then per earlier notes: Fitch A-/Neg, Moody's A2/Neg, S&P A-/Stable). Fitch affirmed Santander BP A- on 14 Jan (bank, ignore).
  CAUTION: web search shows later 2026 rating actions (Moody's Sep 2026, S&P Nov 2026) - post-window, NOT used.
- Fiscal: budget 2026 finished in Sejm 9 Jan (deficit 271.7bn), reached President 13 Jan, President undecided (12 Jan); vetoes cost 1.8bn (2026)/2.8bn (2027) + 855m NFZ; GG deficit Q3 58.4bn (4Q roll 7.0% GDP);
  FWSZ 2025 spend 51.4bn (5 Jan); KPO PIP milestone saga 7-9 Jan; EU funds 58.8% of 2021-27 cohesion contracted; BGK paid 63.1bn; MoF considering JPY/CHF/USD issues (14 Jan); SAFE: only Erste Group mention (12 Jan).

## Not used / post-window seen (do not use)
- BNP Paribas RPP note 16 Jan; mBank RPP note 15 Jan; PKO Dziennik 15-16 Jan (Glapinski dovish 15 Jan, Kotecki Feb cut); 22/28 Jan auction rows in MoF db; NZ coupon notice 18 Mar 2026.
