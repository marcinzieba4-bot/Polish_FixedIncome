# Global PIT facts 13-26 Feb 2026: working notes
Windows (CET publication): R0216 = 13-15 Feb; R0217 = 16 Feb; R0218 = 17 Feb; R0219 = 18 Feb; R0220 = 19 Feb; R0223 = 20-22 Feb; R0224 = 23 Feb; R0225 = 24 Feb; R0226 = 25 Feb; R0227 = 26 Feb.
Output: facts.json (125 facts + 15 fed_pricing rows), built by build/make_json.py. The schema is identical to 2026-01-H2 facts_global.json (facts: published / window_report_date / topic / text / src; fed_pricing: published / text / src). The window is set from the CET publication date.

## Access
- strefainwestorow listing (as of 26 Nov 2026): 13 Feb = p489-491, 16 Feb p486-489, 19 Feb p479-482, 23 Feb p475-477, 26 Feb p468-470 (`?page=N`). Weekends are thin: only the weekend "Skrót wiadomości" summaries. Index: dl/list/all.tsv (682 urls); 383 macro articles in dl/art; text in txt/ (scripts/ext.py).
- PAP yield table (~06:35) carries the PREVIOUS day's EU/CEE closes (date-stamped from 16 Feb on) and live 06:3x US/JP values. The 13 Feb table has no stamps. scripts/tab.py parses it.
- Odaily newsflash IDs 468480-469860 cover 12-27 Feb (titles in dl/od/titles.tsv; UTC+8, so CET = -7h). Full bodies: scripts/odfull.py reads the "initData" JSON (datePublished is UTC, converted to CET). Some bodies are "$22" chunk references; read them from the `22:T` push chunk.
- Trading Economics news pages: the datetime stamp is UTC (UK CPI story at 07:11 = 07:00 GMT release + 11 min). The sidebar shows LATER (Nov 2026) items. They were ignored. Only the article's own metaDesc/body was used.
- countryeconomy.com/ratings/<country> gives rating-change histories. 25 sovereigns were scanned for changes dated 12-27 Feb.

## Key series (dates = close date unless stated)
- Bund 10Y (PAP table): 12 Feb 2.78, 13 Feb 2.76, 16 Feb 2.75, 17 Feb 2.74, 18 Feb 2.74, 19 Feb 2.74, 20 Feb 2.74, 23 Feb 2.71, 24 Feb 2.71, 25 Feb 2.71. TE intraday: 2.725 low 16 Feb, 2.70 on 24 Feb (lowest since late Nov). 26 Feb close is not available inside the window.
- UST 10Y: 13 Feb 4.05 (Fri close; 4.11 pre-CPI morning), 17 Feb ~4.06, 18 Feb ~4.09-4.10, 19 Feb ~4.07, 20 Feb 4.08, 23 Feb ~4.03, 24 Feb ~4.03-4.04, 25 Feb 4.04. UST2: 3.47 (13 Feb am) -> 3.40 intraday low post-CPI -> 3.39-3.48 range afterwards.
- Gilt 10Y: 4.45 (12 Feb) -> 4.31 (23-24 Feb) -> 4.32 (25 Feb). Gilt 2Y 3.60 -> 3.58.
- Spreads vs Bund: OAT 59 -> 55bp; BTP 60-61bp flat; Spain 37 -> 40-41bp.
- CEE 10Y: CZ 4.43 -> 4.36; HU 6.55 -> 6.40 (6.45 on 16 Feb; 6.48 after the MNB cut; 6.40 on 25 Feb).
- JGB 10Y: 2.22 (13 Feb) -> 2.11 (20/23 Feb) -> 2.16 (26 Feb am).
- Brent (front = Apr from mid-Feb; PAP intraday ~18:00 / ~22:00 CET): 13 Feb 67.6/67.5; 16 Feb 68.5; 17 Feb 67.1/67.3; 18 Feb 69.5/70.6; 19 Feb 71.8/71.4; 20 Feb 71.6/71.6; 23 Feb 71.8/71.6; 24 Feb 71.3/71.2; 25 Feb 70.7/70.9; 26 Feb 72.0/70.9 (intraday 69.7-72.0). Settlements IMPLIED from the next-morning % change in PAP oil articles (derived, not exchange data): 13 Feb ~67.75, 16 Feb ~68.65, 17 Feb ~67.4, 18 Feb ~70.35, 19 Feb ~71.65, 20 Feb ~71.75, 23 Feb ~71.5, 24 Feb ~70.75, 25 Feb ~70.85. 18 Feb (+4.3%) was the biggest daily gain since Oct 2025. 20 Feb was a 6-month high.
- DXY: 97.13 (13 Feb am) -> 96.88 (post-CPI) -> 97.07 (16 Feb) -> 97.31 (17 Feb) -> 97.48 (18 Feb) -> 97.89 (19 Feb) -> 97.82 (20 Feb) -> 97.4-97.7 (23 Feb). No DXY prints for 24-26 Feb; EUR/USD 1.1769 (24 Feb 16:17), 1.1804 (25 Feb), 1.1789 (26 Feb ~18:00). ECB fixings: 1.1862 (13 Feb) ... 1.1753 (19 Feb low) ... 1.1814 (26 Feb).
- Gold: <5,000 on 12-13 Feb (sharp drop on 12 Feb, before the window) -> >5,000 after CPI (13 Feb 15:14) -> 4,897 (17 Feb, -2.9%) -> 5,016 (18 Feb) -> >5,040 (20 Feb) -> 5,232 (23 Feb, +3%, tariff/trade tension) -> 5,127 intraday dip (24 Feb) -> 5,192-5,205 (25-26 Feb am). No new record in the windows (the record was 29 Jan, ~5,568).

## Timing judgements (CET)
- US Jan CPI was released 13 Feb 14:30 (delayed calendar), so it falls in R0216.
- FOMC minutes 18 Feb 20:00 -> R0219. Odaily stamps 20:01-20:10. Timiraos note 19 Feb 03:35 -> R0220.
- FT Lagarde early-exit story: reported "on Wednesday" 18 Feb (Euronews 09:27 CET) -> R0219, not R0218.
- SCOTUS IEEPA ruling 20 Feb (10:00 ET session; 16:00 CET is approximate; Roll Call posted 11:04 ET) -> R0223. Trump's 15% post came Sat 21 Feb (Odaily 22 Feb 02:57 CET) -> R0223.
- State of the Union 24 Feb 21:00 ET = 25 Feb 03:00 CET -> R0226.
- Bailey at the Treasury Committee (24 Feb hearing) is filed by the dated article (Professional Adviser, 25 Feb) -> R0226. This is the conservative placement; the hearing itself was public on 24 Feb (R0225).
- Lagarde "Face the Nation" (aired Sunday 22 Feb) is filed by the PAP report of 24 Feb 18:52 -> R0225 (conservative).
- The WSJ "limited strike" report (US 19 Feb) is filed under PAP 20 Feb -> R0223 (conservative). Trump's "I'm considering it" quote was on 20 Feb.
- The French no-confidence votes (Wed 25 Feb) are filed under PAP 26 Feb 17:01 -> R0227 (conservative).
- Trump's "prefer agreement over war" post: Odaily 24 Feb 00:00 CET -> R0225. WSJ Section 232 report: 23 Feb 23:59 CET -> R0224.
- FedWatch snapshot 26 Feb 00:05 CET -> R0227; 26 Feb 23:20 CET -> R0227.
- EXCLUDED as out of window: WSJ story that the Fed is challenging the Powell subpoenas (27 Feb 01:22 CET); Fitch on Poland and the Portugal/Slovenia rating changes (27 Feb); TE Bund 27 Feb note; Jan PPI (27 Feb); later Warsh hearing (April); Lagarde's actual resignation (Oct); later CNB/ECB/Fed hikes. None of these were used.
- Placeholder clocks: CNB minutes 13 Feb 12:00; Estonia/Moody's 13 Feb 23:00; Bailey 25 Feb 12:00; SCOTUS 16:00.

## Caveats / conflicts
- US Q4 GDP consensus: 2.8% (PAP) vs 3.0% (Jin10). Core PCE Dec: "in line" at 3.0% per PAP vs 2.9% expected per Jin10. Both are recorded in separate facts.
- US claims 26 Feb consensus: 217k (PAP) vs 215k (Jin10).
- Jin10 calls the committee handling Warsh the "Senate Finance Committee". It is Senate Banking (Tillis sits on it). The Jin10 minutes item names the Jan dissenters as "Waller and Mester". This was corrected to Waller and Miran (per the 28 Jan FOMC statement in the H2 file).
- FedWatch figures come from Odaily/Jin10 relays, not CME directly. The 19 Feb "6% March cut" comes from a Sinclair (CBS Austin) story whose 2:40 PM stamp is assumed to be ET.
- ECB pricing comes from Trading Economics only: 30% chance of a cut by Dec (13 Feb) vs ~40% (17 Feb). No €STR-curve numbers were collected.
- The Estonia/Moody's 13 Feb entry is from a third-party table only (outlook Stable). The action type (affirmation vs outlook change) is unverified.
- PAP Brent contract labels are inconsistent ("marcowe"/"kwietniowe"); values are front-month (Apr after the Mar expiry).

## Gaps
- US retail sales and US PPI: no release inside the windows (Dec retail sales came out before 13 Feb; Jan PPI on 27 Feb per the PAP calendar). No US CPI beyond 13 Feb. Q4 GDP and Dec PCE (20 Feb) are covered.
- Fed chair: only the 13 Feb Bessent/Tillis items. No formal Senate transmittal or hearing date was found inside the windows.
- Fed speakers not captured: Bowman (16/19/26 Feb), Daly (17 Feb), Kashkari (19 Feb), Logan (20 Feb), Musalem/Barkin (25 Feb) content.
- ECB: no Schnabel (18 Feb), Nagel, Lane, Cipollone or Villeroy policy quotes. Lagarde NABE (23 Feb) content not retrieved.
- UK: Bailey hearing quote only (Pill, Greene and Taylor not captured); no BoE swap pricing number beyond "almost fully priced by April".
- CNB: only the 13 Feb minutes. A Zamrazilová interview (MF Dnes/iDnes "Rozstřel", 20 Feb) exists but its text was not retrieved. No CZ CPI inside the windows (Jan CPI came out before 13 Feb).
- HU: MNB vote split not public in-window (the minutes come later). HU Jan CPI (2.1%) was released before the window and is only cited as background.
- No euro-area sovereign rating action found 13-26 Feb besides Estonia/Moody's (13 Feb). Portugal and Slovenia changes on 27 Feb are out of window.
- DXY not collected for 24-26 Feb (EUR/USD used instead). No exchange settlement prices for Brent (implied only).
