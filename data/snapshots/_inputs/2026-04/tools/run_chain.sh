#!/bin/bash
# usage: run_chain.sh SNAPROOT  (builds the 20 April snapshots from data/snapshots/2026-03-31 onwards)
set -e
cd /home/user/Polish_FixedIncome
SP=/tmp/claude-0/-home-user-Polish-FixedIncome/24a3fc3c-8e3f-5cce-b7fb-dcdc0e9e199e/scratchpad/apr
ROOT=$1; PREV=data/snapshots/2026-03-31
for R in 2026-04-01 2026-04-02 2026-04-07 2026-04-08 2026-04-09 2026-04-10 2026-04-13 2026-04-14 2026-04-15 2026-04-16 2026-04-17 2026-04-20 2026-04-21 2026-04-22 2026-04-23 2026-04-24 2026-04-27 2026-04-28 2026-04-29 2026-04-30; do
  C=$(python3 -c "import json;print(json.load(open('$SP/specs/$R.json'))['market_cutoff'])")
  S=$ROOT/$R; rm -rf $S
  python src/pit_snapshot.py $PREV $S $SP/specs/$R.json $SP/raw > $SP/logs_$R.txt 2>&1
  python src/analytics.py $C --snap $S >> $SP/logs_$R.txt 2>&1
  python src/auction_study.py --snap $S >> $SP/logs_$R.txt 2>&1
  python src/floaters_linkers.py $C --snap $S >> $SP/logs_$R.txt 2>&1
  python src/quasi.py $C --snap $S >> $SP/logs_$R.txt 2>&1
  python src/core_compare.py $C --snap $S >> $SP/logs_$R.txt 2>&1
  python src/build_report.py $S >> $SP/logs_$R.txt 2>&1
  echo "$R ok $(head -1 $SP/logs_$R.txt | cut -c1-160)"
  PREV=$S
done
