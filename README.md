# Polish Fixed Income dashboard

Bond-by-bond analytics for Polish government bonds (POLGB), rendered as one self-contained HTML page:

- **Index duration**: modified/Macaulay duration, cash-flow yield, convexity, DV01, carry/roll and scenario P&L
  for GPWB 1-3Y (`GPWB-B1Y3Y`), GPWB 1-4Y (`GPWB-B1Y4Y`) and `TBSP.Index`. Computed from the official GPW Benchmark
  portfolios and cross-checked against the published index statistics.
- **Curve & asset swaps**: Nelson-Siegel-Svensson fit to Treasury BondSpot fixings; yield-to-IRS spreads by bond and tenor bucket.
- **Rich/cheap**: residual of each bond vs the fitted zero curve.
- **Roll yield, decomposed**: coupon income, pull-to-par, roll-down and repo funding as separate additive pieces (3M and 12M horizons), with breakevens.
- **Poland vs core markets**: curve steepness, carry+roll, central-bank stance and real rates (NBP, ECB, Fed, BoE, CNB, MNB, BNR),
  PL−DE/PL−US spread history, FX-hedged yields from EUR/PLN forward points, German/French/Italian/Spanish/Czech/Hungarian/US bonds
  asset-swapped and swapped into PLN/EUR (ASW now, 1M and 12M ago) vs POLGB, and POLGB vs Poland EUR Eurobonds.
- **Floaters, linkers & quasi-sovereigns**: WZ (6M WIBOR) and NZ (POLSTR) discount margins from a bootstrapped WIBOR forward curve,
  spread/rate duration, floater-vs-fixed-ASW by tenor; IZ real yields, breakevens and 12M carry vs nominals under CPI scenarios; BGK/PFR spreads.
- **Auctions & timing**: MoF calendar, recent auction results, measured auction-cycle behaviour, cash flows, index rebalances.
- **Assessment**: ranked trade ideas with entry timing and risks.

## Refresh

```bash
pip install -r requirements.txt
python src/fetch_bondspot.py 2026-11-09          # BondSpot fixing + session summary
python src/fetch_history.py 2026-08-03 2026-11-09 # optional: fixing history for the auction-cycle study
python src/auction_study.py                       # auction-cycle stats (add --xlsm to re-read the MoF database)
python src/analytics.py 2026-11-09               # -> data/analytics/analytics_YYYYMMDD.json
python src/fetch_swaps.py                        # PLN/CZK/HUF/EUR/USD swap curves + €STR OIS (BlueGamma, last close)
python src/fetch_core.py 2026-08-01              # Bund/UST curves, €STR, SOFR, EURIBOR, PAP cross-country table
python src/core_compare.py 2026-11-09            # -> data/analytics/core_YYYYMMDD.json
python src/floaters_linkers.py 2026-11-09        # -> data/analytics/fl_YYYYMMDD.json (WZ/NZ/IZ)
python src/quasi.py 2026-11-09                   # -> data/quasi.json (BGK FPC/FWSZ, PFR; prices hand-entered in the script)
python src/build_dashboard.py 2026-11-09         # -> dist/dashboard/index.html
python src/deploy.py                             # needs PFI_S3_BUCKET / PFI_S3_KEY (+ optional PFI_CF_DIST, PFI_CF_PATHS)
```

Inputs that are maintained by hand (sources are listed inside each file):

| File | What | Update |
|---|---|---|
| `data/market_inputs.json` | IRS pillars, WIBOR/POLSTR, repo/funding, NBP rates, macro notes | daily/weekly |
| `data/index_portfolios.json` | GPW Benchmark index units + official stats | monthly (after each "Portfele obligacji" communiqué) |
| `data/bonds_static.json` | coupons/maturities of fixed-rate POLGBs | when a new line is issued |
| `data/core/core_inputs.json` | central-bank rates/stance, CPI, EUR/USD swaps & OIS, EUR/PLN forward points, Poland Eurobond yields | weekly / after CB meetings |
| `data/calendar.json` | auctions, MPC, data, flows, index events | monthly (MoF supply plan) |

## Conventions

Annual coupons on the 25th, Act/Act ICMA accrual, annual-compounding yields, clean prices, T+2 settlement (Polish holidays).
Modified duration = Macaulay / (1 + y). Index statistics are market-value weighted at today's dirty prices.
Horizon returns hold the fitted zero curve fixed by time-to-cash-flow and keep each bond's z-spread residual constant.

Not investment advice.

## Point-in-time (retrospective) reports

A snapshot folder holds every input as it was known on a cut-off date, so a report can be rebuilt for a past date
without look-ahead. Example: `data/snapshots/2026-01-02/` (report date Fri 2 Jan 2026; market close 30 Dec 2025;
information published by 31 Dec 2025). `facts.json` carries every qualitative statement with its publication date and
an audit table; benchmarks, RV switches, rebalance projections and trade ideas are chosen by rules in `build_report.py`.

```bash
S=data/snapshots/2026-01-02
python src/fetch_bondspot.py 2025-12-30 --out $S/bondspot_20251230.json
python src/fetch_history.py 2025-08-25 2025-12-30 --out $S/fixing_history.json
python src/fetch_core_asof.py 2025-12-30 2025-08-25 $S/core_rates.json
python src/analytics.py 2025-12-30 --snap $S
python src/auction_study.py --snap $S
python src/floaters_linkers.py 2025-12-30 --snap $S
python src/quasi.py 2025-12-30 --snap $S
python src/core_compare.py 2025-12-30 --snap $S
python src/build_report.py $S                     # -> $S/dist/index.html
```

### Daily series (January 2026) and how to continue it

Snapshots exist for every session report from 2 Jan to 30 Jun 2026 (`data/snapshots/2026-0M-DD/`). From 7 Jan they are
generated by `src/pit_snapshot.py` from the previous snapshot plus a *day spec* holding the hand-collected, dated
inputs. The specs, the raw research (with source URLs and publication times) and the helper scripts are archived in
`data/snapshots/_inputs/2026-01-H1/` (7-15 Jan) and `data/snapshots/_inputs/2026-01-H2/` (16-30 Jan, incl. the GPWB communique for the 30 Jan change).
February inputs are in `data/snapshots/_inputs/2026-02/`; the 2 Feb spec switches to the post-30 Jan portfolios (`index_portfolios` key). March inputs are in `data/snapshots/_inputs/2026-03/` (2 Mar spec switches to the 27 Feb portfolios; WZ0330/WZ0930 coupons reset via `floaters_update` from 26 Mar; NBP reference 3.75% from the 5 Mar report). For April: load the 31 Mar communique (PS1026 leaves TBSP; PDF in `_inputs/2026-03/research/`, regenerated 30 Mar) as `index_portfolios` on the 1 Apr spec, and added PS0731 to `bonds_static.json` via the `bonds_static_add` spec key from the 9 Apr report (first fixing 8 Apr). April inputs are in `data/snapshots/_inputs/2026-04/` (twenty reports; no session on 3 and 6 Apr; Erste tables for 9, 14 and 23 Apr rebuilt from the next issue's change columns, see `tools/build_specs_apr.py`). May (done): the 4 May spec loads the 30 Apr portfolios; DS0436 (5.25%, coupon back-solved from its first fixing) joins from the 12 May report and OK0129 from 29 May (`bonds_static_add`); the WZ May/Nov lines reset to 3.96% from the 26 May report (`floaters_update`). May inputs are in `data/snapshots/_inputs/2026-05/` (Erste: 4 May issue headed 01.05 = 30 Apr closes; 5 May PL IRS table stale after the UK holiday, so the 30 Apr swaps are carried for that report). June (done): the 1 Jun spec loads the 29 May portfolios; no new fixed-rate line (no `bonds_static_add`) and no WZ reset; no session on Corpus Christi (4 Jun), so the 5 Jun report uses the 3 Jun close (T+2 = 8 Jun). June inputs are in `data/snapshots/_inputs/2026-06/` (21 reports; agents' brief in `research/BRIEF_agents.md`). The 3 Jun switch enters via `mof_ops_add` as S/AZ + O/AZ rows from the 5 Jun report (MoF database row, same-day release assumed); MoF offers and the 17 Jun additional sale are used only from their first dated mention; the 2Y benchmark rolled WS0428 -> PS0728 on 12 Jun. For July: load `_inputs/2026-06/index_portfolios_2026-06-30.json` (OK0129 joins TBSP, 1-3Y and 1-4Y; OK0127 leaves TBSP; stats from the PDF regenerated 29 Jun) as `index_portfolios` on the 1 Jul spec.

Conventions for report date R (pre-open):
- market cut-off C = previous Polish session close; info cut-off = evening before R;
- PLN IRS/FRA = LSEG bid table headed C in the Erste Codziennik of R (only those levels, never its commentary);
- cross-country yields = PAP/Bloomberg table on strefainwestorow.pl of R morning, rows stamped C (live US/JP rows dropped, US from the Treasury curve);
- POLSTR index dates published on or after R are not used; SOFR is cut one day before C;
- every fact sits in the window in which it was first published (`research/facts_*.json`).

```bash
J=raw_dir            # holds bondspot_YYYYMMDD.json, hist.json, core_YYYYMMDD.json for the cut-off
python src/fetch_bondspot.py $C --out $J/bondspot_${C//-/}.json
python src/fetch_history.py 2026-01-05 $C --out $J/hist.json     # start from a copy of the previous fixing_history.json
python src/fetch_core_asof.py $C 2025-08-25 $J/core_${C//-/}.json
python src/pit_snapshot.py data/snapshots/$PREV data/snapshots/$R spec_$R.json $J
# then analytics / auction_study / floaters_linkers / quasi / core_compare / build_report as above
```

### Daily archive

`python src/build_archive.py` builds `dist/archive/index.html` (all point-in-time reports by month with key numbers and two
charts) and injects previous / archive / next links into every report and an archive link into the live dashboard
(idempotent). `python src/publish_site.py` uploads the dashboard, the archive and all reports and issues one CloudFront
invalidation (targets from `PFI_S3_BUCKET`, `PFI_S3_PREFIX`, `PFI_CF_DIST`). After adding new daily reports, run both.
