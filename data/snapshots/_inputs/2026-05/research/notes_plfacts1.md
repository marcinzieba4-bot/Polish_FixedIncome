# PIT facts 30 Apr - 13 May 2026 (report dates 4-14 May) - working notes
Output: facts.json (same folder). Keys: mof_ops, new_series, bgk, facts, gpwb, wz_coupons, digest, mpc, data, meta. Schema as in 2026-04 facts_poland_2.json.
Builder: scripts/build.py. Helpers: scripts/listparse.py, fetch.sh, h2t.py (strefainwestorow HTML -> text), skrot2.py / skrot3.py (Skrot digests, Poland filter), govlist.py / govpage.py (gov.pl lists and pages), oh_rows.py (MoF bond DB -> work/oh_may.json), pdfmeta.py, pko_ext.py, mil_ext.py.
Raw downloads:
- dl/list: listing pages p334-368. dl/art + dl/txt: 706 PAP items dated 30 Apr-13 May. dl/index.json, dl/titles.txt.
- dl/gov: komunikaty-dlug p1-3, May plan page and PDF. dl/db: Obligacje_Hurtowe.xlsm, Bony_Skarbowe.xls.
- dl/res/{pko,mil,erste}: 9 dailies each, 30 Apr-13 May. dl/web: S&P date checks (Interia, gov.pl EN).
- work/: extracted texts.
Windows: R4 May = 30 Apr-3 May, R5 = 4 May, R6 = 5, R7 = 6, R8 = 7, R11 = 8-10, R12 = 11, R13 = 12, R14 = 13 May.
Timestamps:
- PAP article times are exact. PAP Skrot 17:0x/21:xx = upper bound.
- PDF CreationDate (local, +02) = upper bound. gov.pl = date only.
- S&P: Interia datePublished 8 May 22:16 = upper bound.
- CEST throughout.

## Access tips (27 Nov 2026)
- strefainwestorow listing `https://strefainwestorow.pl/wiadomosci?page=N`. Page ranges:
  - 30 Apr = p360-363; 1-3 May = p359; 4 May = p357-359; 5 May = p355-357; 6 May = p352-355.
  - 7 May = p349-352; 8-10 May = p347-349; 11 May = p345-347; 12 May = p342-345; 13 May = p340-342.
  - Plain curl with xargs -P 12 works. p355 failed once (re-fetch).
  - Items per day: 72 on 4 May ... 99 on 7 May. 9 May has no items; 10 May has only the weekend Skrot.
- The PAP feed lacks several bond items:
  - no PMI article, no T-bill result (8 May), no MoF offer item on 11 May, no Kotecki 13 May article;
  - no BGK result items. The Skrot digests carry most of them (MoF plan, T-bill offer, 13 May results, BGK offer).
- MoF `gov.pl/web/finanse/komunikaty-dlug?page=3&size=10` holds the 30 Apr May plan; the next items are dated 15 May (outside).
  - Page 1 = Oct-Nov, page 2 = Jun-Sep. These later titles were seen while paging and NOT used.
  - May plan PDF: attachment f5e4e8fc..., CreationDate 30 Apr 08:11.
- MoF DBs (both linked from gov.pl/web/finanse/bony-i-obligacje-hurtowe1):
  - Obligacje_Hurtowe.xlsm: attachment d12c559c..., Last-Modified 25 Nov 2026. The 13 May rows match PAP same day exactly.
  - Bony_Skarbowe.xls: attachment 31ac439a-542c-47f8-a292-ccb1ec763145, Last-Modified 18 Nov 2026; holds the 8 May rows.
- PKO: `centrumanaliz.pkobp.pl/aktualnosci?offset=145` (28 Apr-5 May), 140 (6-12 May), 135 (13-19 May). Each item page links the cdn-netpr PDF.
- Millennium: `daily2605DD` exists for all window days.
- Erste archive ids: 169390 (30 Apr) ... 169422 (13 May).
  - The title text shown before each link in the archive HTML belongs to the item above.
  - The FRA table is on page 2 (pdftotext -layout needed for 5-8 May).
- S&P: biznes.pap.pl is Incapsula-blocked. Interia JSON-LD gives timestamps (S&P item 8 May 22:16; Domanski 9 May 10:15). gov.pl/web/finance EN page is dated 10 May.
- WARNING: web searches leaked post-window rating actions (S&P outlook change Nov 2026, Moody's downgrade Sep 2026, a DBRS downgrade report). They were ignored; searches were used only to date the S&P/DBRS items and to look for a dated T-bill result (none found).

## Key findings
- MoF May plan (30 Apr; R4 May):
  - Sales 13 May (6-12bn), 21 May (7-13bn), 27 May (6-12bn), all in OK0129/NZ0331/PS0731/DS0436/NZ0936 (+IZ/other). No switch.
  - T-bill 8 May: 46-week, 3-6bn.
  - Drop: budget accounts ~184bn at end-April.
  - PKO: the 19-37bn of sales is above its expected ~29bn (which included a switch).
  - Retail coupons: ROR 4.00, DOR 4.15, TOS 4.40, COI 4.75, EDO 5.35.
- T-bill 8 May (PL0000006227, maturity 30 Mar 2027):
  - Offer 3-6bn (Skrot 7 May 17:06, R8 May).
  - Sold 3,660m on 3,660m demand at 96.42 = 4.151% (10 Apr: 3.95%). Additional sale 549m (offer 719m).
  - The only dated source is Millennium 11 May 08:44, so the result is put in R12 May (strict).
- 13 May sale (settles 15 May):
  - Offer 6-11bn incl. PS0130 (added). Scheduled 11 May 15:00; first dated mention Millennium 12 May 08:39, so put in R13 May (strict).
  - Result: sold 11,006.33m on 13,727.33m demand (cover 1.25), plus 848m additional of OK0129 the same day.
  - OK0129 1,155 @87.95 (4.868%); PS0130 1,300 @99.901 (5.018%); NZ0331 2,425 @94.72; PS0731 4,019 @93.942 (5.360%); DS0436 2,107.33 @95.50 (5.854%); NZ0936 0 bids.
  - PAP 16:57: yields +6bp. R14 May.
- New series OK0129: PL0000119178, zero, matures 25 Jan 2029. First sale 13 May; 2,003m outstanding after 13 May. ISIN and maturity from the DB only.
- Other MoF items:
  - Financing ~49% at end-April (PAP 11 May).
  - Non-residents -5.0bn to 190.0bn in March (12.2%). SPW turnover March 2,430.8bn. EU funds March EUR 3.956bn.
  - Retail bonds April 5,609.1m.
  - No foreign issue, FX-account, coupon notice or budget-execution release in the windows.
- MPC:
  - Hold 6 May (14:57). Statement 16:00: core probably up in April; wait-and-see; risk wording unchanged.
  - June meeting moved to 1-2 June.
  - Glapinski 7 May: hike probability up since April, cut very unlikely; action if CPI breaches 3.5% with persistent forecasts, or if projections show an unavoidable breach; core rising, demand and wages subdued; gold 595t.
  - April minutes (8 May 14:00): the war lifts CPI short term but weaker activity may curb medium-term pressure; some members flagged the deficit.
  - Kotecki (8 May): forecasts keep CPI in target. Kotecki (13 May): no cuts before mid-2027, hike talk possible from July.
  - Zarzecki (12 May): pause to end-2026; hikes need current and projected CPI > 3.5%.
  - Wnorowski (PKO 12 May): no need to hike now; risk up.
  - Litwiniuk (13 May): hike more likely than cut by end-2026, no July decision.
  - Dabrowski (30 Apr): cut chances fell.
- Ratings:
  - S&P affirmed A-/A-2 FC, A/A-1 LC, stable, on 8 May (~22:16; R11 May). No consolidation expected before the 2027 election; net debt near 70% by 2029.
  - DBRS confirmed A, negative trend (PAP 11 May 08:47; scheduled 8 May after 22:00) - put in R12 May (strict).
  - No Fitch or Moody's sovereign action. Fitch actions on Polish banks only, 6-13 May.
- Data, actual vs consensus:
  - Flash CPI April 3.2% / 0.6% m/m vs PAP 3.0 / 0.4. Fuels -1.8% m/m, food +0.6% m/m.
  - PMI 48.8 vs 48.6-48.7 (no PAP consensus).
  - Registered unemployment 6.0% vs 6.0%.
  - Q1 wages +6.7% (Q4 8.5%). Reserves EUR 254.77bn.
  - NBP 2025 loss 35.74bn. Bank-sector Q1 profit 9.427bn. Firms' CPI expectations (NBP Quick Monitoring) up sharply.
  - Q1 GDP flash is due 14 May and CPI final 15 May (both outside).
- Fiscal:
  - CPN fuel package: Motyka 4 May (two weeks if extended); ME recommendation 10 May; Motyka 12 May (extension within hours).
  - The MoF extended VAT 8% and the excise cut to 31 May (Dz.U. 13 May); the statutory basis runs to 30 June.
  - Windfall-tax details within 7 days (Domanski 13 May).
  - SAFE loan signed 8 May (EUR 43.7bn; ~20bn advance; Domanski: savings up to 80bn).
  - Fiscal Council (12 May): the WZM shock scenario is too optimistic.
  - IMF Georgieva (13 May): cut the deficit.
  - BGK-funds-under-MoF law signed (Millennium 12 May).
- BGK:
  - 29 Apr FPC additional sale 129.5m (Millennium 30 Apr; R4 May).
  - 14 May FPC offer: FPC0229/0231/0332/0235, min 500m (Skrot 12 May; R13 May). Results outside.
  - No FWSZ auction.
- GPWB: the 28 Apr communique took effect 30 Apr (PS0731 into TBSP, 18 bonds; WS0429 into B1Y3Y; WZ1126 out of BWZ). Nothing new; next 27/29 May.
- Market pricing (PAP and bank dailies):
  - 30 Apr: up to 75bp of hikes in 12M (PKO).
  - 5 May: 25bp in 2026 + 50bp in 2027 (PKO).
  - 6 May: FRAs price the reference rate at 4.5%+ in early 2027 (PKO). 75bp within 10M priced before the 6 May rally (ING).
  - 7 May: ~2 hikes by year-end vs >3 early in the week (XTB).
  - 8 May: PKO sees a July hike possible if Hormuz stays shut.
  - Erste FRA 9x12 (bid, close C): 4.53 (29 Apr), 4.57 (30 Apr), 4.62 (5 May), 4.40 (6 May), 4.41 (7 May), 4.46 (8 May), 4.56 (11 May), 4.66 (12 May). WIBOR 3M 3.84-3.85.
  - 10Y path (PAP/PKO): near late-March highs 30 Apr -> ~5.78 (5 May am) -> ~-20bp on 6 May -> slightly lower 7-8 May -> +6-11bp 11 May -> +3-8bp 12 May -> +6bp intraday 13 May.

## Not used / outside the windows
- 14 May and later:
  - Q1 GDP flash (14 May); BGK FPC results; PKO/Erste/Millennium dailies of 14 May+. Post-window titles in the PKO and Erste archive lists were seen while locating files and are not used.
  - 15 May: April CPI final, March C/A, MoF April FX account and 2025 market-transactions communiques, budget data after April, Scope review.
  - 20 May: WZ coupon notice and CHF issue communiques (titles only). 21/27 May auctions; the June MPC.
- MoF DB rows after 13 May exist and were not read.
- Pre-window context, not re-used as new facts:
  - 28 Apr items: April sales, WZM 2026-30, the GPWB communique.
  - March voting record (27 Apr); mid-April Wnorowski and Zarzecki interviews (re-quoted in PAP 4 May).
- Web-search snippets on later rating actions (S&P Nov 2026, Moody's Sep 2026, a DBRS downgrade) - ignored.

## Gaps
- 8 May T-bill results: no same-day dated source. The DB plus Millennium 11 May put it in R12 May; alternative R11 May if the MoF same-day communique is accepted.
- 13 May offer: the MoF 11 May 15:00 communique was not retrieved, so it sits in R13 May; alternative R12 May.
- DBRS: the agency's own release time was not retrieved (biznes.pap.pl blocked; pulse.bot not allowed), so it sits in R12 May; alternative R11 May.
- Wnorowski: original interview source and time unknown (first dated mention PKO 12 May 07:57).
- Kotecki 13 May PAP Biznes interview: Skrot 17:06 upper bound.
- OK0129 ISIN and maturity from the MoF DB only.
- No PAP consensus for PMI or Q1 wages; April core CPI (NBP, 16 May) is outside.
- BGK per-series FPC results not found (bgk.pl 403). Signing date of the BGK-funds law unknown.
- The April MPC voting record was not seen in the windows.
- ING Think, Pekao and mBank own notes were not downloaded; their views come via PAP.
- The PAP 6 May 17:14 lead says yields 'wzrosly dwucyfrowo', but the body and PKO/Erste show a ~20bp fall. Recorded as a fall.
