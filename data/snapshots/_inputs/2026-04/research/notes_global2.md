# Global PIT facts 15-29 Apr 2026: working notes
Windows (Warsaw publication time, CEST throughout): R0416 = 15 Apr; R0417 = 16 Apr; R0420 = 17-19 Apr; R0421 = 20 Apr; R0422 = 21 Apr; R0423 = 22 Apr; R0424 = 23 Apr; R0427 = 24-26 Apr; R0428 = 27 Apr; R0429 = 28 Apr; R0430 = 29 Apr.
Output: facts.json (170 facts + 11 fed_pricing rows), built by build/make_json.py from build/f_MMDD.py (facts per window), build/extra.py (pricing, CB decisions, CPI) and build/digest.py. The facts and fed_pricing schema is the same as the March facts_global_2.json: facts have published / window_report_date / topic / text / src; fed_pricing rows have published / text / src, plus a window_report_date field. The window comes from the Warsaw publication date. New objects, as requested:
- fed_pricing_by_R, ecb_pricing, boe_pricing: dicts keyed by R, each a short text naming its source date.
- cb_decisions: a list of {bank, date, decision, rate, vote, published, note, src}. It includes the last pre-window ECB, BoE, CNB and MNB decisions, so stances are known. Filter on published <= the info cut-off.
- cpi: a list of {country, period, value, core, published, note, src}. It covers EA, US, UK, CZ, HU and RO, plus the German April flash.
- digest and glob: dicts keyed by R.
The build script checks that every cited PAP, Odaily and TE item was downloaded, flags window mismatches between a fact's time and its source's time (none remain), and enforces the length limits (450 characters for digest entries, 60 for glob).

## Big picture (as sourced, no hindsight)
The two-week US-Iran ceasefire (agreed 7-8 Apr) holds militarily, but there is a double blockade. The US has blockaded Iranian ports since 13-14 Apr, and Iran keeps Hormuz under IRGC control and charges transit fees.
- 17 Apr: Iran declared the strait open for the truce. Brent fell about 10%, to below $90 (~$90.4 settle implied). Core yields fell about 8bp, and Fed-cut odds for 2026 rose back to roughly 50-60%.
- 18 Apr: Iran re-closed the strait.
- 19-20 Apr: the US seized the ship Touska.
- 21 Apr: talks in Islamabad never started. Trump extended the truce open-endedly and kept the blockade.
- 22-23 Apr: ships were fired on and seized, and the Navy was ordered to sink mine-layers.
- 25 Apr: the envoys' trip was cancelled.
- 27 Apr: Iran proposed a 'Hormuz-first' deal, which Trump disliked. The UAE quit OPEC on 28 Apr.
- 29 Apr: Trump said the blockade will last until there is a nuclear deal and possibly for months.
Over these windows Brent (June contract) went from ~$95 to $90, then to $101-106, then $111 and finally ~$120 on 29 Apr, the highest since June 2022.

Data and markets:
- Euro area: data turned stagflationary. HICP was revised up to 2.6%, the flash composite PMI fell to 48.6, the ZEW dropped to -17.2, the Ifo fell to 84.4 (lowest since 2020), and consumer inflation expectations reached 4.0%.
- Pricing: ECB pricing went from two hikes, to two hikes plus ~55% for a third (24 Apr), to three hikes fully priced (29 Apr). BoE pricing went from one hike to almost three. Fed pricing went from cut hopes on 17 Apr to hike risk after a hawkish 8-4 hold on 29 Apr; three of the four dissents were against the easing bias.
- Bonds: the Bund 10Y moved towards 3.10%, its highest since 2011. The gilt 10Y went above 5%, a 2008 high. BTP-Bund widened from 72bp to 82bp.
- CEE: Hungary's 10Y fell below 6% after Tisza's two-thirds win, then drifted back to ~6.0-6.1%. The MNB held at 6.25%.

## Access (as of 27 Nov 2026)
- **strefainwestorow listing.** The listing has 30 items per page: p391-388 = 15 Apr; p387-385 = 16-17 Apr; p384 = 17-20 Apr; p377 = 22-23 Apr; p372 = 24-27 Apr; p363-359 = 29-30 Apr. 18 Apr has no items, and only one item each was found for 25 and 26 Apr (the weekend digest on 26 Apr).
  - The index of pages 340-405 is in dl/list/all.tsv (1,945 urls). 248 macro/global articles are in dl/art, their text in txt/, and their times in dl/list/idx.tsv (scripts/ext.py).
  - Digest global sections are read with scripts/skr.py or skg.sh, market lines with scripts/mk.py and mk2.py, and the yield table with scripts/tab.py and tabsum.py.
  - The April PAP feed on strefa is thinner than March's. There are no stand-alone ECB, BoE or Fed-speaker pieces and almost no pricing quotes. Global coverage comes from the 'Skrot wiadomosci' 17:0x/21:0x digests (and the weekend digests of 19 and 26 Apr), the DZIEN NA RYNKACH pieces (~08:20 Asia, ~09:35 Europe, ~14:30 US futures, ~18:10 Europe close, ~22:15 Wall St), the oil pieces (~08:00), the TYDZIEN NA RYNKACH week-aheads (19 Apr 21:12 and 27 Apr 06:34) and the two Powell articles (29 Apr 20:48 and 21:55).
- **Odaily newsflash.** IDs 476690-479010 cover 14 Apr 23:00 to 30 Apr 13:21 CEST. dl/od/all.tsv holds (id, CEST time, title, body), via scripts/odget.sh and odparse.py.
  - The page's JSON-LD datePublished is true UTC; I verified this against the FOMC (20:00 CEST = 18:00Z). So CEST = UTC + 2h (scripts/od.sh prints CEST).
  - Odaily coverage of ECB and BoE is essentially nil in April. Many Jin10 items have Chinese titles but English bodies.
- **Trading Economics (TE) news.** TE was used far more than in March and is the main source for ECB, BoE and Fed pricing, European yields, data with consensus, and rating actions.
  - Pages resolve by ID under any indicator path. IDs 539900-546450 (8 Apr to 1 May) are in dl/te/all.tsv (id, CEST time, headline, body), via scripts/teget.sh and teparse.py; datePublished is UTC (+2h applied).
  - Only each article's own body was used. The cited URL paths were spot-checked and resolve.
- **Official sources.**
  - The FOMC statement (federalreserve.gov monetary20260429a.htm) gave the vote and the easing-bias language.
  - The Eurostat 16 Apr HICP release gave the core, energy and country rows.
  - countryeconomy.com/ratings/<country> was scanned for 25 European sovereigns, reading only rows dated 15-29 Apr.
  - The ECB website speech index and the CNB schedule page could not be fetched (404). The ECB RSS lists only current (Nov 2026) items and was not used.

## Key series (dates = close date unless stated; PAP/Bloomberg table, EU rows = previous close)
- **Bund 10Y:** 14 Apr 3.02, 15 Apr 3.04, 16 Apr 3.03, 17 Apr 2.96, 20 Apr 2.98, 21 Apr 3.00, 22 Apr 3.01, 23 Apr 3.01, 24 Apr 2.99, 27 Apr 3.03, 28 Apr 3.07. For 29 Apr, PAP had 3.10% at 18:08, and the 30 Apr 06:39 table has 3.11 (R0430 morning table: levels only, not used as a fact). TE: "highest since 2011" on 23 Apr and 29 Apr.
- **Schatz:** 2.54, 2.54, 2.52, 2.41, 2.46, 2.53, 2.56, 2.57, 2.55, 2.57, 2.65; the 29 Apr close is 2.74 (30 Apr table).
- **Gilt 10Y:** 4.78, 4.81, 4.85, 4.76, 4.83, 4.88, 4.91, 4.94, 4.91, 4.97, 5.01; 29 Apr 5.07 (30 Apr table). **Gilt 2Y:** 4.21, 4.23, 4.22, 4.12, 4.19, 4.27, 4.34, 4.37, 4.35, 4.39, 4.45; 29 Apr 4.56.
- **Spreads vs Bund (10Y):**
  - OAT: 64, 64, 64, 62, 63, 66, 65, 65, 65, 66, 65 (29 Apr: 67).
  - BTP: 76, 78, 78, 72, 74, 77, 77, 79, 79, 80, 82 (29 Apr: 85).
  - Spain: 43-47.
  - PL10-Bund: 249 -> 241 (17 Apr) -> 267 (28-29 Apr).
- **UST10, live PAP table at 06:3x:** 4.25 (15 Apr am), 4.27, 4.32 (17 Apr, 07:3x, unstamped table), 4.27 (20 Apr), 4.25, 4.29, 4.32, 4.33, 4.32, 4.35, 4.35 (29 Apr table, US rows stamped 28 Apr); 4.43 in the 30 Apr table. Intraday: ~4.23-4.25 on 17 Apr, and 4.41-4.42 after the FOMC on 29 Apr.
- **UST2:** 3.75, 3.75, 3.78, 3.73, 3.72, 3.77, 3.81, 3.84, 3.80, 3.81, 3.84; above 3.95 after the FOMC; 3.94 in the 30 Apr table.
- **CEE 10Y:** CZ10 4.75 -> 4.66 (17 Apr) -> 4.91 (28 Apr); HU10 6.14 -> 5.90 (20 Apr) -> 6.13 (24 Apr) -> 6.07 (28 Apr). **JGB10:** 2.38-2.48 (2.53 in the 30 Apr table).
- **Brent June (PAP ~18:00 European close unless stated):**
  - 15 Apr: 94.75 (22:15; no ~18:00 piece that day).
  - 16 Apr: 98.35.
  - 17 Apr: ~86.5 low; settle ~90.4 implied by the 20 Apr +5.3% move.
  - 20 Apr: 95.31. 21 Apr: 98.08 (~100 at 22:13). 22 Apr: 101.77. 23 Apr: 103.26 (105.7 at 22:20; TE ~106).
  - 24 Apr: 104.6. 27 Apr: 106.3 at 14:32, >108 at 22:27. 28 Apr: 111.51.
  - 29 Apr: 117.69, then 119.75 at 22:20 (TE: 'almost $120', highest since June 2022).
  - Since 28 Feb Brent is up ~50% (PAP 27 Apr). No exchange settlement prices were collected.
- **TTF:** EUR42.2 (16 Apr) -> <EUR39 (17 Apr, lowest since 27 Feb) -> 39.8 (20 Apr) -> 42.5 (21 Apr) -> 43.9 (22 Apr) -> 43.4 (28 Apr) -> 46.8 (29 Apr). EU gas storage 29.6% vs a 43.0% 5-year average (16 Apr), and 31.5% vs 44% (27 Apr).
- **DXY:** ~98, a 6-week low (15 Apr) -> 98.3 (20-21 Apr) -> 98.58 (24 Apr) -> 99.3 high / 98.5 (27 Apr) -> 98.7 (28 Apr) -> 98.96 post-FOMC (29 Apr).
- **ECB EUR/USD fixings:** 1.1780, 1.1782, 1.1797, 1.1760, 1.1767, 1.1733, 1.1694, 1.1712, 1.1749, 1.1680, 1.1706.
- **USD/JPY:** 159.1 -> 158.1 (17 Apr) -> 159.4-159.9 -> 160.20 (29 Apr).
- **Gold:** $4,826 (15 Apr am) -> ~4,825 (16-17 Apr; futures above $4,900 on 17 Apr) -> 4,821 (20 Apr) -> 4,759 (21 Apr) -> ~4,745 (22-24 Apr) -> 4,721 (27 Apr) -> 4,592 (28 Apr) -> 4,565 (29 Apr, a one-month low after the FOMC). Silver ~$80 -> ~$72.

## Timing judgements
- **FOMC (29 Apr).** The decision (29 Apr 20:00) and the presser (20:30) fall in R0430, and so do the post-FOMC swaps and WSJ pricing (20:21-21:40). The Powell fact is stamped 21:55 (the PAP 'opis' that carries its content); Odaily items start at 20:36.
- **ECB and BoE (30 Apr)** fall outside the windows. So do the EZ April flash HICP, Q1 GDP, US Q1 GDP, March PCE, the 30 Apr PAP yield table and the 30 Apr PAP articles; none of them were used. The ECB and BoE pricing shown is pre-meeting.
- **BoJ (28 Apr ~05:11) and MNB (28 Apr 14:00)** fall in R0429.
- **Beige Book** (15 Apr 20:00, PAP 22:15) is in R0416; Odaily carried it on 16 Apr 00:07. The **ECB account** (16 Apr 13:30) is in R0417.
- **Overnight items.** Items first seen between 00:00 and 06:00 belong to the window of that calendar date: FedWatch 16 Apr 00:04 -> R0417; Trump's truce extension 22 Apr 00:04 -> R0423; the Lebanon 3-week extension 24 Apr 00:14 -> R0427; Tillis 27 Apr 02:42 -> R0428; the NYT report that Trump is unhappy, 28 Apr 02:23 -> R0429; the WSJ long-blockade story, 29 Apr 03:06 -> R0430.
- **Rating actions.** The Fri 24 Apr evening actions were first seen on TE on 25 Apr 05:3x (S&P Belgium and Slovakia, Fitch Lithuania, Moody's Norway), with S&P Finland from countryeconomy -> R0427. Moody's Belgium (17 Apr, countryeconomy only; placeholder 23:00) -> R0420.
- **Data facts** use the official release time and cite the PAP digest or TE, as in March. Placeholders: EZ IP 11:00, NAHB 16:00, UK IP/GDP 08:00, US claims/IP 14:30, EZ trade 11:00, CBRT 13:00, Conference Board 16:00, ECB CES 10:00, German CPI 14:00.
- **Weekend digest.** The Witkoff/Kushner cancellation and other weekend content is stamped with the 26 Apr 20:05 weekend digest; Odaily first had the cancellation on 25 Apr 18:01. Both fall in R0427.
- **Cross-window items.** Data released before 15 Apr are not facts here, but they appear in the cpi list with their original release times: US March CPI (10 Apr), HU March CPI (8 Apr), CZ March final and RO March CPI (14 Apr), US March PPI (14 Apr), and the UMich preliminary (10 Apr).

## Caveats / conflicts
- **PAP evening Brent prints are unreliable** in several 22:xx Wall Street pieces: 16 Apr '$90.06' (+2.19%), 17 Apr '$83.13' (-8.84%), 20 Apr '$86.97' (+5.3%), 24 Apr '$89.79'. The 28 Apr 15:02 piece repeats 27 Apr's 'Brent $106.31 (+0.91%)'. These levels are flagged or not used; the ~18:00 European-close quotes, the % moves and TE were used instead.
- **TTF:** PAP's 23 Apr 18:06 line (EUR43.93, +4.75%) is identical to 22 Apr's and is probably stale.
- **TE gilt glitch:** TE '543434' (21 Apr 09:47) has the gilt 10Y at 5.10% (18-year high) and '543492' has '+32bp'. Both conflict with the PAP table (4.83-4.88%) and the other TE pieces (gilts first above 4.95% on 23 Apr). They are treated as a data glitch and not used.
- **FOMC dissents:** TE says 'three members dissenting over language'; the official statement shows four (Miran for a cut plus three against the easing bias). The statement is used.
- **Fed pricing after the FOMC:** Jin10 has ~50% for a 25bp hike by April 2027 via swaps, while TE has 'roughly one in three'. Both are quoted.
- **Consensus figures differ by source:** claims 213k (PAP) vs 215k (Jin10) on 16 Apr; Ifo 85.7 (PAP) vs 85.5 (TE); UK retail 0.0% (PAP) vs +0.2% (TE). Ranges are given.
- **Beige Book wording:** 'slight to modest' (Odaily) vs 'od niewielkiego do umiarkowanego' (PAP).
- **TE 'Euro Gains for 3rd Week'** (17 Apr) says 'up 2.7% on the week'. This looks implausible and was not used.
- **Bund levels:** TE intraday levels (3.05%, 'towards 3.1%') run slightly above the PAP close prints (3.01-3.07); both are labelled.
- **Iran's leader:** the 'Khamenei' order on Hormuz (26 Apr) refers to Supreme Leader Mojtaba Khamenei (named 9 Mar).
- **Moody's Lithuania:** the countryeconomy row dated 17 Apr shows only '(Stable)', i.e. no rating change, and is treated as an affirmation.
- **Missing table stamps:** the 17 Apr PAP yield table has no date stamps (EU rows are 16 Apr closes, US rows live at 07:3x).

## Gaps
- **ECB:** no Lagarde 22 Apr 19:30 speech content, and no Nagel, de Guindos, Kocher or Sleijpen speeches (21-23 Apr). The only Schnabel item is ABN Amro's second-hand reference that 'the ECB can take time', in the 27 Apr week-ahead. There are no €STR or OIS levels: ECB pricing is TE text only.
- **BoE:** apart from TE's summaries of Bailey and Greene (16 Apr) and Breeden (24 Apr), there are no speeches. Pricing is TE text only (no SONIA levels). The UK labour data cover the 3 months to Feb; the March payroll figure (-11k) is from TE.
- **Fed:** no FedWatch prints for 17 Apr evening to 20 Apr, 22-23 Apr or 25-28 Apr. Fed speakers were captured only up to the blackout (Musalem, Harker, Goolsbee, Williams, Daly); there are no SEP or dots (April has none). The March PCE and Q1 GDP advance are published on 30 Apr, outside the windows. Commerzbank's estimate (PCE ~3.4% headline, 3.1% core) is in the week-ahead fact; Powell said core PCE is ~3.2%.
- **US data not captured:** existing and new home sales were not searched for. US March PPI (+0.5% m/m vs +1.1% expected, 14 Apr) is before the windows and was not filed.
- **CNB:** no meeting in the windows (the last was 19 Mar, a 7-0 hold at 3.50%). The 2026 schedule page was not retrievable, so the next date was not confirmed. No CZ April flash CPI in the windows. CZ core CPI is not given.
- **NBR:** no decision found in TE or PAP for 1-29 Apr, and no core CPI for Romania.
- **Ratings:** no agency press releases were retrieved. Moody's Belgium (17 Apr) and S&P Finland (24 Apr) come from countryeconomy rows only. No actions were found for France, Italy, Spain, Austria, Czechia, Hungary or Romania in 15-29 Apr. The S&P review of Poland is on 8 May (outside).
- **US tariffs/trade:** only the USMCA items (Greer's 'no return to zero tariffs', 20-21 Apr), the US accusation of Chinese AI-technology theft (23 Apr), Canada's beer and alcohol stance (23-24 Apr) and the Section-232 context. Nothing on the Section 122 10% tariff's 150-day limit (it runs 150 days from 24 Feb) was found in the windows.
- **Prices:** no exchange settlement prices for Brent, TTF or gold (intraday and PAP quotes only). Brent switched contract month at the end of April (the June contract expired 30 Apr), which may exaggerate the late-April squeeze in front-month quotes.
