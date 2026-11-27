# Global PIT facts 14-28 May 2026: working notes
Windows (Warsaw publication time, CEST throughout): R0515 = 14 May; R0518 = 15-17 May; R0519 = 18 May; R0520 = 19 May; R0521 = 20 May; R0522 = 21 May; R0525 = 22-24 May; R0526 = 25 May (Whit Monday in DE/HU, Memorial Day in the US, UK bank holiday); R0527 = 26 May; R0528 = 27 May; R0529 = 28 May.
Output: facts.json (183 facts + 14 fed_pricing rows), built by build/make_json.py from build/f_MMDD.py (facts per window), build/extra.py (pricing, CB decisions, CPI) and build/digest.py. The schema is the same as the April facts_global_2.json:
- facts: published / window_report_date / topic / text / src. fed_pricing rows: published / text / src / window_report_date.
- fed_pricing_by_R, ecb_pricing, boe_pricing: dicts keyed by R, each a short text naming its source date.
- cb_decisions: a list of {bank, date, decision, rate, vote, published, note, src}. It includes the last pre-window Fed, ECB, BoE, BoJ, MNB and CNB decisions so stances are known. Filter on published <= the info cut-off. Notes contain only what was known when the decision was published.
- cpi: a list of {country, period, value, core, published, note, src}. It covers EA, DE, US (CPI and PCE), UK, CZ, HU and RO, including the pre-window April prints with their original release times.
- digest (<= 450 characters) and glob (<= 60 characters, leading space): dicts keyed by R.
The build script checks that every cited PAP, Odaily and TE item was downloaded and flags window mismatches between a fact's time and its source's time (none remain). It also enforces the length limits.

## Big picture (as sourced, no hindsight)
The 8 April ceasefire nominally holds, but the double blockade continues: the US blockades Iranian ports, and Iran controls Hormuz traffic by permission and fees. Over the fortnight the story ran from stalemate and strike threats to a near-deal.
- 14 May: the Trump-Xi summit agreed that Hormuz must reopen. US April CPI of 3.8% (published 12 May) had already pushed out Fed cuts.
- 15-19 May: Trump rejected Iran's 14-point plan and said 'we don't need the Strait open'. Israel and the Pentagon prepared to resume strikes. On 18 May Trump called off a strike planned for 19 May at the request of Saudi Arabia, Qatar and the UAE.
- 20 May: Trump said the talks were in their 'final stage'. Brent fell 5.6%.
- 21 May: Iran's leader ordered enriched uranium kept at home, and Iran and Oman discussed tolls. Late that day a 'final draft' was reported.
- 23-25 May: Trump said a deal was 'largely negotiated': a 60-day ceasefire extension, a phased Hormuz reopening and frozen funds, with nuclear issues deferred. He kept the blockade and told his envoys not to rush.
- 26-28 May: US 'self-defence' strikes in Hormozgan and IRGC fire on ships and aircraft. On 28 May at 16:15 Axios reported that negotiators had agreed a 60-day MoU, which still awaited Trump's approval.

Markets:
- Brent July: ~$105 → $109-111 (15-19 May) → $105 (20 May) → ~$103 (22 May) → ~$97 (25 May) → ~$100 (26 May) → ~$95 (27-28 May).
- Core yields: the global bond rout peaked on 19 May.
  - UST10 at ~4.7% intraday, a 16-month high; UST30 at 5.2%, the highest since 2007.
  - Bund 10Y at ~3.2% intraday (3.19% close), the highest since 2011.
  - Gilt 10Y at ~5.2% on 15 May, the highest since 2008, amplified by the Labour leadership crisis (Streeting resigned; Burnham's path to challenge Starmer).
  - Yields then fell back with oil: Bund 2.95-2.99% and UST10 ~4.47% by 25-28 May.
- CB pricing:
  - ECB: three hikes (~90% for June) on 14-18 May → two hikes plus 60% for a third (22 May) → two (25 May) → DFR ~2.6% by December (27 May) → ~65bp (28 May). A June 11 hike stays the base case (Schnabel: even with a peace deal).
  - BoE: nearly three hikes → two after weak jobs data and the 2.8% April CPI → ~40bp (27 May) → one fully priced (28 May).
  - Fed: no 2026 cut → FedWatch 28% (14 May) → ~40% for a December hike (15-19 May) → a 25bp hike by end-2026 fully priced (22 May, Jin10) → ~50% by December (27-28 May).
- Fed leadership: Powell's chair term ended on 15 May (chair pro tem; Bowman and Miran dissented on the open-ended term). Warsh was sworn in on 22 May. Miran resigned effective at Warsh's swearing-in.
- Data:
  - FOMC minutes (20 May): a majority see firming as likely if inflation persists.
  - ECB account (28 May): April was a close call.
  - Euro area: April HICP confirmed at 3.0% (core 2.2%). The flash composite PMI fell to 47.5 and the Commission cut 2026 GDP to 0.9%.
  - UK: CPI 2.8%, unemployment 5.0%, composite PMI 48.5.
  - US: April PCE 3.8% (core 3.3%) and Q1 GDP 1.6% (second estimate); UMich sentiment fell to a record-low 44.8 with one-year expectations at 4.8%.
- CEE: the NBR held at 6.50% (15 May) and the MNB at 6.25% (26 May; Varga sees room to ease). HU10 fell from 5.71% to 5.42% and CZ10 from 4.95-5.04% to 4.85%.
- Ratings: S&P revised Bulgaria's outlook to positive (BBB+) on 15 May. No other European sovereign actions were found.

## Access (as of 27 Nov 2026)
- **strefainwestorow listing** (30 items per page): p337-340 = 14 May; p335-337 = 15 May; p335 = 17 May (weekend digest); p332-335 = 18 May; p330-332 = 19 May; p326-330 = 20 May; p322-326 = 21 May; p319-322 = 22 May; p319 = 23-24 May; p317-319 = 25 May; p315-317 = 26 May; p312-315 = 27 May; p309-312 = 28 May.
  - The index of p306-345 is dl/list/all.tsv. 237 macro/global articles are in dl/art, their text in txt/ and their times in dl/list/idx.tsv (scripts/ext.py).
  - The 20 May yield table was missing from the listing (page shift) and was fetched by URL.
  - scripts/day.py prints a day's digest global lines (17:0x, then only new lines at 21:0x); scripts/mk2.py prints the market lines; scripts/tabsum.py and tab.py print the yield tables.
  - The weekend digests (17 May 19:42, 24 May 21:16) have no section headers, so read them with grep.
- **Odaily newsflash.** IDs 481150-485250 cover 13 May 22:00 to 29 May CEST, but only 2,407 of 4,101 IDs exist; the rest are real 404s (ID gaps, verified by re-fetch).
  - dl/od/all.tsv holds (id, CEST, title, body); JSON-LD datePublished is UTC, +2h applied. scripts/odsel.py filters macro and geopolitics items.
  - Coverage of ECB and BoE speakers is nil, and Fed-speaker coverage is thin before 21 May.
- **Trading Economics.** IDs 550400-554850 (13 May 17:31 to 29 May) are in dl/te/all.tsv (id, CEST, headline, body, url), via scripts/teget.sh and teparse.py, with +2h applied.
  - scripts/tesel.py filters relevant headlines and scripts/pricing.py extracts CB-pricing sentences per day.
  - Pre-window lookups (for cb_decisions and cpi only) were fetched by ID: 546540-546720 (30 Apr: ECB, BoE, EZ flash HICP), 548340-548480 and 548740-548900 (6-7 May: the CNB on 7 May), 549000-549200 (8 May: HU CPI) and 549650-550399 (11-13 May: US CPI, CZ and RO CPI).
- **Official sources:**
  - Fed JSON (ne-speeches.json, ne-press.json) for times in ET.
  - FOMC minutes (fomcminutes20260429.htm); the wording was verified against the official text.
  - Fed press releases: Miran resignation (other20260514b), Powell pro tem and the Bowman/Miran statement (other20260515a), Warsh oath (other20260522a).
  - Waller speech (waller20260522a).
  - BoE April MPS page (8-1 vote).
  - countryeconomy.com/ratings for 32 European countries; only rows dated 13-29 May were read.

## Key series (dates = close date; PAP/Bloomberg morning table, EU rows = previous close)
- **Bund 10Y:** 13 May 3.10, 14 May 3.04, 15 May 3.17, 18 May 3.15, 19 May 3.19, 20 May 3.10, 21 May 3.10, 22 May 3.04, 25 May 2.95, 26 May 2.98, 27 May 2.99. For 28 May, PAP had 2.96 at 18:07 and the 29 May table also shows 2.96 (levels only).
  - TE intraday: 3.13% on 15 May ('highest since May 2011'), ~3.2% on 18-19 May, below 3% on 25 May.
- **Schatz:** 2.71, 2.65, 2.74, 2.71, 2.76, 2.66, 2.69, 2.64, 2.54, 2.59, 2.59 (28 May: 2.56).
- **Gilt 10Y:** 5.07, 4.99, 5.17, 5.10, 5.13, 4.99, 4.97, 4.90, 4.90 (UK holiday), 4.88, 4.86 (28 May: 4.81). **Gilt 2Y:** 4.49, 4.43, 4.55, 4.48, 4.51, 4.37, 4.38, 4.33, 4.33, 4.30, 4.27 (4.24).
  - TE: 5.15-5.2% intraday on 15-18 May; the 30Y hit 5.82% (highest since 1998) on 15 May.
- **Spreads vs Bund (10Y):**
  - OAT: 63, 62, 65, 63, 64, 62, 63, 63, 61, 61, 61 (61).
  - BTP: 75, 73, 78, 76, 78, 73, 74, 73, 70, 72, 72 (72).
  - Spain: 42-44.
  - PL10-Bund: 282bp (13 May) → 285-287 (15-19 May) → 282 (25 May) → 279 (27 May).
- **UST10, PAP live at 06:3x:** 4.46 (14 May), 4.53 (15 May, 07:42 unstamped), 4.62, 4.60, 4.66, 4.59, 4.56, 4.56 (25 May table = 22 May close, Memorial Day), 4.50, 4.47, 4.53; 4.44 in the 29 May table.
  - Intraday: 4.6% (15 May, TE), ~4.7-4.76% (19 May, TE; PAP 18:02 4.67), 4.58% after the 20 May fall.
  - UST30: 5.177-5.198% (19 May).
- **UST2:** 3.97, 4.06, 4.10, 4.06, 4.10, 4.06, 4.08, 4.12, 4.05, 4.02, 4.07 (4.02).
- **JGB10:** 2.62 → 2.79 (21 May) → 2.69-2.71 (25 May) → 2.65 (29 May table). JGB20 3.78% (19 May, highest since 1996).
- **CEE 10Y:** CZ10 4.95 → 5.04 (19 May) → 4.85 (27 May); HU10 5.71 → 5.50 (14 May) → 5.67 (18 May) → 5.42 (27 May).
- **Brent July (PAP ~18:00 European close unless stated):**
  - 14 May: 104.97 (late 106.55, labelled 'June').
  - 15 May: 109.7; weekly +8% (TE).
  - 18 May: 111.08 (TE ~108 late).
  - 19 May: 110.43.
  - 20 May: 105.72; settle 105.02 (-5.6%).
  - 21 May: 107.88; 104.24 at 22:20; the 22 May morning '+2.0% to 104.63' implies a ~102.6 settle.
  - 22 May: 103.4; 103.77 late.
  - 25 May: 97.58 (briefly below 94); a ~96.1 settle is implied by 26 May '+2.48% to 98.52'.
  - 26 May: 100.44; 99.54 late.
  - 27 May: 95.82; 95.00 late.
  - 28 May: 94.81; 94.27 late.
  - No exchange settlement prices were collected.
- **TTF:** EUR46.9 (14 May) → >50 (15 May, TE) → 50.2 (18 May) → 52.0 (19 May) → 48.9 (20 May) → 49.6 (21 May) → ~45.5 (25 May, TE) → [26 May PAP 41.75, flagged] → 46.2 (27 May) → 46.9 (28 May).
  - EU storage: 36.9% vs a 50.7% five-year average (21 May); 38.8% vs 52.8% (28 May).
- **ECB EUR/USD fixings:** 1.1702, 1.1628, 1.1648, 1.1620, 1.1600, 1.1599, 1.1595, 1.1643, 1.1634, 1.1637, 1.1617. EUR/USD low ~1.159-1.161 (18-21 May); a one-month or six-week low per TE.
- **DXY:** 98.5-98.6 (14 May) → ~99 (15 May) → 99.4, a six-week high (19 May) → 99.1 (20 May) → retreat on deal hopes (25 May).
- **USD/JPY:** 157.95-158.1 (14 May) → 158.7 (15 May) → 159.1 (19 May) → 159.2-159.5 (21-28 May), near the late-April/early-May intervention levels.
- **Gold:** $4,693-4,711 (14 May) → 4,561, then below 4,500 late (15 May) → 4,543 (18 May) → 4,508 (19 May) → 4,532 (20 May) → 4,510 (21 May) → 4,505 (26 May) → 4,430-4,437 (27 May) → 4,422-4,501 (28 May). Silver: $85-88 → ~$74-77.

## Timing judgements
- **Morning tables.** Each table sits in the window of its publication date, following the March and April convention. The 15 May table (07:42, unstamped; EU rows = 14 May closes) is in R0518. The 25 May table (US rows also 22 May closes because of Memorial Day) is in R0526. The 29 May table is levels-only for R0529 and is quoted in these notes only.
- **Fed (Fed JSON times are ET, +6h).**
  - Miran resignation: 14 May 20:00 → R0515.
  - Powell pro tem: 15 May 23:00 → R0518.
  - FOMC minutes: 20 May 20:00 → R0521.
  - Waller speech: 22 May 16:00 → R0525.
  - Warsh oath: the ceremony was first seen on Odaily on 22 May at 18:10; the Fed release was 22:15 → R0525.
  - Jefferson: 27 May 20:00 ET = 28 May 02:00 Warsaw → R0529 (Odaily 02:36). Cook (27 May 21:55, on AI) was not used.
- **Trump's strike postponement.** It was posted late on 18 May ET, first seen on Odaily on 18 May at 23:16 → R0519, with TE 22:22 the same evening. The 'two to three days' detail (19 May 01:56) goes in R0520.
- **CENTCOM 'self-defence' strikes (Mon 25 May ET).** First seen on Odaily on 26 May at 02:12 → R0527, not R0526.
- **Weekend items.** These are stamped with their Odaily times:
  - FT 60-day extension: 23 May 16:33.
  - Axios 'close': 23 May 22:38.
  - Tasnim disputed clauses: 24 May 10:28.
  - Trump 'no rush': 24 May 16:13.
  - All of these are in R0525. The PAP weekend digest (24 May 21:16) confirms the blockade 'until a deal'.
- **Rating actions.** S&P Bulgaria (Fri 15 May) has a countryeconomy row only, with a 23:00 placeholder → R0518. No TE or PAP coverage.
- **ECB speakers.**
  - Kazaks: TE 14 May 12:45 → R0515.
  - Rehn: Jin10 21 May 07:01 → R0522.
  - Schnabel's Reuters interview: TE 26 May 10:02, first sighting → R0527.
  - Villeroy ('Tuesday' 26 May): TE 27 May 08:13 → R0528.
- **Data facts** use official release times, as in March and April. Placeholders:
  - UK: GDP 14 May 08:00; labour 19 May 08:00; CPI 20 May 08:00; retail and public finances 22 May 08:00.
  - Euro area: HICP final 20 May 11:00; trade 19 May 11:00; PMIs 21 May 10:00; ESI 28 May 11:00.
  - Germany: PPI 20 May 08:00; Ifo 22 May 10:00; GfK and GDP 22 May 08:00.
  - US: retail sales and claims 14 May 14:30; Empire State and IP 15 May 14:30/15:15; claims, Philly Fed and starts 21 May 14:30; S&P PMIs 21 May 15:45; UMich 22 May 16:00; Conference Board 26 May 16:00; PCE, GDP and durables 28 May 14:30.
  - NBR 15 May: TE 14:11, an upper bound. MNB 26 May 14:00. ECB account 28 May 13:30.
- **Cross-window CPI.** US April CPI (12 May), the German final (12 May), the CZ final and RO (13 May) and HU (8 May) appear only in the cpi list, with their original release times. The ECB, BoE and CNB decisions and the April EZ flash HICP (30 Apr - 7 May) appear only in cb_decisions and cpi.

## Caveats / conflicts
- **PAP stale or bad lines (not used):**
  - The 25 May 18:06 TTF and gold/silver line ('TTF -5.6% to EUR48.88', 'gold +0.5% to $4,532') is identical to 20 May.
  - The 26 May 18:06 TTF EUR41.75 (+3.8%) conflicts with TE (~EUR45.5 on 25 May) and with PAP's own 27 May print (EUR46.22, +2.6%).
  - The 28 May 18:07 'Bund rises 3bp to 2.96%' is inconsistent; TE says the Bund reversed lower to ~2.96%. The level is used, not the sign.
- **Brent:**
  - The 14 May 22:16 'June Brent $106.55 (+0.87%)' carries a stale contract label.
  - The 21 May 22:20 print ($104.24) differs from the settle implied by 22 May morning (~$102.6).
  - TE's 18 May 14:16 'Brent near $102' conflicts with PAP ($108.8-111.1) and with TE's own 22:22 (~$108). Probably a glitch; not used.
  - On 25-26 May the WTI % changes are against Friday because of Memorial Day, so they are not comparable with Brent.
- **ECB pricing:** TE on 15 May says 'three hikes fully priced' while PAP (Reuters) says 'more than two, the first in June'. Both are quoted. All later pricing is TE text only (no €STR or OIS levels).
- **Fed pricing:** the measures differ.
  - FedWatch: 28% for a hike by year-end on 14 May; ~40% for December on 15 and 19-20 May; ~40% by January.
  - Jin10 futures and swaps: >50% by January 2027 (15 May), >80% by end-2026 (19 May), fully priced (22 May).
  - TE: ~50% for December (20-21 and 28 May), ~55% by October (22 May).
- **UST10 peak:** TE has 4.76% intraday on 19 May while PAP's close-of-Europe was 4.67%. The digest says '~4.7%'.
- **Bulgaria:** the countryeconomy page now also shows a later row (not read or used beyond its date). Only the 15 May row was used.
- **Musalem (28 May):** the Jin10/Odaily translation ('higher real rates should be addressed through rate hike policies') is ambiguous and is quoted as relayed.

## Gaps
- **ECB:** no Lagarde remarks in the window; there is no Odaily ECB coverage, and the TE speaker mentions found are Kazaks, Rehn, Schnabel, Villeroy and Moulin.
  - Lane (28 May 02:00), Cipollone and Schnabel (28 May) were not captured.
  - No €STR, OIS or June-hike probability after 27 May except '~65bp' (28 May).
  - The official ECB account page was not fetched; the TE summary was used.
- **BoE:** no speeches captured (Bailey's 29 May appearance is outside the windows). Pricing is TE text only. The next MPC date (June) was not confirmed in window sources.
- **Fed:** FedWatch probabilities for the June meeting itself were not found. Speakers before 21 May (Hammack, Logan, Daly, Bostic and others) were not captured, as Odaily coverage is thin and there are no PAP stand-alone pieces. Logan (27 May) was not captured.
- **US data not captured:** April PPI details (13 May, pre-window), existing and new home sales, and the Q1 GDP price index.
- **CNB:** the vote on 7 May and the CZ Q1 GDP revision (29 May, outside) were not retrieved. **NBR:** no vote split or core CPI. **MNB:** no vote.
- **Ratings:** only countryeconomy rows were checked (no agency press releases, no DBRS or Scope). No actions were found for France, Italy, Spain, the UK, Czechia, Hungary or Romania. The other agent covers Fitch and Moody's reviews of Poland, if any.
- **Tariffs:** covered only by the EU-US deal legislation (provisional 20 May, member states 27 May, EP vote in June), Greer on China, Mexico and Canada, the China 'preliminary' deals, and the G7 focus on China. Nothing on Section 122 (150 days from 24 Feb) or Section 232 was found.
- **Prices:** no exchange settlements for Brent, TTF or gold. The Brent July contract expires at end-May, so front-month labels in late-May PAP pieces may shift.
