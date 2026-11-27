#!/bin/bash
# usage: run_chain.sh SNAPROOT  (builds the 20 May snapshots from data/snapshots/2026-04-30 onwards)
set -e
cd /home/user/Polish_FixedIncome
SP=/tmp/claude-0/-home-user-Polish-FixedIncome/24a3fc3c-8e3f-5cce-b7fb-dcdc0e9e199e/scratchpad/may
ROOT=$1; PREV=data/snapshots/2026-04-30
for R in 2026-05-04 2026-05-05 2026-05-06 2026-05-07 2026-05-08 2026-05-11 2026-05-12 2026-05-13 2026-05-14 2026-05-15 2026-05-18 2026-05-19 2026-05-20 2026-05-21 2026-05-22 2026-05-25 2026-05-26 2026-05-27 2026-05-28 2026-05-29; do
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
