# PIT facts 30 Jan - 12 Feb 2026 (report dates 2-13 Feb) - working notes
Output: facts.json (same folder; keys mof_ops, new_series, bgk, facts, gpwb, meta - same schema as the 2026-01-H2 run). Builder: scripts/build.py.
Raw downloads: dl/list (strefainwestorow p486-512), dl/art + dl/txt (577 PAP articles 30 Jan-12 Feb), dl/gov (MoF pages + Feb plan PDF), dl/res/{pko,mil,erste,ca,db,bps}.
Windows: R2Feb=30 Jan-1 Feb, R3=2, R4=3, R5=4, R6=5, R9=6-8, R10=9, R11=10, R12=11, R13=12 Feb.
Timestamps: PAP article times exact; PAP "Skrot" 17:01/17:03 = upper bound; PDF CreationDate UTC +1h; Erste = upload time in URL.

## Access tips (26 Nov 2026)
- strefainwestorow listing: 30 Jan = p508-510, 12 Feb = p491-493 (about 2 pages/day; ~60 slugs/day). All 577 slugs fetched.
- MoF debt communiques: gov.pl/web/finanse/komunikaty-dlug?page=5&size=10 (30 Jan plan, 2 Feb JPY mandate, 6 Feb JPY pricing). Feb plan PDF = attachment be1ae193.
- MoF db (OH.xlsm, BS.bin) reused from agent_jan2_plfacts/dl/gov/db. Used ONLY rows 2026021101-15 (11 Feb) and 2026020601-02 (6 Feb T-bill). Later rows (18 Feb etc.) seen, NOT used.
- PKO Dziennik pages: centrumanaliz.pkobp.pl/aktualnosci/dziennik-ekonomiczny-<slug>; offsets 200/205 cover 30 Jan-12 Feb.
- Erste ids 169016-169049 (archive page from earlier run). Note: titles in archive are shifted by one item.
- CA MAKROmapa: makromapa-02022026_34812.pdf, makromapa-09022026_34888.pdf. DB: only wa260209pol (wa260202pol missing). BPS: only 20260209.
- ING Think snaps (3, 4, 5 Feb) fetched via WebFetch. IMF PR 26/030 page dated 3 Feb.
- Blocked: bgk.pl (403), bosbank.pl (403), nbp.pl (bot check).
- WARNING: web searches on MPC topics return March-2026 outcomes; none used.

## Key findings
- 30 Jan: GUS 2025 GDP 3.6% (cons 3.6 Parkiet / 3.5 Millennium); private cons 3.7, investment 4.2. MoF Feb plan: auctions 11/18/25 Feb, each 7-12bn; no switch; T-bill 6 Feb 33w 2-4bn. Budget accounts ~180bn est. Non-resident SPW 174.3bn (+4.6). BGK FWA0931 1bn = private placement.
- 2 Feb: PMI 48.8 vs 49.2 cons. PAP survey 10/18 hold. Parkiet 9 hold / 9 cut (mean 3.88). PKO and CA expected a cut; ING, Millennium, Santander a hold. JPY mandate (Daiwa, Nomura, SMBC).
- 3 Feb: Pekao: FRA 9x12 at 3.35% implies terminal 3.25-3.50. IMF Article IV (dated 3 Feb US) placed in the 4 Feb window.
- 4 Feb: MPC hold at 4.00% (dep 3.50, lomb 4.50), ~14:40; statement 16:00 says CPI may fall in Q1 and stay consistent with target. FRA +3-5bp, SPW +1bp. Fitch (Trajkovic): outlooks last 1-2 years; at most one cut in 2026; GG deficit ~7%.
- 5 Feb: Glapinski: a March cut "yes" if the projection shows nothing worrying; terminal 3.5% "possible"; return of inflation to target is durable. SPW -3/-5bp, pricing unchanged.
- 6 Feb: JPY 211.6bn priced (3Y 1.88%, 5Y 2.22%, 10Y 2.90%, 20Y 3.65%; settles 13 Feb). T-bill 33w: 2,567.2 vs 4,377 at 3.529%, plus 205 additional. Jan minutes: one member said rates are too low. MoF Q4 GDP estimate 4.1%. Budget accounts 183.4bn. Reserves EUR 246.76bn.
- 9 Feb: Q4 wages 8.5% (above expectations); pension indexation 5.3%. Unemployment 6.0%. MoF offer for 11 Feb: 8-12bn, 8 series (IZ0831, DS1033, WS0437 added). Kotecki and Wnorowski (via PKO 9 Feb): March cut likely, terminal 3.50-3.75%.
- 10 Feb: Litwiniuk (Bloomberg): 2x25bp incl. March, or 50bp in April; terminal 3.5%. BGK FPC offer.
- 11 Feb auction (db per-series, confirmed by totals): 11,871.7 sold vs 25,839.0 demand (cover 2.18); additional sale 1,379.0.
  - OK0128: 0 sold (demand 40).
  - WZ0930: 725 @97.913.
  - PS0131: 3,836 @100.870 (4.298%).
  - NZ0331: 571 vs 7,867.8 demand.
  - IZ0831: 805 @97.287 (real yield 2.276%).
  - DS1033: 1,401 @107.970 (4.732%).
  - DS1035: 3,926 @99.685 (5.035%).
  - WS0437: 607.7 @98.710 (5.148%).
  - Financing about 33%. Wnorowski (DGP): 3.5% realistic. Zarzecki (Reuters): March plausible; 3.25% "bold". Bloomberg: State Tribunal case against Glapinski dropped (first mention Erste 11 Feb).
- 12 Feb: Q4 GDP flash 4.0% (cons 4.0; Millennium cons 3.9), +1.0% q/q. Kotecki (PAP): March and April -25bp each, terminal 3.50%. Maslowska: March cut, terminal 3.50%. 10Y SPW below 5%. BGK FPC: 3,394 vs 6,346, plus 754.6 additional. SAFE bill through committees; FIZB may issue bonds.

## Not used / outside the window (do not use)
- January flash CPI (13 Feb), Dec BoP (13 Feb), PKO/Erste dailies of 13 Feb and later, MoF db rows from 18 Feb on, MoF FX communique (16 Feb).
- Search snippets about the March MPC outcome.
