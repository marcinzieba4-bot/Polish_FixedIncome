"""Fetch Treasury BondSpot Poland (TBSP) fixing + session summary for one date.

Usage:  python src/fetch_bondspot.py 2026-11-09 [--quotes-date 2026-11-06]

Writes data/market/bondspot_<date>.json with
  fixing[]   : ticker, isin, bid/ask price, bid/ask yield, fixing price & yield
  quotes[]   : best bid/ask of the session summary (used for bonds with no fixing yield)
  repo[]     : special & general repo transactions (rate, term)
  tbills[]   : T-bill bid/ask yields
  tbsp_index : TBSP.Index level
"""
import datetime as dt
import json
import pathlib
import sys

import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://www.bondspot.pl"
UA = {"User-Agent": "Mozilla/5.0 (polish-fi-dashboard)"}


def _num(s):
    s = (s or "").replace("\xa0", "").replace(" ", "").replace(",", ".")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _get(path, d):
    url = f"{BASE}/{path}?date={d:%Y%m%d}&month={d.month}&year={d.year}"
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return url, BeautifulSoup(r.text, "lxml")


def _rows(table):
    return [[c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])] for tr in table.find_all("tr")]


def fetch_fixing(d):
    url, s = _get("fixing_obligacji", d)
    tabs = s.find_all("table")
    level = None
    for r in _rows(tabs[0]):
        if r and r[0].startswith("Warto") and len(r) > 1:
            level = _num(r[1])
    out = []
    if len(tabs) > 2:
        for r in _rows(tabs[2])[1:]:
            if len(r) < 9:
                continue
            out.append(dict(ticker=r[1], isin=r[2], bid=_num(r[3]), ask=_num(r[4]), bid_yld=_num(r[5]),
                            ask_yld=_num(r[6]), fix_price=_num(r[7]), fix_yld=_num(r[8])))
    return url, level, out


def fetch_session(d):
    try:
        url, s = _get("notowania_TBSPoland", d)
    except requests.HTTPError:
        return None, [], [], []
    quotes, repo, tbills = [], [], []
    for t in s.find_all("table"):
        rows = _rows(t)
        if not rows or not rows[0]:
            continue
        head = rows[0][0]
        if head.startswith("PODSUMOWANIE OBROTU - OBLIGACJE PLN"):
            for r in rows[4:]:
                if len(r) >= 4 and r[0] != "RAZEM":
                    quotes.append(dict(ticker=r[0], isin=r[1], bid=_num(r[2]), ask=_num(r[3]),
                                       last=_num(r[7]) if len(r) > 7 else None,
                                       volume=_num(r[9]) if len(r) > 9 else None))
        elif head.startswith("PODSUMOWANIE OBROTU - BONY"):
            for r in rows[4:]:
                if len(r) >= 5 and r[0] != "RAZEM":
                    tbills.append(dict(name=r[0], isin=r[1], days=_num(r[2]), bid_yld=_num(r[3]), ask_yld=_num(r[4])))
        elif head.startswith("TRANSAKCJE WARUNKOWE"):
            for r in rows:
                if len(r) == 8 and r[0] not in ("Nazwa",):
                    repo.append(dict(name=r[0], isin=r[1], term=r[2], days=_num(r[3]), min=_num(r[4]),
                                     max=_num(r[5]), avg=_num(r[6]), nominal_mln=_num(r[7])))
    return url, quotes, repo, tbills


def main():
    d = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    qd = d
    if "--quotes-date" in sys.argv:
        qd = dt.date.fromisoformat(sys.argv[sys.argv.index("--quotes-date") + 1])
    fx_url, level, fixing = fetch_fixing(d)
    s_url, quotes, repo, tbills = fetch_session(qd)
    if not quotes and qd == d:  # today's session summary is only published after the close
        for back in range(1, 6):
            qd = d - dt.timedelta(days=back)
            s_url, quotes, repo, tbills = fetch_session(qd)
            if quotes:
                break
    out = dict(date=d.isoformat(), quotes_date=qd.isoformat(), fixing_url=fx_url, session_url=s_url,
               tbsp_index=level, fixing=fixing, quotes=quotes, repo=repo, tbills=tbills,
               fetched_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    p = ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"data/market/bondspot_{d:%Y%m%d}.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"wrote {p}: {len(fixing)} fixings, {len(quotes)} quotes ({qd}), {len(repo)} repo, TBSP={level}")


if __name__ == "__main__":
    main()
