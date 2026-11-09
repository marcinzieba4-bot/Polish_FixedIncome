"""Fetch BondSpot fixing history (price + yield per bond per day) for a date range.

Usage: python src/fetch_history.py 2026-09-01 2026-11-09
Writes data/market/fixing_history.json  {date: {ticker: [fix_price, fix_yield]}}
"""
import datetime as dt
import json
import pathlib
import sys
import time

from fetch_bondspot import fetch_fixing

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    d0, d1 = (dt.date.fromisoformat(x) for x in sys.argv[1:3])
    p = ROOT / "data" / "market" / "fixing_history.json"
    hist = json.loads(p.read_text()) if p.exists() else {}
    d = d0
    while d <= d1:
        if d.weekday() < 5 and d.isoformat() not in hist:
            try:
                _, level, fx = fetch_fixing(d)
                if fx:
                    hist[d.isoformat()] = {"_tbsp": level, **{f["ticker"]: [f["fix_price"], f["fix_yld"]] for f in fx}}
            except Exception as e:  # holidays / missing days
                print(d, "skip", e)
            time.sleep(0.3)
        d += dt.timedelta(days=1)
    p.write_text(json.dumps(dict(sorted(hist.items())), indent=0))
    print("days:", len(hist))


if __name__ == "__main__":
    main()
