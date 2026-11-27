# PIT facts 15-29 Jun 2026 (report dates 16-30 Jun) - working notes
Output: facts.json (keys mof_ops, new_series, bgk, facts, gpwb, wz_coupons, digest, mpc, data, meta; schema of the May facts_poland_2.json, month-relative keys renamed apr->may, e.g. changes_vs_may, may_official_stats, may_reference) and index_portfolios_2026-06-30.json (schema of index_portfolios_2026-05-29.json; changes_vs_2026-05-29 with may/jun/diff).
Builder: scripts/build.py (+ build_ops.py for the MoF DB rows and the GPWB reconciliation). Helpers: listparse.py (listing -> dl/index_all.json), rd.py (article body + time -> dl/txt, dl/art_index.json), h2t.py, skrot.py (Skrot sections -> work/skrot_pl.txt, deduped work/skrot_dedup2.txt), oh_rows.py (MoF DB -> work/oh_jun.json), gpwb_parse_jun.py (-> work/gpwb_parsed.json), validate.py (schema check vs the May templates: 0 errors).
Raw downloads:
- dl/list (listing p251-296), dl/art + dl/txt (806 PAP items dated 15-29 Jun).
- dl/gov (komunikaty-dlug p1-4, June plan page, May FX-account page), dl/db (Obligacje_Hurtowe.xlsm, Bony_Skarbowe.xls, hurtowe page).
- dl/gpwb (served PDF Portfele_obligacji_2026_06_26_.pdf + headers, pap/ copy of the 26 Jun ESPI attachment, communique page c2866.html, calendar, listing pages).
- dl/res/{pko (item pages only), mil, erste} (11 dailies each, 15-29 Jun). dl/web (nbp.pl block page).
Windows: R16=15 Jun, R17=16, R18=17, R19=18, R22=19-21, R23=22, R24=23, R25=24, R26=25, R29=26-28, R30=29 Jun.
Timestamps: PAP article times exact. PAP Skrot 17:0x/21:xx = upper bound. Erste/Millennium PDF CreationDate (UTC in pdfinfo, +02 applied) = upper bound. PKO and gov.pl = date only (time written as 00:00). MoF offer communiques: PAP calendar slot 15:00 (strict alternatives noted). CEST throughout.

## Access tips (27 Nov 2026)
- strefainwestorow listing `https://strefainwestorow.pl/wiadomosci?page=N`.
  - 15 Jun = p284-286; 16 Jun = p281-284; 17 Jun = p278-281; 18 Jun = p274-278; 19 Jun = p272-274; 22 Jun = p270-272.
  - 23 Jun = p267-269; 24 Jun = p265-267; 25 Jun = p263-265; 26 Jun = p261-263; 29 Jun = p259-261; 30 Jun starts p259.
  - 20 and 27 Jun have no items; weekend Skrot digests on 21 Jun (20:12) and 28 Jun (21:03), in a different format (no Poland sections).
  - Plain curl, xargs -P 16 fine; 806 items in ~3 min (run in background). 6 duplicate URLs across pages (list shifted during the fetch) = nothing lost.
  - Real slugs are truncated: resolve guessed slugs by the longest common prefix (build.py `a()`).
- Bond-related PAP items: no auction headline articles again; offers via FX/FI pieces, results via Skrot. The 17 Jun ADDITIONAL sale is in no PAP item (first in Erste/Millennium 18 Jun); the 24 Jun one is in the same-day Skrot.
- MoF: `gov.pl/web/finanse/komunikaty-dlug?page=3&size=10`. The only in-window entry is 15.06 (FX account for May; PAP carried it 16 Jun 16:58).
  - The July supply plan and the Q3 financing plan are both dated 30.06 (page 2) - outside.
  - Pages 1-2 otherwise hold later notices: titles only seen.
  - Auction offer/result communiques are not on any gov.pl list found; one web search (to locate them) gave only plan pages.
- MoF DB: same attachments d12c559c (Last-Modified 25 Nov 2026) and 31ac439a (18 Nov). openpyxl reads the .xlsm; `pip install xlrd` for the .xls.
  - 17/24 Jun rows match PAP totals exactly. SD PodazMin = additional-sale offer: 2,067m (17 Jun), 1,765m (24 Jun).
  - No other wholesale operation 4-30 Jun; no T-bills between 8 May and 10 Jul.
- PKO: listing `centrumanaliz.pkobp.pl/aktualnosci?offset=105-120` covers 10 Jun-8 Jul.
  - The cdn-netpr PDFs now return HTTP 401 (a retry with a browser Referer was refused by the session's permission classifier - not pursued).
  - The item pages carry the full daily text and a `publication-date` (date only). Used those.
- Millennium `daily2606DD`: all 11 days exist (Last-Modified ~07:00 UTC). Plain pdftotext reads the page-2 'Rynek krajowy' paragraph best.
- Erste ids 169503 (15 Jun) ... 169541 (29 Jun); id/timestamp table copied from agent_jun_curves2/dl/ids.tsv, PDFs re-downloaded here.
- GPWB:
  - The listing `komunikaty-i-uchwaly-gpw?ph_main1_offset=60` shows cmn_id=2866 (26.06.2026). The page needs the exact title parameter (`TBSP.Index / GPWB-B1Y3Y / GPWB-B1Y4Y/ GPWB-B1Y5Y / GPWB-B3Y5Y / GPWB-B5Y / GPWB-BWZ (Komunikat)`), a Referer and the cookies set by the listing; otherwise it returns 9 bytes.
  - PDF link `Portfele_obligacji_2026_06_26_.pdf` (trailing underscore). `_2026_06_26.pdf` and the _22.._30 variants are 404.
  - The PDF needs browser UA + Accept headers.
- Blocked: nbp.pl (Imperva, 403). bgk.pl not tried (403 in May).

## Key findings
- MoF supply in the windows: two sales, no switch, buyback or T-bill. Lines come from the MoF DB, confirmed by PAP.
  - 17 Jun (plan 6-12bn; offer 7-12bn, communique slot 15 Jun 15:00, first seen 17 Jun 08:50 -> R16 primary / R18 strict): 12,000.53m sold against 18,267.53m (cover 1.52, a 3-month high); additional 791m (offer 2,067m).
    - PS0731 4,442.03m @95.925 (4.918%); DS0436 2,397m @98.71 (5.416%); OK0129 1,931.5m @89.39 (4.399%).
    - NZ0331 1,873m @94.862; DS1030 1,088m @86.65 (4.711%); IZ0836 151m (real 2.983%); NZ0936 118m.
  - 24 Jun (offer 7-12bn, communique slot 22 Jun 15:00, first seen 23 Jun 08:41 -> R23 primary / R24 strict): 12,000.3m against 15,420.3m (cover 1.28); additional 1,316m (offer 1,765m).
    - PS0731 4,187m @95.971 (4.911%); NZ0331 2,717m; OK0129 2,355m (4.396%); DS0436 1,919.3m (5.417%); DS1035 802m (5.334%); NZ0936 20m.
  - Financing of 2026 needs: ~58% (Erste) / ~59% (Millennium) after 17 Jun -> ~62% of PLN 688bn (MoF, 24 Jun).
  - The July/Q3 plan was not out by 29 Jun (due 30 Jun 15:00). July retail coupons unchanged (24 Jun).
- June plan (29 May, background only): sales 17 and 24 Jun at 6-12bn each (OK0129/NZ0331/PS0731/DS0436/NZ0936 + IZ/other); switch 3 Jun (buybacks DS0726, PS1026, WZ1126, OK0127, PS0527); no T-bills.
- MoF other items:
  - Budget deficit after May 108.2bn (39.8% of 271.7bn).
  - FX on accounts EUR 15.68bn (gov.pl 15.06).
  - State Treasury debt 2,135.6bn (+2.2% m/m; 22 Jun).
  - EU funds May EUR 1.13bn (26 Jun).
  - MoF draft WIBOR ban for new consumer contracts (22 Jun); alcohol excise roadmap +18bn/10y and sugar fee (24 Jun).
- GPWB communique (published 26 Jun, page + PAP 19:02 -> R29; effective after the 30 Jun session; holdings "as of 25 Jun"):
  - OK0129 enters TBSP (19 bonds), B1Y3Y (6), B1Y4Y (9) and B1Y5Y (12). OK0127 leaves TBSP.
  - Unit changes: DS1033/DS1035/DS1034/DS1030/PS0731/PS0527/DS0436 (TBSP); B5Y; DS1030 in B1Y5Y/B3Y5Y; NZ0331 in BWZ.
  - Units reconcile exactly with MoF auctions held 27 May-25 Jun, INCLUDING the 24 Jun sale settled 26 Jun (after the "as of" date): see facts.gpwb.integrity_flag.
  - REGENERATED PDF: the served file is CreationDate 29 Jun 13:16 CEST, Last-Modified 29 Jun 13:51 CEST, 8 pages, Print-To-PDF. The 26 Jun original (PAP/ESPI attachment) is CreationDate 26 Jun 13:25 CEST, 7 pages, holdings only.
  - Holdings are identical in both versions; the re-post ADDS the statistics page. Official stats are therefore first public 29 Jun (R30), not 26 Jun.
  - Stats as of 25 Jun: TBSP YTM 4.56%, mod dur 3.76, value 945.1bn; B1Y3Y 4.08% / 1.81; B1Y4Y 4.21% / 2.29.
  - Next change 31 Jul (announcement 29 Jul, GPWB calendar).
- BGK:
  - First FPC switch, 18 Jun (offer 16 Jun): sold FPC0229/0231/0332/0235 for 1,348.57m (demand 2,110.873m); bought back FPC0427 for 1,435.297m (offers 2,193.527m).
  - FPC0235 admitted to Catalyst from 22 Jun. No regular FPC tender; BGK Q3 plan due 30 Jun.
- MPC:
  - Kotecki (Bloomberg, Skrot 15 Jun): changes unlikely to end-2026 or Q1 2027; hike appetite lower; too early to signal cuts.
  - Sobon (NBP board, 17 Jun): no policy cycle. Duda (DGP, 18 Jun): stable rates the base case, little room for cuts.
  - May voting record (18 Jun): Tyrowicz +100bp rejected. NIK (16 Jun): 2025 MPC guidance gave limited information.
  - Tyrowicz against the 2025 policy report (MSiG, 29 Jun).
  - No June minutes in the windows. Next MPC 7-8 Jul (PAP 29 Jun).
- Data, actual vs consensus:
  - May CPI 3.1 / -0.3 m/m (= flash). Core 3.1 (PKO cites 3.0 consensus).
  - Industry 4.1 vs 2.5 (m/m -0.8 vs -2.2). Retail 3.0 vs 3.8. Wages 5.8 vs 6.0; employment -0.9 (as expected).
  - Construction 3.9 vs 4.9. PPI 2.4 vs 2.5. M3 11.0 (vs ~11.4). Unemployment 5.9 (as expected).
  - GUS consumer price expectations 20.2 (24.7); BWUK -9.9. GUS composite 98.8. Orders +143.3% (SAFE). ESI 100.6.
  - NBP survey: CPI 3.0 / 2.9 / 2.7; reference rate 3.76 / 3.66 / 3.50.
- Fiscal and ratings:
  - Windfall tax: government 16 Jun; Sejm 19 Jun (60% rate, ~4bn); Senate cap amendments 25 Jun.
  - Fuel: excise back 15 Jun (decided 12 Jun, part 1); VAT 8% and price caps to 30 Jun; decision on VAT "shortly" (Tusk 16 Jun). None announced by 29 Jun.
  - KPO 8th request PLN 33.8bn (19/25 Jun). Fiscal Council (17 Jun): faster consolidation. NIK: SRW limit overstated by 84.5bn.
  - Ratings: no sovereign action. Fitch CEO Linnell (remarks 23 Jun, first dated 24 Jun 08:55 -> R25): public finances the key risk to A- negative.
  - Fitch bank IDRs (17 Jun) not sovereign.
- Market path (PAP DS0436 afternoon quotes): 5.57 (12 Jun) -> 5.45 (15) -> 5.41 (16) -> 5.40 (17) -> 5.44 (18) -> 5.44 (19) -> 5.42 (22) -> 5.41 (23) -> 5.38 (24) -> 5.33 (25) -> 5.27 (26) -> 5.30 (29 Jun).
  - Banks: hike pricing gone by 25-26 Jun (PKO, Erste FRAs), small 2027 cut odds priced by 26 Jun (PKO 29 Jun).

## Not used / outside the windows
- 30 Jun and later:
  - Flash June CPI; the MoF July plan / Q3 plan and the BGK Q3 plan; 30 Jun dailies.
  - gov.pl titles Jul-Nov, PKO listing titles to 8 Jul, GPWB listing items after 26 Jun (seen while paging).
  - DB rows after 29 Jun (e.g. the 10 Jul T-bill).
- Part-1 / pre-window, context only:
  - June plan (29 May); 3 Jun switch (amounts used only to reconcile GPWB units); MPC 1-2 Jun.
  - Dabrowski (Bloomberg, 12 Jun; recapped 15 Jun); CPN extension without the excise cut (12 Jun); April C/A (12 Jun).
  - 27 May sale and 13/21 May OK0129 amounts (reconciliation only).
- Weekend global headlines (US-Iran talks, Hormuz) left to the global agents except a one-line mention in the R22 digest.

## Gaps
- MoF offer communiques (15 and 22 Jun, 15:00 slot) were not retrieved.
  - Offers are placed in R16/R23 (primary). The strict first-dated-mention alternative is R18/R24 (noted in mof_ops and facts).
  - Coordinator: choose one convention.
- 17 Jun additional sale (791m): DB trade date 17 Jun, but the first dated mention is 18 Jun 08:35. Kept in the R18 op; strict alternative R19.
- PKO PDFs 401 -> item-page text, date only.
- nbp.pl blocked: no NBP primary documents (minutes, voting PDF, M3 release). June MPC minutes not seen by 29 Jun.
- BGK per-series switch results not found.
- Original publication times not found (upper bounds used): Kotecki (Bloomberg), Duda (DGP), Fitch CEO (interview source unknown).
- MoF FX-account page: gov.pl date 15.06 but PAP only 16 Jun 16:58. Kept in R16; alternative R17.
- No PAP consensus for core, M3 or unemployment; bank figures used.
- The EC consumer inflation-expectations figure (PAP 29 Jun: 20.2 from 24.7) equals the GUS figures of 18 Jun, a probable PAP mix-up (as in May). Flagged.
- Banks give different May tax-growth rates for the budget (PKO excise -15%, Erste +2.7%). Both recorded as published.
