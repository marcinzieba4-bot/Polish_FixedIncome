# PIT facts 29 May - 14 Jun 2026 (report dates 1-15 Jun) - working notes
Output: facts.json (same folder). Keys: mof_ops, new_series, bgk, facts, gpwb, wz_coupons, digest, mpc, data, meta. Schema as in 2026-05 facts_poland_1.json (checked by scripts/validate.py: 0 errors; the switch entry adds the March-style switch keys).
Builder: scripts/build.py. Helpers: scripts/listparse.py (listing -> dl/index.json), h2t.py (strefainwestorow HTML -> dl/txt + dl/times.json), skrot.py (Skrot sections -> work/skrot_pl.txt, deduplicated in work/skrot_dedup.txt), govlist.py / govpage.py (gov.pl lists and pages), oh_rows.py (MoF DB -> work/oh_jun.json), validate.py.
Raw downloads:
- dl/list: listing pages p250-315. dl/art + dl/txt: 707 PAP items dated 29 May-14 Jun. dl/index.json, dl/titles.txt.
- dl/gov: komunikaty-dlug p1-4, June plan page and PDF, dlug-publiczny page. dl/db: Obligacje_Hurtowe.xlsm (OH.xlsm), Bony_Skarbowe.xls (BS.xls), bony-i-obligacje-hurtowe1 page.
- dl/res/{pko,mil,erste}: 10 dailies each (29 May; 1, 2, 3, 5, 8, 9, 10, 11, 12 Jun); dl/res/erste/archiwum.html. dl/gpwb: kalendarium-indeksow (kal2.html).
- work/res: pdftotext output (layout and raw).
Windows: R1 Jun = 29-31 May, R2 = 1 Jun, R3 = 2 Jun, R5 = 3-4 Jun, R8 = 5-7 Jun, R9 = 8 Jun, R10 = 9 Jun, R11 = 10 Jun, R12 = 11 Jun, R15 = 12-14 Jun.
Timestamps:
- PAP article times are exact. PAP Skrot 17:0x/21:xx = upper bound.
- PDF CreationDate (local, +02) = upper bound. gov.pl = date only.
- CEST throughout.

## Access tips (27 Nov 2026)
- strefainwestorow listing `https://strefainwestorow.pl/wiadomosci?page=N`. Page ranges:
  - 29 May = p307-309; 1 Jun = p304-307; 2 Jun = p302-304; 3 Jun = p299-302; 4 Jun = p298-299; 5 Jun = p297-298.
  - 8 Jun = p295-297; 9 Jun = p293-295; 10 Jun = p290-293; 11 Jun = p288-290; 12 Jun = p286-288; 13-14 Jun = p286.
  - Plain curl, xargs -P 16. 23 of 707 articles came back empty the first time (proxy resets); two re-fetch passes fixed all.
  - Items per day: 81 on 3 and 11 Jun ... 12 on 4 Jun (holiday). 30 May has 2 items, 13 Jun 1; weekend Skrot on 31 May, 7 and 14 Jun.
- The PAP feed lacks all MoF auction headlines (no switch result on 3 Jun, no PMI article, no C/A article, no Maslowska or Dabrowski-Bloomberg article). The Skrot digests carry the June plan, switch offer, PMI, C/A, both Bloomberg MPC interviews and the BGK items.
- MoF `gov.pl/web/finanse/komunikaty-dlug?page=3&size=10`: in-window entries are only the 29.05 June plan; the next item is 15.06 (May FX account, outside).
  - Pages 1-2 hold Jun-Nov notices; only their titles were seen while paging.
  - June plan PDF: attachment b1424f70-67ea-42be-a925-dd46ba7496d6, CreationDate 29 May 11:08 CEST, Last-Modified 11:42 CEST. gov.pl drops connections often: retry loops needed.
- MoF DBs (linked from gov.pl/web/finanse/bony-i-obligacje-hurtowe1): Obligacje_Hurtowe.xlsm attachment d12c559c... (Last-Modified 25 Nov 2026); Bony_Skarbowe.xls 31ac439a... (Last-Modified 18 Nov 2026). Only rows dated 27 May (reconciliation) and 3 Jun were read; later rows exist and were not used.
- PKO: listing `centrumanaliz.pkobp.pl/aktualnosci?offset=115-125` covers 28 May-15 Jun. Item pages link cdn-netpr PDFs; the cdn link is a 302 redirect, so use `curl -L`.
- Millennium `daily2605DD` / `daily2606DD`: all 10 window days exist.
- Erste archive `erste.pl/serwis-ekonomiczny/codziennik/archiwum` (5 MB). Window ids: 169465 (29 May), 169472, 169480, 169482, 169489, 169491, 169494, 169495, 169498, 169499 (12 Jun). There is no 4 Jun file.
- GPWB: `gpwbenchmark.pl/kalendarz` returned 404; `gpwbenchmark.pl/kalendarium-indeksow` works with a browser UA and Accept headers.
- WARNING: two web searches for the 3 Jun switch result returned only the June/July plan pages and unrelated items. Nothing post-window was used.

## Key findings
- MoF June plan (29 May; R1):
  - Sales on 17 Jun (settles 19 Jun) and 24 Jun (settles 26 Jun), PLN 6-12bn each, in OK0129/NZ0331/PS0731/DS0436/NZ0936 (+IZ/other).
  - One switch on 3 Jun (settles 8 Jun) buying back DS0726/PS1026/WZ1126/OK0127/PS0527. No T-bills.
  - Retail coupons unchanged. Drop: budget accounts >200bn at end-May. MoF: ~56% of needs financed.
- 3 Jun switch (offer 1 Jun, R2: also sells DS1034). The lines come from the MoF DB only:
  - Sold 11,634.946m on 12,837.703m demand (cover 1.10); bought back 10,904.925m (12,043.667m tendered); net supply +730.0m.
  - OK0129 3,841.466 @88.35 (4.812%); PS0731 3,584.737 @94.40 (5.269%); NZ0331 2,177.522 @94.66; DS0436 1,000.659 @96.601 (5.703%); DS1034 511.996 @96.431 (5.535%); NZ0936 518.566 @87.441.
  - Buyback: PS0527 7,424.049 @99.87; WZ1126 1,745.876 @100.105; DS0726 990 @99.80; PS1026 585 @98.69; OK0127 160 @97.70.
  - No additional sale. Six ZG rows (undocumented, as in March).
  - Placed in R5 as a SLOT: no dated in-window mention was found anywhere (see Gaps).
- Other MoF items:
  - April: non-residents +0.6bn to 190.5bn (12.1%); SPW turnover 2,045.2bn; EU funds EUR 1.06bn (29 May).
  - May retail bonds 5,398.5m; budget accounts 208.3bn at end-May; 148.7bn of 2026 redemptions left (8 Jun).
  - PDP 2,008.2bn (50.6% of GDP) and EDP 61.6% at end-Q1 (10 Jun). Drop: POLSTR SPW 40bn; WIBOR end-2036 'optimal' (10 Jun).
  - No foreign issue, FX-account, WZ/NZ/PP coupon notice or budget-execution release in the windows.
- MPC:
  - Hold on 2 Jun (15:36): May CPI eased on food; data-dependent; risk wording unchanged.
  - Glapinski (3 Jun): lower CPI cuts hike odds; rates 'good', no reason to discuss changes; a hike debate only with durable oil plus the end of fuel support. GS, Noble and Erste called it dovish.
  - May minutes (5 Jun): CPI outlook highly uncertain; a further rise was possible; most backed the hold.
  - Tyrowicz voted against the NBP 2025 accounts resolution (MSiG 3 Jun).
  - Maslowska (Bloomberg, Skrot 9 Jun): cuts more likely than hikes. Dabrowski: room for cuts if the world calms (Polsat 10 Jun); a cut is more likely than a hike (Bloomberg, Skrot 12 Jun).
- Data, actual vs consensus:
  - May flash CPI 3.1% / -0.3% m/m vs 3.7 / +0.2 (food -1.0% m/m).
  - Q1 GDP 3.5% (flash 3.4); consumption 3.3 vs 3.9, investment 2.4 vs 3.0.
  - PMI 49.4 vs 48.5; registered unemployment 5.9 vs 5.9.
  - April C/A EUR -1,558m vs -342m (PAP; PKO calendar -505m).
  - Reserves EUR 255.6bn; bank profit Jan-Apr 13.22bn (-19.9%).
- Fiscal and ratings:
  - 2027 macro: GDP 3.1%, CPI 2.5%, public pay +3%, pensions >=3.48% (9 Jun). Minimum wage 4,950 (+3.0%), first dated 10 Jun (PKO).
  - Windfall tax ~5bn for Mar-Dec (29 May), then 60% rate and 3.8bn in the 11 Jun draft.
  - EC: CSRs and leeway for energy-related spending (3 Jun). EKF consensus: deficit 6.9% of GDP (2 Jun).
  - Fuel: the VAT cut was extended to 30 Jun (Dz.U. 12 Jun); the excise cut is not extended from 15 Jun (MoF source, 12 Jun); Tusk (13 Jun): CPN to end in summer.
  - SAFE: EUR 6.6bn advance; 29 contracts for PLN 78bn (30 May). KPO: 31bn zl tranche (2 Jun).
  - No rating action or scheduled sovereign review in the windows. Fitch's 8 Jun item is a forecast round. S&P's Vartapetov gave PAP interview remarks (first dated Erste 1 Jun / Skrot 1 Jun).
- BGK:
  - FPC switch on 18 Jun announced 29 May (buyback FPC0427).
  - EUR FPC deal 2 Jun: 8Y EUR 1.25bn + 15Y EUR 0.75bn, demand EUR 4.6bn.
  - Q3 issuance will prefund 2027 FPC needs, ~30% secured (12 Jun). No FPC sale tender and no FWSZ auction in the windows.
- GPWB: the 27 May communique took effect on 29 May (DS0436 into TBSP, 19 bonds; PS0527 out of B1Y3Y/B1Y4Y/B1Y5Y; NZ0331/NZ0928 into BWZ). No new bond-index communique. Calendar: 4 Jun no session; next announcement 26 Jun, change 30 Jun. NBP: no FX table on 4 Jun.
- Market pricing (PAP and bank dailies):
  - 29 May: yields -20bp on the CPI miss; Erste: 6M+ FRAs -20bp.
  - 2 Jun: ING ~+25bp priced for 2026; PKO: an October hike fully priced plus half of another; Millennium: 1-2 hikes.
  - 5 Jun (Millennium): ~1 hike by year-end and ~2 in 12 months had been priced before Glapinski.
  - 8 Jun (Millennium): 1-2 hikes by year-end still priced.
  - 9 Jun: -11-14bp; Erste: 9-12M FRAs -20bp. 11 Jun: PKO says fewer hikes are expected.
  - DS0436 (PAP): 5.77 (29 May am) -> 5.60 (29 May) -> 5.70 (1 Jun) -> 5.67 (3 Jun) -> 5.71 (5 Jun) -> 5.79 (8 Jun pm) -> 5.71 (9 Jun) -> 5.70 (10 Jun) -> 5.66 (11 Jun) -> 5.57 (12 Jun).

## Not used / outside the windows
- 15 Jun and later:
  - May CPI final (15 Jun) and the MoF May FX-account notice (15 Jun, title only).
  - Offers and results of the 17/24 Jun sales; the BGK 18 Jun switch; core CPI.
  - GPWB 26/30 Jun; PKO 15 Jun daily and later PKO/Erste archive titles; MoF list titles Jul-Nov; T-bill DB rows from July.
- Pre-window context, not re-used as new facts:
  - 27 May sale; 28 May BGK tender (in the Millennium 29 May recap); 27 May GPWB communique; CPN extension to 15 Jun (28 May); ESI (28 May).
  - May MPC remarks (Zarzecki, Kotecki, Litwiniuk) re-quoted on 1 Jun; Vartapetov 26 May.

## Gaps
- 3 Jun switch results:
  - Not in the PAP feed or in any PKO/Millennium/Erste daily of 5-12 Jun; the MoF communique was not retrieved and the web searches found nothing.
  - Slot R5 assumes the standard same-day communique; strict placement is impossible from the sources read. Lines are from the MoF DB only.
- Switch offer: MoF time not retrieved (calendar slot 15:00; Skrot 17:02 upper bound).
- Original times not found (upper bounds used):
  - Vartapetov interview (first dated mention Erste 1 Jun 08:53; probably PAP Biznes 29 May; alt R1).
  - Maslowska (Skrot 9 Jun 17:06; PAP 10 Jun says 'Monday' = 8 Jun, ING/Millennium point to 9 Jun; alt R9).
  - Dabrowski Bloomberg (Skrot 12 Jun 17:08).
  - Minimum-wage decision (PKO 10 Jun 08:17; KPRM 9 Jun communique not retrieved; alt R10).
- BGK EUR deal coupons/spreads and FPC details: bgk.pl 403.
- PMI and C/A: no PAP article. Consensus from the PKO/Millennium calendars and the Skrot (C/A -342m PAP vs -505m in the PKO calendar).
- The MoF 8 Jun report line '132 mld zl do konca roku' is reported as written; its exact definition is unclear.
- The PAP feed on strefainwestorow is a subset of PAP Biznes. Other MPC remarks, if any, may be missing. ING Think, Pekao and mBank notes were not downloaded; their views come via PAP.
