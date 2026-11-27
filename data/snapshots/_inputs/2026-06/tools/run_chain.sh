#!/bin/bash
# usage: run_chain.sh SNAPROOT  (builds the 21 June snapshots from data/snapshots/2026-05-29 onwards)
set -e
cd /home/user/Polish_FixedIncome
SP=/tmp/claude-0/-home-user-Polish-FixedIncome/f82df0b1-d4bb-529b-9fb4-ff4ddefccef7/scratchpad/jun
ROOT=$1; PREV=data/snapshots/2026-05-29
for R in 2026-06-01 2026-06-02 2026-06-03 2026-06-05 2026-06-08 2026-06-09 2026-06-10 2026-06-11 2026-06-12 2026-06-15 2026-06-16 2026-06-17 2026-06-18 2026-06-19 2026-06-22 2026-06-23 2026-06-24 2026-06-25 2026-06-26 2026-06-29 2026-06-30; do
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
