# PIT notes for 2 Jan 2026 close (report dated Mon 5 Jan 2026)
Rule: levels <= close 2 Jan 2026; facts published <= 4 Jan 2026. Later docs used ONLY for 2 Jan closes/fixings.

## Access tips (new)
- gpwbenchmark: use host WITHOUT www (www returns empty reply to curl). Annual 2026 files not yet published.
  WIBOR rolling table: https://gpwbenchmark.pl/dane-opoznione ; POLSTR/WIRON: https://gpwbenchmark.pl/dane_opoznione
  (pages also show later dates; extract the 2026-01-02 row ONLY)
- strefainwestorow listing: https://strefainwestorow.pl/wiadomosci?page=N ; early Jan 2026 = pages 544-547 (as of 26 Nov 2026)
- Erste/Santander Codziennik 5 Jan 2026 (created 5 Jan 13:53 UTC) market tables headed "02.01.2026":
  https://www.erste.pl/regulation_file_server/time20260105150318/download?id=168959&lang=pl_PL  (use tables only; commentary is post-cutoff)
- Millennium daily260102/260105 -> 404. DB Poland daily260102pol/260105pol -> 404. BOS weekly 2 Jan (bosbank.pl) -> Cloudflare 403.

## 1. Fixings 2 Jan 2026
- WIBOR (GPW Benchmark dane-opoznione row 2026-01-02): ON 3.85, SW 3.95, 1M 4.04, 3M 3.97, 6M 3.85, 1Y 3.76 (TN/2W '-').
  WIBID: ON 3.55, SW 3.75, 1M 3.84, 3M 3.77, 6M 3.65. Cross-check Erste 5 Jan table "Stawki WIBOR" (02.01.2026): ON 3.85, SW 3.95, 1M 4.04, 3M 3.97, 6M 3.85 -> match.
- POLSTR index date 2026-01-02: 3.634; compound 1M 3.66671, 3M 4.03237, 6M 4.43047; POLSTR CI 124.42518849.
  WIRON 2026-01-02: 3.332; compound 1M 3.27485, 3M 3.64134, 6M 4.03422. (index date T published T+1 -> 5 Jan; UNVERIFIED-TIMING of publication; value reflects 2 Jan)
  (ref: POLSTR 31.12.2025 = 2.619 (year-end), 30.12 = 3.528; WIRON 31.12 = 2.277)
- EURIBOR 2 Jan (Bundesbank BBIG1): 1M 1.953, 3M 2.029, 6M 2.105, 12M 2.245 (31 Dec: 1.939/2.026/2.107/2.243)
- PRIBOR 2 Jan (CNB year.txt?year=2026): O/N 3.50, 1W 3.51, 2W 3.53, 1M 3.53, 3M 3.52, 6M 3.54, 1Y 3.52
- BUBOR: NO fixing on 2 Jan 2026 (bubor2.xls sheet 2026 starts after 2 Jan; HU rest day). Latest <=2 Jan: 31 Dec 2025: O/N 6.50, 3M 6.47, 6M 6.39, 12M 6.37.

## 2. PLN IRS / FRA (Erste Codziennik 5 Jan 2026, table "Rynek stopy procentowej 02.01.2026"; footnote: bid, interbank, end of day; src LSEG Datastream)
- IRS PL: 1Y 3.60, 2Y 3.54, 3Y 3.59, 4Y 3.67, 5Y 3.75, 8Y 4.02, 10Y 4.19 (7Y NOT FOUND). Change col (bp): 0,+1,+1,+1,+2,+2,+1 (baseline presumably prior session).
- US IRS: 1Y 3.69, 2Y 3.58, 3Y 3.61, 4Y 3.64, 5Y 3.71, 8Y 3.92, 10Y 4.04 ; EZ IRS: 1Y 2.17, 2Y 2.27, 3Y 2.39, 4Y 2.50, 5Y 2.60, 8Y 2.84, 10Y 2.97
- FRA: 1x4 3.79, 3x6 3.56, 6x9 3.36, 9x12 3.33, 3x9 3.50, 6x12 3.36
- CDS 5Y USD PL 60bp; PL 10Y spread vs Bund 234bp (HU 109/402).
- Bonds in same table: OK0128 3.89 (+12?!), PS0131 4.63, DS1035 5.19 -> inconsistent w/ PAP 16:18 (3.80/4.56/5.16) -> treat as suspect.
- FX prev session 02.01.2026 (Erste): EURPLN min 4.2080 max 4.2215 open 4.2157 close 4.2085 fixing 4.2156; USDPLN close 3.5858 fixing 3.5963; EURUSD close 1.1736.

## 3. PAP/Bloomberg yield table
- 2 Jan 2026 07:46 https://strefainwestorow.pl/wiadomosci/20260102/rentownosci-obligacji-wybranych-panstw-tabela : column "02.01.2026" but current = 1D for all rows -> = last closes before 2 Jan (31 Dec where traded; HU/DE/IT etc look = 30 Dec). Per-row dates not stamped. PL 3.85/4.58/5.17.
- 5 Jan 2026 06:36 https://strefainwestorow.pl/wiadomosci/20260105/rentownosci-obligacji-wybranych-panstw-tabela : per-row date stamps.
  02.01.2026 rows (current col): PL 2Y 3.83, 5Y 4.58, 10Y 5.17 ; CZ 3.74/4.12/4.65 ; TR 33.72/30.70/26.93 ; IE 2.05/2.52/3.06 ; IT 2.24/2.89/3.61 ; PT 2.11/2.52/3.20 ; ES 2.29/2.68/3.34 ; DE 2.14/2.48/2.90 ; FR 2.34/2.89/3.61 ; UK 3.74/3.96/4.54
  HU rows stamped 30.12.2025: 3Y 6.24, 5Y 6.42, 10Y 6.79
  JP/US rows stamped 06:32 (= 5 Jan live, POST-CUTOFF, do not use current col). US 1D col (prior close, presumably 2 Jan): 3.47/3.74/4.19. JP 1D = 1.18/1.55/2.07 (Japan closed 1-2 Jan -> = 30 Dec close).
  PL 5D col 3.90/4.61/5.18; 1M col 3.96/4.56/5.18.

## 4. Catalyst closes 2 Jan 2026 (biznesradar notowania-historyczne; cols open/max/min/close/vol/turnover)
- FPC0229: 2 Jan close 104.05 (vol 186); prev 29.12 104.12
- FPC0630: 2 Jan close 90.50 (vol 279; range 90.50-91.11); prev 30.12 90.70
- FPC0231: 2 Jan close 105.00 (vol 1 -> thin); prev trade 10.12 104.00
- FPC0733: 2 Jan close 84.00 (vol 24; open 83.40); prev 30.12 83.04
- FPC0235: 2 Jan close 105.30 (vol 472); prev 30.12 105.39

## 5. FX
- NBP fixing 2 Jan 2026 table 001/A/NBP/2026: EURPLN 4.2156, USDPLN 3.5963, CHF 4.5314, GBP 4.8391, CZK 0.1743, HUF(100) 1.0987 (api.nbp.pl + PAP 11:50)
- PAP 2 Jan 16:18: EURPLN 4.2106, USDPLN 3.5879, EURUSD 1.1735; OK0128 3.80, PS0131 4.56, DS1035 5.16 (2Y -3bp, 5Y -2bp, 10Y -2bp on day). 09:12: OK0128 3.80, PS0131 4.55, DS1035 5.15.
  URL https://strefainwestorow.pl/wiadomosci/20260102/dzien-na-fxfi-eurpln-w-okolicach-421-w-styczniu-mozliwe-oslabienie-zlotego

## 6. Facts 1-4 Jan 2026
- PL mfg PMI Dec 48.5 (Nov 49.1), S&P Global, 2 Jan 09:00. 8th month <50; first m/m drop since June (PKO, PAP 2 Jan 16:44: "zgodny z oczekiwaniami"). Pre-release consensus 49.3 (Erste Codziennik 23 Dec calendar, "rynek"), Santander f'cast 49.6.
- EZ mfg PMI final 48.8 (flash 49.2; Nov 49.6); DE 47.0 (flash 47.7); FR 50.7; UK 50.6 (flash 51.2); US S&P mfg final 51.8 (Nov 52.2). (PAP skrót 2 Jan 17:00/21:00)
- NBP Survey of Professional Forecasters (PAP 2 Jan 10:43; survey 4-18 Dec, 25 experts): CPI 2026 2.6% (2.2-3.0), 2027 2.5%; GDP 2026 3.6%, 2027 3.0%; avg ref rate 2026 3.69% (3.39-3.95), 2027 3.42%; EURPLN 4.25 (2026), 4.27 (2027); Brent 62-64.
  https://strefainwestorow.pl/wiadomosci/20260102/w-26-inflacja-w-polsce-wyniesie-26-proc-w-27-cpi-na-poziomie-25-proc-ankieta
- BOS weekly (PAP 2 Jan 13:38): CPI to fall to ~2.0% y/y early 2026 (Q1 path ~2.0% vs ~2.5% before); electricity bill +4.7% m/m Jan; basket change/COICOP 2018 uncertainty; flash Jan CPI mid-Feb on 2025 weights.
- DM BOS Rogalski (PAP 2 Jan 16:44): EURPLN may test 4.2360 trendline; PLN weakening in Jan possible; Fed: Jan cut odds ~15%, full 25bp priced only by June; April >70%; FOMC minutes 30 Dec raised uncertainty; SCOTUS tariff ruling likely in Jan; US payrolls 9 Jan.
- MoF (PAP 2 Jan): "Minister Finansów i Gospodarki" issued T-bonds to raise ARP share capital (non-market). No 9 Jan auction series announced by 4 Jan (NOT FOUND).
- MPC member comments 1-4 Jan: NOT FOUND in PAP feed.
- Bank research 2-4 Jan: PKO (PMI comment only). ING/Pekao/Millennium/Santander/mBank: NOT FOUND (first 2026 dailies on 5 Jan = post-cutoff).
- Geopolitics: 3 Jan US strike on Venezuela, Maduro captured & flown to NY (PAP 3-4 Jan). Ukraine peace meetings announced for 3, 6, 7 Jan (Zelensky, PAP 2 Jan). Trump delayed furniture tariff hikes to 2027 (31 Dec order, PAP 2 Jan). Bulgaria joined euro 1 Jan.
- Other PL 2 Jan: NBP Nov: new mortgage lending 7.398bn; avg mortgage rate 6.41% (Oct 6.51); corporate loans 14.823bn. EU funds 2026: 180bn PLN incl. 120bn KPO (Pełczyńska-Nałęcz).
