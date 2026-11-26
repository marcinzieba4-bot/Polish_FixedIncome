# PIT facts 13-26 Feb 2026 (report dates 16-27 Feb) - working notes
Output: facts.json (same folder; keys mof_ops, new_series, bgk, facts, gpwb, meta - same schema as the 2026-01-H2 run).
Builder: scripts/build.py (+ scripts/gpwb_parse.py, skrot.py, dump.py, paras.py, db.py, db2.py).
Raw downloads: dl/ (list, art, txt = PAP via strefainwestorow; gov; gpwb; res/{pko,mil,erste,ca,db,bps,bnp}).
Windows: R16=13-15 Feb, R17=16, R18=17, R19=18, R20=19, R23=20-22, R24=23, R25=24, R26=25, R27=26 Feb.
Timestamps: PAP article times exact; PAP "Skrot wiadomosci" 17:01/21:xx = upper bounds; PDF CreationDate (local +01) = upper bound; Erste = upload time in URL.

## Access tips (26 Nov 2026)
- strefainwestorow listing: 13 Feb = p489-491, 20 Feb = p477-479, 26 Feb = p468-470. 684 slugs 13-26 Feb; 133 macro ones fetched.
- MoF debt communiques: https://www.gov.pl/web/finanse/komunikaty-dlug?page=4&size=10 (16 Feb FX funds; next is 27 Feb March plan). Feb plan on page 5.
- MoF db (OH.xlsm, BS.bin) copied from the earlier run (downloaded 26 Nov). Used only 18 and 25 Feb rows; totals match PAP exactly.
- GPWB: plain curl now gets "Empty reply"; works with a full browser UA plus Accept/Accept-Language headers.
- PKO Dziennik: listing offsets 185-200 at centrumanaliz.pkobp.pl/aktualnosci?offset=N. Erste archive page still works. CA MAKROmapa 23 Feb id 35042 (probe by content-type, since the site soft-404s with 200). BPS 20260216/20260223 OK. DB wa260216pol and wa260224pol (no 23 Feb file).
- Blocked: bgk.pl (Cloudflare 403). BNP Paribas fileserver: in-window items are brokerage/product docs, no macro notes found.
- Web searches leaked post-window outcomes (Fitch 27 Feb, March MPC). These were ignored and are NOT used anywhere.

## Key findings
- MoF 18 Feb auction (offer 16 Feb: 8-13bn vs plan 7-12; Czarnecki said dealer demand drove the raise). Sold 13,000.4 vs 22,117.4 (cover 1.70); additional sale 2,121.0.
  - OK0128 360/1405 @93.754 (3.400%); PS0730 2596/3110 @101.551 (4.101%); PS0131 2230/3490 @101.240 (4.212%); NZ0331 2276/6879 @96.350.
  - DS1034 624.6/984.6 @101.400 (4.792%); DS1035 4328.3/4923.3 @100.500 (4.927%); IZ0836 585.5/1325.5 @93.934 (2.667% real).
  - Additional sale: PS0730 175, NZ0331 605.74, DS1035 1217.26, IZ0836 123. Financing reached ~36%.
- MoF 25 Feb auction (offer 23 Feb: 8-12bn vs plan 7-12). Sold 11,890.5 vs 15,637.5 (cover 1.32, lowest demand of 2026); additional sale 596.8.
  - OK0128 27/27 @93.780 (3.42%); WZ0930 1237/2327 @98.193; PS0131 2650/3706 @101.142 (4.233%); NZ0331 2585/3613 @96.350.
  - DS0432 1806.5/2035.5 @85.725 (4.447%); DS1035 3585/3929 @100.350 (4.947%).
  - Additional sale: NZ0331 75.4, DS0432 91.8, DS1035 429.6. Financing reached ~38%.
- No new series (PS0730 and IZ0836 were re-openings). No switch, buyback, T-bill or foreign issue in the windows.
  - The MoF ends WZ (WIBOR6M) floaters from March, per the 20 Feb communique / Bloomberg. That date comes via PKO 23 Feb.
  - YTD regular-auction supply is ~82.4bn, versus the 75-100bn Q1 plan.
- GPWB (published 25 Feb, PDF created 12:13 CET, Last-Modified 18:22 CET; effective 27 Feb; holdings as of 24 Feb):
  - No entries or exits in any index.
  - B1Y3Y: mod dur 1.74%, YTM 3.37%. B1Y4Y: mod dur 2.50%, YTM 3.65%. TBSP: 18 bonds, mod dur 3.78%, YTM 4.00%, value 906.6bn.
  - Units reconcile with settlements through 20 Feb. The file is original (CreationDate = ModDate).
- Data, actual vs PAP consensus:
  - CPI flash 2.2 vs 1.9 (m/m 0.6 vs 0.6).
  - Wages 6.1 vs 7.2; employment -0.8 vs -0.6.
  - Industrial output -1.5 vs +2.0; PPI -2.6 vs -2.3; construction -12.8 vs -5.0.
  - Retail 4.4 vs 3.1; unemployment 6.0.
  - M3 10.0 vs ~10.4; C/A Dec -1,698 vs -1,080.
  - Sentiment: BWUK -9.1, ESI 101.3 (down from 103.2), EC inflation expectations 29.4, HICP 2.5.
- MPC:
  - Dabrowski: April safer, 50% odds of a March cut (PKO 18 Feb); 3.5% target (25 Feb).
  - Zarzecki (20 Feb): a 25bp cut is justified, 50bp is not.
  - Glapinski (24 Feb): projection shows CPI near target in 2026-27.
  - Litwiniuk (by 25 Feb): March probable, further cuts toward 3.5%.
  - Jan voting record (26 Feb): Tyrowicz's +75bp motion was rejected.
- Banks: all expect a 25bp cut on 4 Mar.
  - Millennium: March plus Q2. ING: 3.25% or lower. BOS: 3.25%. BPS: 3.75% after March.
  - mBank (Sadoch) mentions 50bp talk. Fitch is expected unchanged (Santander, Millennium, CA, PKO, ING).
- Fiscal:
  - Budget deficit: Jan 3.7bn; 2025 275.6bn vs 288.8bn plan.
  - Fiscal Council warns on debt. SAFE: Sejm 13 Feb, Senate amendments 19 Feb, signing planned 2H March; a presidential veto risk is debated.
  - BGK FPC 19 Feb: 1,877 vs 2,738, plus 333.5 additional sale.

## Not used / outside the windows (do not use)
- Q4 GDP flash (12 Feb), Jan MPC minutes (6 Feb), 11 Feb auction, 6 Feb T-bill auction.
- MPC remarks by Kotecki, Wnorowski and Maslowska from 10-12 Feb (appear only as recaps).
- March supply plan (27 Feb), Fitch review (27 Feb), and anything later.
- Jan core CPI: not published in the windows.
