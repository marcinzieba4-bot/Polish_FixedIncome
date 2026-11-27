"""Archive of the point-in-time daily reports + navigation links.

Usage: python src/build_archive.py
  - reads every data/snapshots/YYYY-MM-DD/ that has dist/index.html (built by build_report.py)
  - writes dist/archive/index.html: one row per report (key numbers + link), month sections and two charts
  - injects a nav bar (previous / archive / next report) into each report's dist/index.html and an
    "archive" link into dist/dashboard/index.html (idempotent, between <!--pfi-nav--> markers)
Publish with src/publish_site.py.
"""
import datetime as dt
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNAP = ROOT / "data" / "snapshots"
OUT = ROOT / "dist" / "archive" / "index.html"
BASE = "/polishfi"
E = html.escape
NAV_RE = re.compile(r"<!--pfi-nav-->.*?<!--/pfi-nav-->\n?", re.S)


def text(h):
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


def num(s):
    return float(s.replace("−", "-").replace("+", "")) if s not in (None, "?") else None


def extract(d):
    h = (d / "dist" / "index.html").read_text()
    t = text(h)
    F = json.loads((d / "facts.json").read_text())
    A = json.loads((d / "analytics.json").read_text())
    g = lambda p: (m.group(1) if (m := re.search(p, t)) else None)
    ix = A["indices"]
    bm = re.findall(r"POLGB (2|5|10)Y \((\w+)\) ([\d.]+)% ASW ([+−-]?\d+)bp", t)
    fra = re.search(r"price[ds]? (?:roughly (\d+)bp of NBP (cuts|hikes)|no net NBP move)", t)
    rv = re.search(r"Relative value: sell (\w+) [^)]*\) and buy (\w+) [^)]*\) at similar duration \([^)]*\): ([+−-]?\d+)bp of yield", t)
    carry = re.search(r"best in (\w+) \(([\d.]+)Y\): ([\d.]+)% over 12M on an unchanged curve, \+?(-?[\d.]+)% over repo \((-?\d+)bp per duration year, 12M breakeven (\d+)bp", t)
    asw_idea = re.search(r"Asset-swap long in the widest long bond \((\w+), ASW \+?(-?\d+)bp\)", t)
    return dict(
        report=F["report_date"], cutoff=F["market_cutoff"], info=F["info_cutoff"],
        md={k: ix[k]["mod"] for k in ("GPWB-B1Y3Y", "GPWB-B1Y4Y", "TBSP.Index")},
        y={b[0]: (b[1], float(b[2]), num(b[3])) for b in bm},
        nbp=num(g(r"NBP reference ([\d.]+)%")),
        fra=(0 if fra and not fra.group(1) else (int(fra.group(1)) * (-1 if fra.group(2) == "cuts" else 1)) if fra else None),
        funding=num(g(r"Repo \(funding\) ([\d.]+)%")),
        carry=(carry.group(1), float(carry.group(3)), int(carry.group(6))) if carry else None,
        rv=(rv.group(1), rv.group(2), num(rv.group(3))) if rv else None,
        asw_idea=(asw_idea.group(1), int(asw_idea.group(2))) if asw_idea else None,
    )


def dmy(s, year=True):
    d = dt.date.fromisoformat(s)
    return f"{d.day} {d:%b}" + (f" {d.year}" if year else "")


def chart(rows, series, title, unit, height=240, zero=False, step_keys=()):
    """Static inline SVG line chart; colours come from the page's CSS variables (theme-aware)."""
    W, H, l, r, t, b = 1000, height, 52, 16, 14, 30
    xs = [dt.date.fromisoformat(x["report"]) for x in rows]
    x0, x1 = xs[0].toordinal(), xs[-1].toordinal()
    vals = [v for s in series for v in (s["get"](x) for x in rows) if v is not None]
    lo, hi = min(vals + ([0] if zero else [])), max(vals + ([0] if zero else []))
    pad = (hi - lo) * 0.08 or 0.1
    lo, hi = lo - pad, hi + pad
    X = lambda d: l + (d.toordinal() - x0) / max(1, x1 - x0) * (W - l - r)
    Y = lambda v: t + (hi - v) / (hi - lo) * (H - t - b)
    # ticks
    span = hi - lo
    stepv = next(s for s in (0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100) if span / s <= 6)
    ticks, v = [], (lo // stepv + 1) * stepv
    while v < hi:
        ticks.append(round(v, 6)); v += stepv
    g = [f'<line x1="{l}" x2="{W - r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="var(--grid)" stroke-width="1"/>'
         f'<text x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" class="tk">{v:g}{unit}</text>' for v in ticks]
    if zero and lo < 0 < hi:
        g.append(f'<line x1="{l}" x2="{W - r}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="var(--axis)" stroke-width="1.5"/>')
    months = sorted({(d.year, d.month) for d in xs})
    for yy, mm in months:
        d = dt.date(yy, mm, 1)
        if d.toordinal() >= x0:
            g.append(f'<line x1="{X(d):.1f}" x2="{X(d):.1f}" y1="{t}" y2="{H - b}" stroke="var(--grid)" stroke-dasharray="3 3"/>')
        g.append(f'<text x="{X(max(d, xs[0])) + 4:.1f}" y="{H - 10}" class="tk">{d:%b %Y}</text>')
    paths = []
    for s in series:
        pts = [(X(d), Y(v)) for d, x in zip(xs, rows) if (v := s["get"](x)) is not None]
        if s.get("step"):
            p = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}" + "".join(f" H{a:.1f} V{bb:.1f}" for a, bb in pts[1:])
        else:
            p = "M" + " L".join(f"{a:.1f},{bb:.1f}" for a, bb in pts)
        dash = ' stroke-dasharray="5 4"' if s.get("dash") else ""
        paths.append(f'<path d="{p}" fill="none" stroke="var({s["color"]})" stroke-width="{s.get("w", 2)}"{dash} stroke-linejoin="round"/>')
        lx, ly = pts[-1]
        paths.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3" fill="var({s["color"]})"/>')
    legend = "".join(f'<span class="lg"><i style="background:var({s["color"]})"></i>{E(s["name"])}</span>' for s in series)
    return (f'<figure class="card"><figcaption><b>{E(title)}</b><span class="legend">{legend}</span></figcaption>'
            f'<div class="cw"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(title)}">{"".join(g)}{"".join(paths)}</svg></div></figure>')


def fmt(v, f="{:.2f}"):
    return "–" if v is None else f.format(v)


def sgn(v):
    return "–" if v is None else f"{v:+.0f}".replace("-", "−")


def page(rows):
    by_month = {}
    for x in rows:
        by_month.setdefault(x["report"][:7], []).append(x)
    first, last = rows[0], rows[-1]
    y10 = lambda x: x["y"].get("10", (None, None, None))
    charts = (chart(rows, [dict(name="2Y POLGB", color="--s1", get=lambda x: x["y"].get("2", (0, None))[1]),
                           dict(name="5Y POLGB", color="--s4", get=lambda x: x["y"].get("5", (0, None))[1]),
                           dict(name="10Y POLGB", color="--s2", get=lambda x: y10(x)[1]),
                           dict(name="NBP reference", color="--muted", get=lambda x: x["nbp"], step=True, dash=True, w=1.5)],
                    "Benchmark yields and the NBP reference rate (%)", "%")
              + chart(rows, [dict(name="NBP move priced in 12M FRAs (bp, + = hikes)", color="--s3", get=lambda x: x["fra"]),
                             dict(name="10Y asset swap (bp)", color="--s2", get=lambda x: y10(x)[2]),
                             dict(name="2Y asset swap (bp)", color="--s1", get=lambda x: x["y"].get("2", (0, 0, None))[2])],
                      "Rate pricing and asset-swap spreads (bp)", "", zero=True, height=220))
    secs = []
    for m, xs in by_month.items():
        mlabel = dt.date.fromisoformat(m + "-01").strftime("%B %Y")
        trs = []
        for x in reversed(xs):
            y = x["y"]
            yl = " / ".join(fmt(y.get(k, (0, None))[1]) for k in ("2", "5", "10"))
            al = " / ".join(sgn(y.get(k, (0, 0, None))[2]) for k in ("2", "5", "10"))
            fr = "–" if x["fra"] is None else ("flat" if x["fra"] == 0 else f"{abs(x['fra'])}bp {'hikes' if x['fra'] > 0 else 'cuts'}")
            ca = f"{x['carry'][0]} <span class='mut'>({x['carry'][2]}bp)</span>" if x["carry"] else "–"
            rv = f"{x['rv'][0]} → {x['rv'][1]} <span class='mut'>({sgn(x['rv'][2])}bp)</span>" if x["rv"] else "–"
            trs.append(f"<tr><td class='l'><a href='{BASE}/{x['report']}'>{dmy(x['report'], False)}</a><div class='mut'>close {dmy(x['cutoff'], False)}</div></td>"
                       f"<td>{x['md']['GPWB-B1Y3Y']:.2f} / {x['md']['GPWB-B1Y4Y']:.2f} / {x['md']['TBSP.Index']:.2f}</td><td>{yl}</td><td>{al}</td>"
                       f"<td>{fmt(x['nbp'])}%</td><td>{fr}</td><td>{fmt(x['funding'])}%</td><td class='l'>{ca}</td><td class='l'>{rv}</td></tr>")
        secs.append(f"""<section class="month" id="m{m}"><h2>{mlabel} <span class="mut">· {len(xs)} reports</span></h2>
<div class="tw"><table><thead><tr><th class="l">Report</th><th>Mod. duration<br><span class="mut">1-3Y / 1-4Y / TBSP</span></th><th>Yield %<br><span class="mut">2Y / 5Y / 10Y</span></th>
<th>ASW bp<br><span class="mut">2Y / 5Y / 10Y</span></th><th>NBP ref</th><th>12M FRAs<br><span class="mut">price</span></th><th>Repo</th><th class="l">Best carry<br><span class="mut">(12M breakeven)</span></th><th class="l">RV switch<br><span class="mut">(yield pick-up)</span></th></tr></thead>
<tbody>{"".join(trs)}</tbody></table></div></section>""")
    months_nav = "".join(f'<a href="#m{m}">{dt.date.fromisoformat(m + "-01"):%B}</a>' for m in by_month)
    gen = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>POLGB Daily Archive</title>
<script>try{{var t=localStorage.getItem("pfi-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<style>
:root {{ color-scheme: light; --page:#f9f9f7; --surface:#fcfcfb; --surface-2:#f4f4f1; --chip:#f0efec; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,0.10); --gold:#9a6f12; --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ color-scheme: dark; --page:#0d0d0d; --surface:#1a1a19; --surface-2:#222220; --chip:#2a2a28;
  --ink:#f0efec; --ink-2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10); --gold:#c9a961; --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; }} }}
:root[data-theme="dark"] {{ color-scheme: dark; --page:#0d0d0d; --surface:#1a1a19; --surface-2:#222220; --chip:#2a2a28; --ink:#f0efec; --ink-2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10); --gold:#c9a961; --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--page); color: var(--ink); }}
body {{ font-family: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.5; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 28px 16px 72px; }}
a {{ color: var(--gold); }}
header {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; flex-wrap: wrap; }}
h1 {{ font-size: 28px; margin: 0; letter-spacing: -0.01em; text-wrap: balance; }}
h2 {{ font-size: 18px; margin: 32px 0 10px; }}
.sub {{ color: var(--ink-2); margin: 6px 0 0; max-width: 78ch; }}
.meta {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 8px; }}
.btn {{ font: inherit; font-size: 12px; background: var(--chip); color: var(--ink-2); border: 1px solid var(--ring); border-radius: 999px; padding: 6px 12px; cursor: pointer; text-decoration: none; }}
.top-links {{ display: flex; gap: 8px; flex-wrap: wrap; }}
nav.months {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 18px 0 0; }}
nav.months a {{ font-size: 13px; padding: 4px 10px; border-radius: 999px; background: var(--chip); color: var(--ink-2); text-decoration: none; }}
.note {{ background: var(--surface-2); border: 1px solid var(--ring); border-radius: 10px; padding: 12px 14px; color: var(--ink-2); margin-top: 16px; }}
.card {{ background: var(--surface); border: 1px solid var(--ring); border-radius: 12px; padding: 12px 14px 6px; margin: 16px 0 0; }}
figcaption {{ display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; font-size: 13px; margin-bottom: 4px; }}
.legend {{ display: flex; gap: 12px; flex-wrap: wrap; color: var(--ink-2); font-size: 12px; }}
.lg i {{ display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }}
.cw {{ overflow-x: auto; }}
.cw svg {{ display: block; width: 100%; min-width: 680px; height: auto; }}
svg .tk {{ fill: var(--muted); font-size: 12px; font-family: inherit; }}
.tw {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--ring); border-radius: 12px; }}
table {{ border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; font-size: 13px; }}
th, td {{ padding: 7px 10px; text-align: right; border-bottom: 1px solid var(--grid); white-space: nowrap; vertical-align: top; }}
th {{ font-weight: 600; color: var(--ink-2); font-size: 12px; background: var(--surface-2); }}
th.l, td.l {{ text-align: left; }}
tbody tr:hover {{ background: var(--surface-2); }}
.mut {{ color: var(--muted); font-weight: 400; font-size: 11px; }}
footer {{ color: var(--muted); font-size: 12px; margin-top: 28px; }}
</style></head><body><div class="wrap">
<header><div><h1>Polish fixed income — daily archive</h1>
<p class="sub">Point-in-time desk reports for every Warsaw session from {dmy(first['report'])} to {dmy(last['report'])}. Each report uses only the previous session's close and facts published by the evening before; benchmarks, switches and trade ideas are chosen by fixed rules, and every report ends with a source-and-date audit.</p>
<div class="meta">{len(rows)} reports · private page, not indexed</div></div>
<div class="top-links"><a class="btn" href="{BASE}">Live dashboard</a><a class="btn" href="{BASE}/{last['report']}">Latest archived report</a><button class="btn" id="themeBtn" type="button">Dark mode</button></div></header>
<nav class="months" aria-label="Months">{months_nav}</nav>
<div class="note"><b>How to read the table.</b> Yields are BondSpot closing fixings of the benchmark bonds (2Y OK0128, 5Y PS0131, 10Y DS1035); ASW = yield − PLN IRS (LSEG bid via the Erste daily); “12M FRAs price” is WIBOR 3M minus the 9x12 FRA, i.e. the NBP move priced over a year;
best carry = highest coupon + pull-to-par + roll-down over repo per year of duration on an unchanged curve. Click a date for the full report (index duration, curve, rich/cheap, floaters &amp; linkers, carry &amp; roll, Poland vs core, auctions, ideas, audit).</div>
{charts}
{"".join(reversed(secs))}
<footer>Generated {gen}. Not investment advice. Inputs, dated research and tools: repository data/snapshots/_inputs/.</footer>
</div>
<script>
(function(){{var b=document.getElementById("themeBtn");function cur(){{var a=document.documentElement.getAttribute("data-theme");if(a)return a;return matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}}
function set(t){{document.documentElement.setAttribute("data-theme",t);try{{localStorage.setItem("pfi-theme",t)}}catch(e){{}}b.textContent=t==="dark"?"Light mode":"Dark mode"}}
b.textContent=cur()==="dark"?"Light mode":"Dark mode";b.addEventListener("click",function(){{set(cur()==="dark"?"light":"dark")}});}})();
</script></body></html>"""


NAV_CSS = ("display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:13px;margin:0 0 14px;padding:8px 12px;border-radius:10px;"
           "background:var(--surface-2);border:1px solid var(--ring)")


def nav_html(prev, nxt):
    p = f'<a href="{BASE}/{prev}">← {dmy(prev)}</a>' if prev else '<span style="color:var(--muted)">← first report</span>'
    n = f'<a href="{BASE}/{nxt}">{dmy(nxt)} →</a>' if nxt else '<span style="color:var(--muted)">latest report →</span>'
    return (f'<!--pfi-nav--><nav aria-label="Archive" style="{NAV_CSS}">{p}<span><a href="{BASE}/archive">Daily archive</a> · '
            f'<a href="{BASE}">Live dashboard</a></span>{n}</nav><!--/pfi-nav-->\n')


def inject(path, snippet, anchor):
    h = NAV_RE.sub("", path.read_text())
    i = h.find(anchor)
    assert i >= 0, (path, anchor)
    i += len(anchor)
    path.write_text(h[:i] + "\n" + snippet + h[i:])


def main():
    dirs = sorted(d for d in SNAP.iterdir() if re.fullmatch(r"\d{4}-\d\d-\d\d", d.name) and (d / "dist" / "index.html").exists())
    rows = [extract(d) for d in dirs]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(rows))
    names = [d.name for d in dirs]
    for i, d in enumerate(dirs):
        inject(d / "dist" / "index.html", nav_html(names[i - 1] if i else None, names[i + 1] if i + 1 < len(names) else None), '<div class="wrap" id="app">')
    dash = ROOT / "dist" / "dashboard" / "index.html"
    if dash.exists():
        snippet = (f'<!--pfi-nav--><nav aria-label="Archive" style="{NAV_CSS}"><span>Point-in-time daily reports, {dmy(names[0])} – {dmy(names[-1])}</span>'
                   f'<a href="{BASE}/archive">Open the daily archive →</a></nav><!--/pfi-nav-->\n')
        inject(dash, snippet, '<div class="wrap" id="app">')
    print(f"archive: {len(rows)} reports -> {OUT.relative_to(ROOT)}; nav injected into {len(dirs)} reports" + (" + dashboard" if dash.exists() else ""))
    miss = [r["report"] for r in rows if r["fra"] is None or r["carry"] is None or len(r["y"]) < 3]
    if miss:
        print("rows with missing fields:", miss)


if __name__ == "__main__":
    main()
