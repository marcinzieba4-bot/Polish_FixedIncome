# Global PIT facts 31 Mar - 14 Apr 2026: working notes
Windows (Warsaw publication time, CEST = UTC+2 throughout): R0401 = 31 Mar; R0402 = 1 Apr; R0407 = 2-6 Apr (Good Friday 3 Apr, Easter Monday 6 Apr); R0408 = 7 Apr; R0409 = 8 Apr; R0410 = 9 Apr; R0413 = 10-12 Apr; R0414 = 13 Apr; R0415 = 14 Apr.
Output: facts.json, built by build/make_json.py (facts in build/facts_a.py and build/facts_b.py, digest/headlines in build/digest.py, helpers in build/lib.py). It has 141 facts and 16 fed_pricing rows.
The facts and fed_pricing schema is the same as the March facts_global_2.json (published / window_report_date / topic / text / src). This file also adds window_report_date to each fed_pricing row.
New objects, all keyed by R:
- fed_pricing_short, ecb_pricing, boe_pricing: short text with the source date.
- cb_decisions: the latest decision known at R for the Fed, ECB, BoE, CNB, MNB and NBR (bank, date, decision, rate, vote, next).
- cpi: the latest print known at R for the euro area, US, UK, Czechia, Hungary and Romania (country, period, value, core, published).
- digest: up to 450 characters per window, in the style of the 'Abroad:' part of WK.
- glob: a headline of up to 60 characters, GLOB style with a leading space.
- yield_tables: the PAP/Bloomberg morning tables, keyed by table timestamp, including the 15 Apr table that is used for levels only.
The window comes from the publication date, and published times come from the article or newsflash stamp. Data facts use the official release time and cite the PAP digest, TE or the official page (as in March).
New topic label: "NBR" (Romania). Czech data are under "CNB" and Hungarian data under "MNB". Hungarian politics and elections, CEE fiscal items and the yield tables are under "sovereign". US tariffs and trade are under "geopolitics", as in March.

## Big picture (as sourced, no hindsight)
- 31 Mar-7 Apr: the war in its fifth and sixth weeks swung between exit talk and escalation:
  - 31 Mar: the WSJ reported that Trump would end the war even with Hormuz shut.
  - 1 Apr: Trump said the US would leave "in two or three weeks".
  - 2 Apr: his prime-time address promised two to three more weeks of heavy strikes.
  - 4-7 Apr: ultimatums, with a deadline of Tue 7 Apr 20:00 ET (02:00 Warsaw on 8 Apr).
- Brent ended March with a record gain of about 50%. June Brent traded at $100-111. Dated Brent topped $140 on 2 Apr.
- Rate pricing shifted with each headline:
  - ECB: two to three 2026 hikes, with ~50-70% odds of an April hike.
  - BoE: two hikes.
  - Fed: no cut. Payrolls were +178k on 3 Apr.
- 8 Apr (announced 00:36 Warsaw): a two-week US-Iran ceasefire brokered by Pakistan.
  - Brent fell 13% to ~$95 and TTF 15%. The Bund 10Y fell 14bp and the Schatz 23bp.
  - ECB hike pricing dropped from 80bp to 51bp, and April odds from >70% to 40%. BoE pricing fell to one hike.
  - The FOMC minutes (8 Apr 20:00) showed more officials favouring two-sided guidance.
- 9-12 Apr: the truce was fragile.
  - Israel kept striking Lebanon, and Iran capped Hormuz transits at about 15 ships a day.
  - US March CPI was 3.3% with soft core at 2.6%. UMich one-year inflation expectations were 4.8%.
  - The Islamabad talks (11-12 Apr, Vance and Ghalibaf) ended without a deal, and Trump ordered a naval blockade.
- 13 Apr: the US blockade of Iranian ports started at 16:00 Warsaw.
  - Brent went back to $102 and ECB pricing to nearly three hikes.
  - Hungary: Tisza won a two-thirds majority on 12 Apr. HUF was at its strongest vs USD since 2022, and HU10Y fell from 7.28% (30 Mar) to 6.23% (13 Apr).
- 14 Apr: hopes for a second round of talks took Brent to ~$95, EUR/USD above 1.18 and DXY to 98.0.
  - The IMF cut 2026 world growth to 3.1%.
  - US PPI was soft.
- Core yields stayed close to the late-March multi-year highs:
  - Bund 10Y: 2.94-3.09% closes, against a 15-year intraday high of 3.13% in late March (TE).
  - Gilt 10Y: 4.71-4.94%.
  - JGB10: new highs since 1999 (2.47% on 13 Apr). JGB2 1.39% was the highest since 1995.
  - Periphery spreads narrowed: BTP-Bund went from 95bp to 76-80bp and OAT-Bund from 73bp to 64-66bp.

## Access
- strefainwestorow listing as of 27 Nov 2026: 31 Mar is p411-413, 1 Apr p408-411, 2-6 Apr p404-408, 7 Apr p402-404, 8 Apr p399-402, 9 Apr p397-399, 10-12 Apr p395-397, 13 Apr p393-395 and 14 Apr p391-393. The URL is https://strefainwestorow.pl/wiadomosci?page=N, and titles are in the h5 tags.
  - The index (809 urls, p389-415) is in dl/list/all.tsv, built by scripts/idx.py.
  - 218 macro, market and digest articles are in dl/art. Their text is in txt/ (scripts/ext.py), and times (the `<time>` tags) are in dl/list/idx_s.tsv.
  - The "TYDZIEŃ NA RYNKACH" piece of 13 Apr was missing from the index because of page shift and was fetched by URL.
  - Digests: 17:00 and 21:00 on weekdays. On 3 Apr there is only a 19:00 digest; the weekend digest is 4-5 Apr and the 6 Apr digest is at 19:55. Read them with scripts/skr.py or skrf.sh; scripts/mk.sh prints market lines.
- PAP yield tables: scripts/tab.py, then scripts/series.py, give dl/series.json. EU rows are the previous close (date-stamped) and US/JP rows are live at 06:3x.
  - The 6 and 7 Apr tables carry the 2 Apr closes stamped 03.04.
  - The 10 Apr table (07:27) has no stamps; its EU rows are the 9 Apr closes, confirmed by the 1D column of 13 Apr.
- Odaily newsflash: IDs 474530-476760 cover 30 Mar 14:39 to 15 Apr 02:19 Warsaw. Index: dl/od/all.tsv (id, Warsaw time from article:published_time UTC + 2h, title, truncated og:description).
  - Full bodies come from scripts/odfull.py (div#newsflash-content).
  - 92 IDs returned no page. Pages come back in Chinese even under /en/, but the title and description are English.
  - Odaily coverage thins out between about 19:00 and 02:00 Warsaw, so US-afternoon Fed speakers are often missing.
- Trading Economics news: IDs 537600-542300, each fetched via /united-states/news/news/<id> (any path resolves).
  - The datePublished field is UTC (+2h applied). Index: dl/te/all.tsv, and the window deduplicated by (time, headline) in dl/te/win.tsv.
  - Descriptions are about 700 characters. For full text, use div.news_description on the page.
  - TE is the main source for ECB and BoE pricing text and for the euro-area, Czech, Hungarian and Romanian data.
  - A few IDs redirect to unrelated dates, which are filtered by date.
- Official sources:
  - Eurostat flash HICP page: euro-indicators w/2-31032026-ap.
  - FOMC minutes: federalreserve.gov fomcminutes20260318.htm.
  - Fed Board speeches: /json/ne-speeches.json and jefferson20260407a.htm.
  - countryeconomy.com/ratings/<country> was scanned for 34 European sovereigns (dl/rat).
  - The ECB speech and interview lists are dynamic (foedb) and were not usable. The BNR and CZSO pages were not reachable or redirected, so TE was used instead.

## Key series (dates are close dates unless stated)
- Bund 10Y (PAP table close): 30 Mar 3.04, 31 Mar 3.00, 1 Apr 2.99, 2 Apr 2.99, 7 Apr 3.08, 8 Apr 2.94, 9 Apr 2.99, 10 Apr 3.06, 13 Apr 3.09, 14 Apr 3.02 (from the 15 Apr table). The 15-year intraday high was 3.13% in late March (TE).
- Schatz: 2.62, 2.62, 2.60, 2.62, 2.72, 2.49, 2.52, 2.60, 2.65, 2.54.
- Spreads vs Bund:
  - OAT: 73, 72, 68, 69, 70, 64, 62, 65, 66, 64bp.
  - BTP: 95, 91, 84, 86, 89, 77, 75, 78, 80, 76bp.
  - Spain: 52, 51, 47, 48, 49, 44, 44, 46, 46, 45bp.
- Gilt 10Y: 4.94, 4.92, 4.83, 4.83, 4.90, 4.71, 4.75, 4.84, 4.87, 4.78. Gilt 2Y: 4.45, 4.41, 4.30, 4.32, 4.41, 4.17, 4.18, 4.26, 4.32, 4.21.
- UST10 (PAP live at 06:3x): 4.32 (31 Mar), 4.29, 4.37 (2 Apr, post-address), 4.35 (6 Apr), 4.34, 4.24 (8 Apr, post-ceasefire), 4.29, 4.30, 4.34, 4.28, 4.25 (15 Apr).
  - European-close quotes: 4.33 (31 Mar), 4.30, 4.30, 4.33 (6 Apr), 4.27 (8 Apr), 4.28, 4.29, 4.33, 4.27.
  - The 8-month high of 4.44% was set on 27 Mar (TE).
- UST2: 3.81, 3.77, 3.85, 3.85, 3.86, 3.72, 3.79, 3.79, 3.83, 3.77, 3.75.
- 2s10s: +48 to +52bp throughout.
- JGB10: 2.34, 2.32, 2.39, 2.42, 2.42, 2.37, 2.40, 2.43, 2.47, 2.43, 2.41. JGB2 was 1.391% on 2 Apr (the highest since 1995).
- CEE:
  - CZ2: 4.29 to 3.96 (14 Apr). CZ10: 4.97 to 4.75.
  - HU10: 7.28 (30 Mar), 7.17, 6.88, 6.94, 6.90, 6.72, 6.65, 6.55, 6.23 (13 Apr, the first close after the election), 6.14 (14 Apr). TE intraday 13 Apr: 6.31%, the lowest since Nov 2024.
- Brent front month. The May contract expired 31 Mar and June is the front month from 1 Apr. These are PAP or TE quotes, not settlement prices:
  - 31 Mar: May $116.5-118.9 (expiry day); TE (June?) ~$105-108.
  - 1 Apr: June $101.8 at 18:20, briefly below $100, ~$100.5-100.8 late.
  - 2 Apr: $108.4-109.4 (+7-8%) after the address.
  - 3 Apr: closed.
  - 6 Apr: $108.6-110, ~$111 late (TE).
  - 7 Apr: ~$110-111 during the day, ~$105-106 late.
  - 8 Apr: $95.11 at 18:20; ~$94.75 late (-13%); ~$91.7 intraday.
  - 9 Apr: $96.9-98.0; above $99 intraday (TE).
  - 10 Apr: $95.4-96.9; ~$94.5 late. Weekly about -11%.
  - 13 Apr: ~$103 at the open; $101.8-102.1 (+7%) at 14:34-18:13; ~$98 late (TE).
  - 14 Apr: $98.6 am; $95.95 at 18:04; ~$95 late (TE).
  - Dated Brent was $141.37 on 2 Apr (S&P Global via Odaily), the highest since 2008.
- TTF: €53.3 (31 Mar close, TE) / €50 (PAP 18:13); €47.7 (1 Apr); ~€50 (2 Apr); €49.5-52.3 (7 Apr); €45.3 (8 Apr, -15%, five-week low); €44.7 (9 Apr); <€45 (10 Apr); €46.2 (13 Apr, +6%); <€44 (14 Apr am, TE).
- DXY: 100.17-100.27 (31 Mar), 99.41 (1 Apr), 99.9-100.2 (2 Apr), 100.0 (6 Apr), 98.66-98.82 (8 Apr), 98.79-98.92 (9 Apr), 98.73-98.80 (10 Apr), 98.79-99.02 (13 Apr), 98.0-98.06 (14 Apr, a one-month low).
- ECB EUR/USD fixings: 31 Mar 1.1498, 1 Apr 1.1605, 2 Apr 1.1525, 7 Apr 1.1557, 8 Apr 1.1706, 9 Apr 1.1685, 10 Apr 1.1711, 13 Apr 1.1684, 14 Apr 1.1793. There were no fixings on 3 or 6 Apr (TARGET holidays). EUR/USD traded above 1.18 on 14 Apr. GBP/USD went from about $1.32 to about $1.36.
- Gold: $4,564-4,620 (31 Mar; TE: the worst month since 2008); $4,778-4,786 (1 Apr; NY futures above $4,800); <$4,600 (2 Apr, -3.3%); $4,644-4,716 (6 Apr); $4,610-4,639 (7 Apr); $4,760-4,839 (8 Apr); $4,713-4,818 (9 Apr); $4,788 (10 Apr); $4,721-4,735 (13 Apr); $4,762-4,835 (14 Apr). Silver: $73-79.
- Central-bank pricing (see the objects):
  - ECB: at least 2 hikes (31 Mar), 2 (1 Apr), ~3 (2-7 Apr), 51bp (8 Apr), at least 2 (9-10 Apr, 30% for a third), nearly 3 (13 Apr), at least 2 (14 Apr). April odds: >70% on 7 Apr, then 40% on 8 Apr.
  - BoE: 2 hikes with 50% for April (31 Mar), <2 (1 Apr), 2 (2-7 Apr), 1 (8-10 Apr), nearly 2 (13-14 Apr).
  - Fed: FedWatch April hold 99.5% (1 and 3 Apr), 98.4% (10 Apr). June cut odds: 9.4%, 7.8%, then 2.0% (after NFP), 1.5%. Odds of a cut by year-end: 20%, 10% (2 Apr), 56% (8 Apr), ~30% (9 Apr), ~30% (14 Apr, TE).

## Timing judgements (Warsaw)
- The WSJ "Trump willing to end war with Hormuz closed" (Odaily 31 Mar 02:49) and the Iranian parliament's transit-fee bill (31 Mar 02:12) go in R0401. The March file excluded both as out of window.
- Trump's address was on 1 Apr at 21:00 ET, which is 2 Apr 03:00 Warsaw, so it goes in R0407. Its announcement (1 Apr) is in R0402.
- The ceasefire: Trump's post was at 8 Apr 00:36 (Odaily 22:36 UTC on 7 Apr), so it goes in R0409, not R0408.
  - The R0408 window ends with Brent ~$105-106 and with "progress in talks" reports (18:37).
  - The 8 Apr morning PAP table (closes 7 Apr; live UST post-ceasefire) is filed in R0409, following the March convention (table of day D in window D).
- Wunsch's WSJ interview was published Mon 6 Apr, but its first sighting in collected sources is TE on 7 Apr at 09:42, so it goes in R0408 (conservative). Hammack's AP interview was in PAP on 7 Apr at 08:25, so also R0408.
- Barkin's remarks ("on Tuesday", 31 Mar) first appear on Odaily on 1 Apr at 14:03, so they go in R0402. Schmid (31 Mar 23:41) goes in R0401.
- Jefferson: his 7 Apr speech was at 17:50 ET, which is 23:50 Warsaw (Fed JSON), so it goes in R0408.
- The FOMC minutes came out on 8 Apr at 20:00, so they go in R0409.
- The 100% pharma tariff was signed on Thu 2 Apr. Its first sighting is the PAP 3 Apr 19:01 digest, so it goes in R0407 either way.
- Putin's Orthodox Easter truce was announced on the evening of 9 Apr (Kremlin), but its first sighting is Odaily on 10 Apr at 02:12, so it goes in R0413.
- Talks:
  - The Islamabad talks started on 11 Apr at 14:26.
  - "No agreement" came on 12 Apr at 02:58-04:00, so it goes in R0413.
  - The blockade announcement was on 12 Apr in the afternoon and evening (PAP weekend digest 20:48), so R0413.
  - The CENTCOM notice was on 13 Apr at 02:24 and the blockade took effect on 13 Apr at 16:00, so both go in R0414.
  - The Brent jump at the Sunday-night open (TE 13 Apr 00:09) goes in R0414.
- Hungarian election:
  - R0413 has only the 15%-count result (Tisza 47.8% vs Fidesz 43.6%), from the PAP weekend digest of 12 Apr at 20:48.
  - The two-thirds projection and Orban's concession first appear on TE (13 Apr 02:28) and PAP (13 Apr 06:20), so they go in R0414. This is conservative: the concession happened on Sunday night.
- Placeholder or official clocks:
  - Eurostat HICP: 31 Mar 11:00.
  - German retail and unemployment block: 31 Mar 09:55.
  - EZ manufacturing PMI: 1 Apr 10:00. EZ unemployment: 11:00. CZ PMI: 09:30.
  - US data: claims and trade 14:30; NFP 3 Apr 14:30; S&P PMIs 15:45; ISM 16:00; CPI and PPI 14:30; UMich 16:00.
  - EZ services PMI: 7 Apr 10:00. Czech flash CPI: 7 Apr 09:00. NBR: 7 Apr 14:00. NY Fed SCE: 7 Apr 17:00.
  - HU CPI: 8 Apr 08:30. EZ retail and PPI: 8 Apr 11:00.
  - German trade and industrial production: 9 Apr 08:00. CZ industrial production: 9 Apr 09:00.
  - German final CPI: 10 Apr 08:00. CZ unemployment: 10 Apr 10:00.
  - CZ current account: 13 Apr 10:00. US existing home sales: 13 Apr 16:00.
  - RO CPI: 14 Apr 08:00. CZ final CPI: 14 Apr 09:00.
  - Lagarde on Bloomberg TV: the 14 Apr 17:06 digest is the upper bound.
- EXCLUDED as out of window:
  - The 15 Apr yield table: it is in yield_tables for R0415 levels only, and its 14 Apr closes are quoted in these notes only.
  - The ECB account of March (16 Apr), the MNB minutes (15 Apr) and the Beige Book (15 Apr).
  - The Warsh hearing itself (21 Apr) and the Moody's Belgium/Lithuania actions (17 Apr, seen on countryeconomy).
  - Web-search snippets about later Lane interviews (May and Sept 2026) were seen and ignored.

## Caveats / conflicts
- Brent contract labels: PAP's late-evening Wall Street pieces carry stale labels such as "WTI kwiecień" and "majowe Brent". Their values are front month (June).
  - The 13 Apr 22:27 line (Brent $91.87, +2.5%) and the 14 Apr 22:14 line ($88.78, -4.5%) do not fit TE (~$98 and ~$95), so they were not used.
  - On 31 Mar PAP quotes the expiring May contract ($116-119) while TE quotes ~$105-108.
- Stale or typo lines in PAP:
  - 8 Apr 14:40 gold/silver line ($4,580/$73.69) is identical to 31 Mar.
  - 14 Apr 18:04 TTF line (€46.20, +5.9%) is identical to 13 Apr.
  - 10 Apr 11:50 Bund "3.12%" against the 3.03% intraday print at 14:49 and the 2.99/3.06% closes.
  - 10 Apr 08:32 DXY "99.92" against ~98.7-98.8 the rest of the day.
  - None of these were used.
- Next FOMC: PAP (6 Apr) says 27-28 Apr, while the March file used 28-29 Apr. cb_decisions shows both. ECB: 29-30 Apr (PAP 30 Mar). BoE: TE says "a move in April", so the meeting date was not verified (30 Apr assumed). CNB next "May 2026" and MNB "Apr 2026" are carried over and unverified.
- The ECB 19 Mar vote ("unanimous"), the CNB 7-0 and the dates of the earlier 2026 NBR meetings are carried from the March file and not re-verified.
- Consensus figures conflict:
  - US CPI y/y: 3.3% (Jin10) vs 3.4% (PAP).
  - UMich one-year expectations: 4.2% (PAP) vs 4.3% (Jin10).
  - NFP: 60k vs 65k. ISM services: 54.8 (PAP) vs 55 (TE).
  - ISM manufacturing: 52.3 (PAP) vs 52.5 (TE).
- TE ECB/BoE pricing statements are qualitative ("at least two", "nearly three") and vary between TE pieces on the same day: on 13 Apr the Bund piece says at least two, the OAT and BTP pieces nearly three. The only hard numbers are PAP 8 Apr (51bp vs 80bp; April 40% vs >70%) and TE 8 Apr (BoE -30bp).
- The "Lagarde and Lane: hawkish response likely" item comes from a TE equity wrap (31 Mar). The underlying speeches and interviews were not retrieved.
- Tables: the 31 Mar UST10 4.32 is live with 1D 4.35. The EU rows in the 6 and 7 Apr tables are stamped 03.04 but are the 2 Apr closes.
- FedWatch figures come from Jin10/Odaily relays, not CME directly. The PAP "56% odds of a cut by year-end" for 8 Apr is reported in hindsight on 9 Apr, so it is in the R0410 rows.

## Gaps
- ECB speakers: the Panetta, Müller, Kazimir and Sleijpen remarks of 31 Mar, Cipollone (1 Apr), Lane, Schnabel, Nagel and de Guindos (13 Apr) and Lagarde's 14 Apr 23:00 speech were not retrieved. Only Villeroy and Lagarde/Lane (via TE), Panetta (PAP 2 Apr), Wunsch (WSJ via TE) and Lagarde on Bloomberg TV (14 Apr) are covered.
- There is no €STR or SONIA curve data and no ECB April-hike odds after 8 Apr.
- BoE: no speaker content in the window (Bailey 14 Apr 18:00 not captured; Taylor and Bailey are only referred to as earlier remarks). No UK CPI in the window: February 3.0% (core 3.2%, 25 Mar) is the latest, and March CPI is due 22 Apr.
- Fed speakers not captured: Goolsbee and Musalem (7 Apr 18:35), Bowman, and Goolsbee, Barkin, Collins and Paulson (14 Apr evening). Barr's 14 Apr speech was on rural communities and not used.
- CNB: no Board decisions in the window and no statements captured. The CNB minutes of the March meeting were not checked.
- MNB: no decision or speakers. The MNB reaction to the election was not captured.
- Romania: there is no NBR vote split, and the core CPI for March is missing.
- Ratings: the countryeconomy scan of 34 European sovereigns shows no rating or outlook change dated 31 Mar-14 Apr. Affirmations without change, and DBRS and Scope, were not checked.
- There are no exchange settlement prices for Brent, TTF or gold, only intraday and late quotes. DXY comes from PAP intraday quotes only.
- US data not captured: retail sales for March (due 15 Apr or later), ISM sub-indices beyond prices and employment, and ECI. The US PCE price data is February (pre-war).
- Euro-area items not captured: Spanish, Italian and French data beyond the HICP flashes, euro-area Q4 GDP revisions, auctions and syndications, and Italian or French budget news.
- Tariffs: only the 100% pharma order (2 Apr), the 50% threat on suppliers of arms to Iran (8 Apr), Bessent's Section 122 status (14 Apr), the EU steel safeguard deal and China's warning. No new Section 232 actions were found.
