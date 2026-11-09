"""Fetch core-market rates for the Poland-vs-core section.

- Bund par yields by residual maturity (Bundesbank BBSIS term structure, daily)
- US Treasury par yield curve (home.treasury.gov, daily CSV)
- €STR (ECB data API), SOFR (NY Fed), EURIBOR (euribor-rates.eu)
Writes data/core/core_rates.json
Usage: python src/fetch_core.py 2026-08-01
"""
import csv
import datetime as dt
import io
import json
import pathlib
import re
import sys

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (polish-fi-dashboard)"}
BB = "https://api.statistiken.bundesbank.de/rest/data/BBSIS/D.I.ZST.ZI.EUR.S1311.B.A604.R{:02d}XX.R.A.A._Z._Z.A?startPeriod={}&format=csv"


def bund(tenor, start):
    t = requests.get(BB.format(tenor, start), headers=UA, timeout=30).text
    out = {}
    for line in t.splitlines():
        m = re.match(r"^(\d{4}-\d{2}-\d{2});([-\d,]+);", line)
        if m:
            out[m.group(1)] = float(m.group(2).replace(",", "."))
    return out


def ust(year):
    url = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all"
           f"?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv")
    rows = list(csv.DictReader(io.StringIO(requests.get(url, headers=UA, timeout=30).text)))
    out = {}
    for r in rows:
        d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date().isoformat()
        out[d] = {k: float(v) for k, v in r.items() if k != "Date" and v}
    return out


def estr(n=10):
    url = f"https://data-api.ecb.europa.eu/service/data/EST/B.EU000A2X2A25.WT?lastNObservations={n}&format=csvdata"
    rows = list(csv.DictReader(io.StringIO(requests.get(url, headers=UA, timeout=30).text)))
    return {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in rows}


def sofr(n=10):
    j = requests.get(f"https://markets.newyorkfed.org/api/rates/secured/sofr/last/{n}.json", headers=UA, timeout=30).json()
    return {r["effectiveDate"]: r["percentRate"] for r in j["refRates"]}


def euribor():
    t = requests.get("https://www.euribor-rates.eu/en/current-euribor-rates/", headers=UA, timeout=30).text
    out = {}
    for name in ["1 week", "1 month", "3 months", "6 months", "12 months"]:
        m = re.search(r"Euribor " + name + r".{0,400}?(-?\d+\.\d{3}) %", t, re.S)
        if m:
            out[name] = float(m.group(1))
    dm = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", t)
    return dict(values=out, date_hint=dm.group(1) if dm else None)


def pap_table(url="https://www.wnp.pl/rynki/rentownosci-obligacji-wybranych-panstw,1117879.html"):
    """PAP 'Rentowności obligacji wybranych państw' (republished by wnp.pl): current + levels 1D/5D/1M/3M/12M ago."""
    from bs4 import BeautifulSoup
    s = BeautifulSoup(requests.get(url, headers=UA, timeout=30).text, "lxml")
    rows = [[c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])] for t in s.find_all("table") for r in t.find_all("tr")]
    hdr = next(r for r in rows if len(r) >= 8 and r[3] == "1D")
    out = dict(date=hdr[2], cols=hdr[2:], url=url, data={})
    num = lambda x: float(x.replace(",", ".")) if x and x not in ("-", "") else None
    for r in rows:
        if len(r) >= 8 and r[1].endswith("-letnie"):
            out["data"].setdefault(r[0], {})[r[1].split("-")[0] + "Y"] = [num(x) for x in r[2:8]]
    return out


def main():
    start = sys.argv[1] if len(sys.argv) > 1 else "2026-08-01"
    out = {"bund": {}, "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    for T in (1, 2, 3, 5, 7, 10, 15, 20, 30):
        out["bund"][str(T)] = bund(T, start)
    u = ust(2026)
    out["ust"] = {d: v for d, v in u.items() if d >= start}
    prev_p = ROOT / "data" / "core" / "core_rates.json"
    prev = json.loads(prev_p.read_text()) if prev_p.exists() else {}
    for key, fn in (("estr", estr), ("sofr", sofr), ("euribor", euribor), ("pap", pap_table)):
        try:
            out[key] = fn()
        except Exception as e:  # keep the last good value if a source times out
            print(f"{key}: fetch failed ({type(e).__name__}); keeping previous value")
            out[key] = prev.get(key)
    p = ROOT / "data" / "core" / "core_rates.json"
    p.write_text(json.dumps(out, indent=0))
    last = max(out["bund"]["10"])
    print("bund last", last, {T: out["bund"][T].get(last) for T in out["bund"]})
    lu = max(out["ust"])
    print("ust last", lu, out["ust"][lu])
    print("estr", list(out["estr"].items())[-2:], "sofr", list(out["sofr"].items())[:2], "euribor", out["euribor"])


if __name__ == "__main__":
    main()
