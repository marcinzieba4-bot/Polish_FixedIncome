# Global PIT facts 30 Jan - 12 Feb 2026: working notes
Windows (CET publication): R0202 = 30 Jan-1 Feb; R0203 = 2 Feb; R0204 = 3 Feb; R0205 = 4 Feb; R0206 = 5 Feb; R0209 = 6-8 Feb; R0210 = 9 Feb; R0211 = 10 Feb; R0212 = 11 Feb; R0213 = 12 Feb.
Output: facts.json (141 facts + 17 fed_pricing rows), built by build/make_json.py (same schema as 2026-01-H2 facts_global.json: facts{published, window_report_date, topic, text, src}, fed_pricing{published, text, src}). The window is set from the CET publication date by the script.

## Access
- strefainwestorow listing as of 26 Nov 2026: 30 Jan = p508-510, 2 Feb ~p505-506, 6 Feb = p500, 10-11 Feb = p495, 13 Feb = p490. Index: dl/list/all.tsv (date, url, title); macro subset dl/list/sel.tsv; idx.tsv adds article timestamps. Article time is in `<time class="pr-1" datetime="HH:MM">`. Text in txt/ (scripts/ext.py); scripts/sk.py prints only global sections of the "Skrót wiadomości" digests (17:00 is a subset of 21:00).
- PAP yield table: scripts/tab2.py. From 2 Feb the rows carry date stamps (EU/CEE = previous close, US/JP = live 06:3x). The 30 Jan and 13 Feb tables are not stamped.
- Odaily newsflash IDs 466400-468600 cover 30 Jan 00:00 - 13 Feb 06:00 CET. dl/od/all.tsv holds (id, CET time, title, body). Timestamps are converted from the page's UTC `dateTime` (+1h). Gap: no items between 12 Feb 17:48 and 13 Feb 01:11 CET. scripts/odm.py filters macro titles.
- Other sources: AGI (Italy rating 22:21), CNB statement, ING THINK (CNB, BoE, HU CPI, Rates Spark), Kitco/Reuters (ECB pricing 19:44), BusinessDay/Reuters (BoE vote), Eurostat (HICP flash components), CZSO flash, MNB minutes PDF (header: published 14:00 11 Feb), Al Jazeera (France budget), OeBFA (S&P Austria).

## Key series (dates = close date unless stated)
- Bund 10Y (PAP table): 29 Jan 2.84, 30 Jan 2.84, 2 Feb 2.87, 3 Feb 2.89 (high), 4 Feb 2.86, 5 Feb 2.84, 6 Feb 2.84, 9 Feb 2.84, 10 Feb 2.81, 11 Feb 2.79, 12 Feb ~2.78 (PAP 18:09). Schatz 2.07-2.12.
- UST 10Y (PAP evening): 30 Jan 4.24-4.25, 2 Feb 4.27, 3 Feb 4.28, 4 Feb 4.27, 5 Feb 4.21 (close ~4.18), 6 Feb 4.22, 9 Feb 4.20, 10 Feb 4.15 (close 4.14 after weak retail), 11 Feb 4.20 post-NFP then 4.16-4.17, 12 Feb 4.13. UST2 (table, live): 3.50-3.57 until 5 Feb, 3.47 (6 Feb), 3.45 (11 Feb a.m.), 3.51 (12 Feb a.m. after NFP).
- Spreads: OAT-Bund 58-61bp, BTP-Bund 60-63bp, Spain 36-38bp, all stable. Gilt 10Y 4.51-4.56 (peak 4.56 on 5 Feb, UK politics), 4.48 on 11 Feb. UK2 3.72 -> 3.66 on 5 Feb (dovish BoE) -> 3.62.
- CEE: CZ2 3.41 (4 Feb) -> 3.49 (5 Feb, CNB) -> 3.56 (9 Feb) -> 3.46-3.47 (10-11 Feb). HU10 6.45-6.56.
- JGB10: 2.23-2.28 (2.28 on 9 Feb a.m. after the election, 2.23 by 12 Feb). USD/JPY: 157.1 (6 Feb ECB fix) -> 156.7 (9 Feb a.m.) -> 153.3 (11 Feb) -> 152.8 (12 Feb a.m.).
- Brent: Mar contract expired 30 Jan (~$70.7-70.8). Front month April from 2 Feb: 65.8 (2 Feb, -5%), 67.0-68.2 (3 Feb), 67.5-68.6 (4 Feb), 67.5 (5 Feb), 67.9-68.5 (6 Feb), 69.0 (9 Feb), 68.7-69.2 (10 Feb), 69.7-70.3 (11 Feb), 67.65-67.9 (12 Feb). PAP's evening Wall Street pieces often label Brent "marcowe" (Mar); the values match April and are treated as front-month April.
- DXY: 96.4 -> 96.9 (30 Jan, +0.8%, biggest daily gain since July) -> 97.5 (2 Feb) -> 97.8 (5 Feb) -> 97.0 (9 Feb) -> 96.8 (10 Feb) -> 97.1 post-NFP -> 96.9. EUR/USD ECB fixes: 1.1919, 1.1840, 1.1801, 1.1820, 1.1798, 1.1794, 1.1886, 1.1894, 1.1900, 1.1874.
- Gold: ~5,400-5,450 early 30 Jan -> close 4,880 (-9.25%, low 4,682) -> below 4,410 on 2 Feb (Asia) -> +6% on 3 Feb (~4,940-4,980) -> >5,000 on 4 Feb early -> ~4,890 (5 Feb) -> 4,955 (6 Feb) -> 5,039-5,080 (9 Feb) -> 5,045 (10 Feb) -> 5,052-5,099 (11 Feb) -> 4,907 on 12 Feb (-3.3% intraday, 17:25). Silver: -26% on 30 Jan (85.3), ~72-77 on 5-6 Feb, ~83 on 11 Feb, 77 on 12 Feb.

## Timing judgements (CET)
- Warsh: Odaily reports from 30 Jan 03:22 (the administration preparing to name him) and Trump's post at 12:49 (Odaily) / 13:05 (PAP). All of it falls in R0202. The earlier run excluded 30 Jan by design, so there is no overlap.
- The Cuba oil-tariff EO and the Canada aircraft tariff threat (29 Jan US time) were first seen at 30 Jan 01:06-01:18 CET -> R0202. They are not in the earlier file.
- S&P Italy: AGI 22:21 30 Jan -> R0202. S&P Austria affirmation on Fri 6 Feb: time unknown (22:00 is a placeholder) -> R0209.
- France budget adoption: no-confidence votes on the evening of Mon 2 Feb (19:30 is a placeholder) -> R0203.
- US shutdown: began Sat 31 Jan; House passed the bill 3 Feb (US afternoon, PAP 21:01) -> R0204; Trump signed the same evening (in the 4 Feb digest).
- Payrolls were postponed from 6 Feb to Wed 11 Feb (14:30 CET) -> R0212. US CPI moved to Fri 13 Feb (14:30) -> OUTSIDE all windows. Only the consensus is used (headline/core +0.3% m/m, 2.5% y/y; PAP 9 Feb).
- JOLTS (Dec) was published 5 Feb 16:00 (delayed from 3 Feb) -> R0206.
- The Iran tariff EO and the removal of India's 25% Russian-oil tariff were signed Fri 6 Feb. The first PAP mention is the weekend digest (8 Feb 19:53) -> R0209 either way.
- Japan election: NHK exit poll on Sun 8 Feb (PAP 19:53) -> R0209. The official 315-seat count (MIC) appeared 10 Feb -> R0211. It was deliberately kept out of the 8 Feb fact.
- WSJ's second-carrier report: Odaily 11 Feb 23:24 -> R0212. PAP carried it on 12 Feb.
- HU CPI: KSH 12 Feb 08:30; the ING snap time is not stamped (09:00 is a placeholder). The ING CNB note (5 Feb, 17:00), the ING BoE snap (5 Feb, 17:00) and the ING Rates Spark (5 Feb, 10:00) are placeholders within the correct day.
- CZ flash CPI: CZSO 5 Feb 09:00 -> R0206. The final print on 13 Feb is out of window and not used.
- CNB minutes (published later) and the ECB February account (5 Mar) are out of window and not used. The SCOTUS IEEPA ruling had not been issued in any window; only "ruling pending" (Odaily 11 Feb 23:23) is used.

## Caveats / conflicts
- PAP stale lines: the gold/silver lines in the 4 Feb 18:04, 9 Feb 18:09 and 12 Feb 18:09 European-close pieces repeat earlier days' numbers (28 Jan, 6 Feb, 11 Feb). The DXY in 12 Feb 18:09 repeats 14:41. These lines are not used; Odaily spot quotes are used instead. PAP 2 Feb 18:07 printed Bund "2.67%" (typo; the table close is 2.87).
- ADP consensus: 45k (Dow Jones via PAP) vs 48k (Jin10). JOLTS consensus: 7.2m (Reuters) vs 7.25m (Bloomberg). Payrolls consensus: 65k (PAP release line) vs ~70k (PAP week-ahead, Jin10). HU CPI consensus: 2.4% (Trading Economics), with ING at 2.0%. CZ CPI consensus: 1.7% (Trading Economics), while ING/analysts called 1.6% "in line".
- EZ HICP: Eurostat compares Jan 1.7% with Dec 2.0% (new COICOP 2018 basis); PAP wrote "wobec 1.9%". PAP's preview consensus was 1.8%, but its release line says 1.7%.
- Jin10 name garbling: "Milan" = Miran, and 466613 calls him "Michelle Bowman"; "Mester" (10 Feb) = Cleveland Fed's Hammack; "Mousalem" = Musalem. Facts are attributed with a note.
- The Odaily 5 Feb claim of "UK 10Y at 4.577%, highest since Nov 2020" is factually doubtful and not used.
- FedWatch 30 Jan 13:37 and 1 Feb 23:05 show the same March odds (15.3/84.7). The weekend print may be stale.

## Gaps
- No FedWatch print found for 5-10 Feb. PAP only says the "first cut is in June" (9-10 Feb).
- Fed speakers not found: Bowman (3 Feb), Jefferson (6 Feb), Waller (9 Feb), Bostic (9 Feb), Hammack comes only via a mislabeled Jin10 item. Powell remarks were not specifically searched.
- ECB speakers: only Lagarde (5 Feb) plus the PAP-reported Kocher/Villeroy euro comments (pre-2 Feb). Lane (9 Feb), Schnabel (11 Feb "Made in Europe", structural) and Cipollone have no rate content. There are no €STR curve numbers beyond Reuters/ING probabilities.
- BoE post-decision market probabilities (March cut odds) are not quantified. ING gives the 6m-fwd OIS at 3.32%; the pre-decision March odds were ~20% (ING) or "little chance" (Reuters).
- CZ/HU: no CZ Q4 GDP flash or HU Q4 GDP (13 Feb, out of window). There are no MNB speaker comments, and the CNB minutes are out of window.
- US: no Q4 ECI or control-group retail sales detail was collected. The CPI print (13 Feb) is out of window. No exchange settlement prices were collected for Brent or gold (intraday PAP/Odaily quotes only).
- Euro-area sovereign: besides S&P Italy (positive outlook) and S&P Austria (affirm), no other EA rating actions were found for the Friday 6 Feb slot. The French budget was adopted 2 Feb. No new EGB auction/syndication results were collected.
