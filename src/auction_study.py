"""Auction-cycle study: how the POLGB curve trades around MoF auctions.

1) (optional) extract 2026 operations from the MoF wholesale-bond database (Obligacje_Hurtowe.xlsm,
   https://www.gov.pl/web/finanse/bony-i-obligacje-hurtowe1)  ->  data/market/mof_operations_2026.json
2) average daily change of a 2-10Y basket yield by session relative to each sale/switch auction
   (BondSpot closing fixings from fetch_history.py)  ->  data/analytics/auction_cycle.json

Usage: python src/auction_study.py [--xlsm path/to/Obligacje_Hurtowe.xlsm]
"""
import collections
import datetime as dt
import json
import pathlib
import statistics as st
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASKET = ["OK0129", "WS0429", "PS0729", "DS1029", "PS0130", "PS0730", "DS1030", "PS0131", "PS0731",
          "DS0432", "DS1033", "DS1034", "DS1035"]


def extract_ops(xlsm):
    import openpyxl
    ws = openpyxl.load_workbook(xlsm, read_only=True, data_only=True)["Operacje"]
    hdr, agg = None, collections.OrderedDict()
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            hdr = r
            continue
        d = dict(zip(hdr, r))
        if d["DataTransakcji"] and d["DataTransakcji"] >= dt.datetime(2026, 1, 1):
            agg.setdefault((d["DataTransakcji"].date().isoformat(), d["TypTransakcji"], d["TypOperacji"]), []).append(d)
    out = [dict(date=k[0], type=k[1], op=k[2],
                lines=[dict(series=x["Seria"], sold=x["SprzedażLubOdkupŁącznie"], demand=x["PopytŁączny"],
                            avg_yld=(x["RentŚr"] * 100 if x["RentŚr"] else None)) for x in v]) for k, v in agg.items()]
    (ROOT / "data" / "market" / "mof_operations_2026.json").write_text(json.dumps(out, indent=1, default=str))
    return out


def main():
    snap = pathlib.Path(sys.argv[sys.argv.index("--snap") + 1]) if "--snap" in sys.argv else None
    if "--xlsm" in sys.argv:
        ops = extract_ops(sys.argv[sys.argv.index("--xlsm") + 1])
    elif snap:
        ops = json.loads((snap / "mof_operations_2025H2.json").read_text())
    else:
        ops = json.loads((ROOT / "data" / "market" / "mof_operations_2026.json").read_text())
    h = json.loads(((snap / "fixing_history.json") if snap else (ROOT / "data" / "market" / "fixing_history.json")).read_text())
    days = sorted(h)
    global BASKET
    if snap:  # point-in-time basket: fixed-rate bonds 1.5-11Y to maturity that existed in the window
        cand = {t for d in days for t in h[d] if t[:2] in ("OK", "PS", "DS", "WS")}
        def ttm(t):
            return (dt.date(2000 + int(t[4:6]), int(t[2:4]), 25) - dt.date.fromisoformat(days[-1])).days / 365.25
        BASKET = sorted(t for t in cand if 1.5 <= ttm(t) <= 11 and sum(t in h[d] for d in days) >= 0.9 * len(days))

    def avg(d):
        v = [h[d][t][1] for t in BASKET if t in h[d] and h[d][t][1] is not None]
        return sum(v) / len(v) if len(v) >= max(5, len(BASKET) - 2) else None

    aucs = sorted({o["date"] for o in ops if o["type"] == "S" and o["op"] in ("AS", "AZ") and o["date"] >= days[0]})
    buck = {}
    for i in range(1, len(days)):
        a0, a1 = avg(days[i - 1]), avg(days[i])
        if a0 is None or a1 is None:
            continue
        rel = None
        for A in aucs:
            if A in days:
                k = i - days.index(A)
                if -3 <= k <= 2 and (rel is None or abs(k) < abs(rel)):
                    rel = k
        buck.setdefault("other" if rel is None else f"T{rel:+d}", []).append((a1 - a0) * 100)
    out = {k: dict(n=len(v), mean=st.mean(v), median=st.median(v), up_share=sum(x > 0 for x in v) / len(v)) for k, v in buck.items()}
    out["_meta"] = dict(start=days[0], end=days[-1], auctions=aucs, basket=BASKET, total_change_bp=(avg(days[-1]) - avg(days[0])) * 100)
    p = (snap / "auction_cycle.json") if snap else (ROOT / "data" / "analytics" / "auction_cycle.json")
    p.write_text(json.dumps(out, indent=1))
    for k in sorted(out):
        if not k.startswith("_"):
            print(f"{k:6} n={out[k]['n']:2d} mean {out[k]['mean']:+.2f}bp up {out[k]['up_share']:.0%}")


if __name__ == "__main__":
    main()
