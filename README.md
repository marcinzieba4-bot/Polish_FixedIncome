# Polish Fixed Income dashboard

Bond-by-bond analytics for Polish government bonds (POLGB), rendered as one self-contained HTML page:

- **Index duration**: modified/Macaulay duration, cash-flow yield, convexity, DV01, carry/roll and scenario P&L
  for GPWB 1-3Y (`GPWB-B1Y3Y`), GPWB 1-4Y (`GPWB-B1Y4Y`) and `TBSP.Index`. Computed from the official GPW Benchmark
  portfolios and cross-checked against the published index statistics.
- **Curve & asset swaps**: Nelson-Siegel-Svensson fit to Treasury BondSpot fixings; yield-to-IRS spreads by bond and tenor bucket.
- **Rich/cheap**: residual of each bond vs the fitted zero curve.
- **Roll yield, decomposed**: coupon income, pull-to-par, roll-down and repo funding as separate additive pieces (3M and 12M horizons), with breakevens.
- **Auctions & timing**: MoF calendar, recent auction results, measured auction-cycle behaviour, cash flows, index rebalances.
- **Assessment**: ranked trade ideas with entry timing and risks.

## Refresh

```bash
pip install -r requirements.txt
python src/fetch_bondspot.py 2026-11-09          # BondSpot fixing + session summary
python src/fetch_history.py 2026-08-03 2026-11-09 # optional: fixing history for the auction-cycle study
python src/auction_study.py                       # auction-cycle stats (add --xlsm to re-read the MoF database)
python src/analytics.py 2026-11-09               # -> data/analytics/analytics_YYYYMMDD.json
python src/build_dashboard.py 2026-11-09         # -> dist/dashboard/index.html
python src/deploy.py                             # needs PFI_S3_BUCKET / PFI_S3_KEY (+ optional PFI_CF_DIST, PFI_CF_PATHS)
```

Inputs that are maintained by hand (sources are listed inside each file):

| File | What | Update |
|---|---|---|
| `data/market_inputs.json` | IRS pillars, WIBOR/POLSTR, repo/funding, NBP rates, macro notes | daily/weekly |
| `data/index_portfolios.json` | GPW Benchmark index units + official stats | monthly (after each "Portfele obligacji" communiqué) |
| `data/bonds_static.json` | coupons/maturities of fixed-rate POLGBs | when a new line is issued |
| `data/calendar.json` | auctions, MPC, data, flows, index events | monthly (MoF supply plan) |

## Conventions

Annual coupons on the 25th, Act/Act ICMA accrual, annual-compounding yields, clean prices, T+2 settlement (Polish holidays).
Modified duration = Macaulay / (1 + y). Index statistics are market-value weighted at today's dirty prices.
Horizon returns hold the fitted zero curve fixed by time-to-cash-flow and keep each bond's z-spread residual constant.

Not investment advice.
