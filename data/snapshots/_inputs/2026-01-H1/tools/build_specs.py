"""Assemble day specs (market part) from the agents' fixings.json + curves.json; merge facts from facts_days.json."""
import json, datetime as dt, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user/2b986bc3-1107-5358-8c0f-f544109c09bc/scratchpad')
FX = json.load(open(SP/'agent_jan_fix/fixings.json'))
CV = json.load(open(SP/'agent_jan_curves/curves.json'))
FD = json.load(open(SP/'jan/facts_days.json')) if (SP/'jan/facts_days.json').exists() else {}
J = SP/'jan'
PLN = dict(PL='Polska', HU='Węgry', CZ='Czechy', TR='Turcja', IE='Irlandia', IT='Włochy', PT='Portugalia', ES='Hiszpania', DE='Niemcy', FR='Francja', UK='Wielka Brytania')
def dmy(d):
    d = dt.date.fromisoformat(d); return f"{d.day} {d:%b %Y}"
DAYS = [('2026-01-07','2026-01-05','2026-01-06'),('2026-01-08','2026-01-07','2026-01-07'),('2026-01-09','2026-01-08','2026-01-08'),
        ('2026-01-12','2026-01-09','2026-01-11'),('2026-01-13','2026-01-12','2026-01-12'),('2026-01-14','2026-01-13','2026-01-13'),('2026-01-15','2026-01-14','2026-01-14')]
for R, C, I in DAYS:
    v = CV[R]; f = FX['by_date'][C]
    # PAP table: for R=7 Jan use the 6 Jan edition (all European rows stamped 5 Jan)
    pt = v['pap_table_0106_edition'] if R == '2026-01-07' else v['pap_table']
    data, stamps, notes = {}, {}, []
    for code, row in pt['rows'].items():
        if code not in PLN or row.get('live'):
            continue
        name = PLN[code]; data[name] = {}
        for ten in ('2Y', '3Y', '5Y', '10Y'):
            arr = row.get(ten)
            if not isinstance(arr, list):
                continue
            arr = list(arr)
            if row.get('after_C'):
                d1 = (row.get('d1') or {}).get('y' + ten[:-1])
                arr = [d1, None] + arr[2:]
            data[name][ten] = arr
            st = row.get('stamp'); stamps[f"{name} {ten[:-1]}-letnie"] = st if isinstance(st, str) else (st[0] if st else 'not stamped')
        if not data[name]:
            data.pop(name)
    K = json.load(open(J/f"core_{C.replace('-','')}.json"))
    u = K['ust'][max(d for d in K['ust'] if d <= C)]
    data['USA'] = {'2Y': [u['2 Yr'], None, None, None, None, None], '5Y': [u['5 Yr'], None, None, None, None, None], '10Y': [u['10 Yr'], None, None, None, None, None]}
    extra = {'2026-01-09': ' (edition carries no row stamps; non-live rows taken as 8 Jan closes)',
             '2026-01-13': ' (rows stamped 12 Jan ~17:30-18:00 CET, i.e. near the European close)'}.get(R, '')
    hu = stamps.get('Węgry 3-letnie') or stamps.get('Węgry 5-letnie')
    pap = dict(date=f"{dmy(C)} closes (PAP/Bloomberg table published {pt['published']}{extra}; US = US Treasury {dmy(C)} curve; live US/Japan quotes excluded)",
               cols=["close", "1D", "5D", "1M", "3M", "12M"], url=pt['url'], data=data, row_stamps=stamps, published=pt['published'])
    # IRS
    if R == '2026-01-07':
        a = v['alt_erste_hdr_0601']
        irs = dict(pillars=a['irs_pl'], header='06.01.2026', src_label='LSEG end-of-day interbank bid rates in the Erste Bank Polska Codziennik of 7 Jan 2026',
                   published='read from the Erste Codziennik of 7 Jan 2026 (table headed 06.01.2026)', short='LSEG bid via Erste',
                   missing_note='7Y not available. No table is headed 5 Jan: the 6 Jan table (Polish holiday) shows zero change on every PLN line and differs from the 2 Jan table, so it carries the 5 Jan close.',
                   audit_note='5 Jan close inferred from the 6 Jan table (holiday; all PLN changes 0, levels differ from 2 Jan). Bid side; 7Y not available.')
        fra = a['fra']; cds = a['cds5y'][0]; spr = None
    else:
        s = v['irs_src']
        irs = dict(pillars=v['irs'], header=s['header_date'], src_label=f"LSEG end-of-day interbank bid rates in the Erste Bank Polska Codziennik of {dmy(R)}",
                   published=f"read from the Erste Codziennik of {dmy(R)} (table headed {s['header_date']})", short='LSEG bid via Erste', missing_note='7Y not available.',
                   audit_note='Only the cut-off-day levels are used; bid side (~1-2bp below mid); 7Y not available.')
        fra = v['fra']; cds = v['cds5y']; spr = v['pl_bund_10y']
        if v.get('flags'):
            spr = None
    pols = [(d, x) for d, x in FX['polstr'].items() if x['published_by_convention'] < R]
    pd_, px = max(pols)
    spec = dict(report_date=R, market_cutoff=C, info_cutoff=I,
                settlement_note=("6 Jan 2026 (Epiphany) is not a settlement day" if C == '2026-01-05' else "normal T+2"),
                wibor=f['wibor'], polstr=dict(date=pd_, value=px['polstr']), irs=irs, fra=fra, cds5y=cds, pl_bund_10y=spr,
                euribor=f['euribor'], pribor=f['pribor'], bubor=f['bubor'], fx=f['nbp_fx'],
                fpc={t: dict(close=x['close'], vol=x['vol'], traded=x['traded'], last_trade_date=x.get('last_trade_date')) for t, x in f['fpc'].items()},
                pap=pap, pap_close=v['pap_close'])
    spec.update(FD.get('_all', {}))
    spec.update(FD.get(R, {}))
    json.dump(spec, open(J/f"specs/{R}.json", 'w'), indent=1, ensure_ascii=False)
    print(R, C, 'polstr', pd_, px['polstr'], 'irs', irs['pillars'], 'fra', fra.get('1x4'), fra.get('9x12'), 'pap rows', len(data))
