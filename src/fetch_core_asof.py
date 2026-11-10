"""Point-in-time core-market rates for a snapshot: Bund curve, UST curve, €STR, SOFR, EURIBOR up to a cut-off date.

Usage: python src/fetch_core_asof.py 2025-12-30 2025-08-25 data/snapshots/2026-01-02/core_rates.json
       (cutoff, history start, output). Only observations dated <= cutoff are kept.
"""
import csv
import datetime as dt
import io
import json
import pathlib
import re
import sys

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fetch_core import UA, bund  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


def ust_year(year):
    url = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all"
           f"?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv")
    out = {}
    for r in csv.DictReader(io.StringIO(requests.get(url, headers=UA, timeout=40).text)):
        out[dt.datetime.strptime(r["Date"], "%m/%d/%Y").date().isoformat()] = {k: float(v) for k, v in r.items() if k != "Date" and v}
    return out


def estr_range(start, end):
    url = f"https://data-api.ecb.europa.eu/service/data/EST/B.EU000A2X2A25.WT?startPeriod={start}&endPeriod={end}&format=csvdata"
    return {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in csv.DictReader(io.StringIO(requests.get(url, headers=UA, timeout=60).text))}


def sofr_range(start, end):
    j = requests.get(f"https://markets.newyorkfed.org/api/rates/secured/sofr/search.json?startDate={start}&endDate={end}", headers=UA, timeout=40).json()
    return {r["effectiveDate"]: r["percentRate"] for r in j.get("refRates", [])}


def euribor_year(year, cutoff):
    """euribor-rates.eu yearly table: last available fixing on/before cutoff per tenor."""
    out = {}
    for tenor, slug in (("3 months", "3-months"), ("6 months", "6-months"), ("12 months", "12-months")):
        t = requests.get(f"https://www.euribor-rates.eu/en/euribor-rates-by-year/{year}/", headers=UA, timeout=40).text
        out["_page_len"] = len(t)
        break
    return out


def main():
    cutoff, start, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    res = {"cutoff": cutoff, "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "bund": {}}
    for T in (1, 2, 3, 5, 7, 10, 15, 20, 30):
        res["bund"][str(T)] = {d: v for d, v in bund(T, start).items() if d <= cutoff}
    u = ust_year(int(cutoff[:4]))
    res["ust"] = {d: v for d, v in u.items() if start <= d <= cutoff}
    res["estr"] = {d: v for d, v in estr_range(start, cutoff).items() if d <= cutoff}
    res["sofr"] = {d: v for d, v in sofr_range(start, cutoff).items() if d <= cutoff}
    p = ROOT / outp
    p.write_text(json.dumps(res, indent=0))
    lb = max(res["bund"]["10"]); lu = max(res["ust"])
    print("bund", lb, {T: res["bund"][T].get(lb) for T in res["bund"]})
    print("ust", lu, res["ust"][lu])
    print("estr", sorted(res["estr"].items())[-2:], "sofr", sorted(res["sofr"].items())[-2:])


if __name__ == "__main__":
    main()
