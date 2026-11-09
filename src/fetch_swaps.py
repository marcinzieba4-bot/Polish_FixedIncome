"""Fetch IBOR swap curves (closing mids + history columns) from BlueGamma public pages.

Curves: PLN (WIBOR), CZK (PRIBOR), HUF (BUBOR), EUR (6M EURIBOR), USD (SOFR), EUR €STR OIS.
The 'Live' column is paywalled; we keep the dated closing columns (last close, -1w, -1m, -1y).
Writes data/core/swaps.json  {ccy: {"dates": [...], "tenors": {years: [v_last, v_1w, v_1m, v_1y]}, "index": {...}}}
"""
import datetime as dt
import json
import pathlib
import re

import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (polish-fi-dashboard)"}
PAGES = {"PLN": "swap-rates/pln-swap-rates", "CZK": "swap-rates/czk-swap-rates", "HUF": "swap-rates/huf-swap-rates",
         "EUR": "euribor-swap-rates", "USD": "usd-swap-rates", "EUR_OIS": "swap-rates/estr-swap-rates"}


def tenor_years(t):
    m = re.match(r"(\d+)\s*(Month|Year)", t)
    if not m:
        return None
    n = int(m.group(1))
    return n / 12 if m.group(2) == "Month" else float(n)


def parse(html):
    s = BeautifulSoup(html, "lxml")
    out = {"tenors": {}, "index": {}, "dates": None}
    for t in s.find_all("table"):
        rows = [[c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])] for r in t.find_all("tr")]
        if rows and rows[0] and rows[0][0] == "Tenor":
            out["dates"] = [re.sub(r"^.*?(\d{2} \w{3} \d{4})$", r"\1", h) for h in rows[0][2:]]
            for r in rows[1:]:
                y = tenor_years(r[0]) if r else None
                if y is None:
                    continue
                vals = [float(v.rstrip("%")) if re.match(r"^-?\d+\.\d+%$", v) else None for v in r[2:]]
                out["tenors"][str(round(y, 4))] = vals
        elif rows and rows[0] and rows[0][0] == "Index":
            for r in rows[1:]:
                if len(r) >= 2:
                    out["index"][r[0]] = r[1]
    txt = s.get_text(" ", strip=True)
    m = re.search(r"Last update:\s*([A-Za-z]+ \d{1,2}, \d{4})", txt)
    out["last_update"] = m.group(1) if m else None
    return out


def main():
    res = {"fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "source": "https://www.bluegamma.io"}
    for ccy, path in PAGES.items():
        r = requests.get(f"https://www.bluegamma.io/{path}", headers=UA, timeout=30)
        p = parse(r.text)
        p["url"] = f"https://www.bluegamma.io/{path}"
        res[ccy] = p
        print(ccy, p["last_update"], p["dates"], {k: v[0] for k, v in list(p["tenors"].items())[:12]})
    (ROOT / "data" / "core" / "swaps.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
