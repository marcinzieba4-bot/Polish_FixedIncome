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
