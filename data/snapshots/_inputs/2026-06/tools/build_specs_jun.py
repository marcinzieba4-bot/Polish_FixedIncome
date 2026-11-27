"""Assemble June 2026 day specs (market part) from the agents' fixings.json + curves.json; merge facts from facts_days.json.
Same rules as build_specs_may.py; June specifics: 29 May index portfolios from the 1 Jun spec; no new fixed-rate line in June;
no Polish session on 4 Jun (Corpus Christi), so the 5 Jun report uses the 3 Jun close."""
import json, datetime as dt, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user-Polish-FixedIncome/f82df0b1-d4bb-529b-9fb4-ff4ddefccef7/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
FX = json.load(open(SP / 'agent_jun_fix/fixings.json'))
CV = {**json.load(open(SP / 'agent_jun_curves1/curves.json')), **json.load(open(SP / 'agent_jun_curves2/curves.json'))}
FD = json.load(open(SP / 'jun/facts_days.json')) if (SP / 'jun/facts_days.json').exists() else {}
J = SP / 'jun'
PLN = dict(PL='Polska', HU='Węgry', CZ='Czechy', TR='Turcja', IE='Irlandia', IT='Włochy', PT='Portugalia', ES='Hiszpania', DE='Niemcy', FR='Francja', UK='Wielka Brytania')
def dmy(d):
    d = dt.date.fromisoformat(d); return f"{d.day} {d:%b %Y}"
DAYS = [('2026-06-01', '2026-05-29', '2026-05-31'), ('2026-06-02', '2026-06-01', '2026-06-01'), ('2026-06-03', '2026-06-02', '2026-06-02'),
        ('2026-06-05', '2026-06-03', '2026-06-04'), ('2026-06-08', '2026-06-05', '2026-06-07'), ('2026-06-09', '2026-06-08', '2026-06-08'),
        ('2026-06-10', '2026-06-09', '2026-06-09'), ('2026-06-11', '2026-06-10', '2026-06-10'), ('2026-06-12', '2026-06-11', '2026-06-11'),
        ('2026-06-15', '2026-06-12', '2026-06-14'), ('2026-06-16', '2026-06-15', '2026-06-15'), ('2026-06-17', '2026-06-16', '2026-06-16'),
        ('2026-06-18', '2026-06-17', '2026-06-17'), ('2026-06-19', '2026-06-18', '2026-06-18'), ('2026-06-22', '2026-06-19', '2026-06-21'),
        ('2026-06-23', '2026-06-22', '2026-06-22'), ('2026-06-24', '2026-06-23', '2026-06-23'), ('2026-06-25', '2026-06-24', '2026-06-24'),
        ('2026-06-26', '2026-06-25', '2026-06-25'), ('2026-06-29', '2026-06-26', '2026-06-28'), ('2026-06-30', '2026-06-29', '2026-06-29')]
# Erste dailies that are not a plain "R-dated daily, table headed C" read (see research/notes_curves*.md)
_d = lambda daily, how: dict(src_label=f"LSEG end-of-day interbank bid rates in the Erste Bank Polska Codziennik of {daily}" + how,
                             published=f"read from the Erste Codziennik of {daily}" + how, audit_note="Only cut-off-day levels are used; bid side (~1-2bp below mid); 7Y not available." + how)
ERSTE = {}  # TODO fill from the curves notes
DERIVED_SPREAD = set()
ADD = {}  # no new fixed-rate line in June (BondSpot fixings 29 May - 29 Jun)
if __name__ == '__main__':
    (J / 'specs').mkdir(parents=True, exist_ok=True)
    for R, C, I in DAYS:
        v = CV[R]; f = FX['by_date'][C]
        pt = v['pap_table']
        alts = [k for k in v if k.startswith('pap_table_') and isinstance(v[k], dict) and v[k].get('rows')]
        if alts and sum(bool(r.get('after_C')) for r in pt['rows'].values()) > 3:
            pt = v[alts[0]]
        data, stamps = {}, {}
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
        K = json.load(open(J / f"raw/core_{C.replace('-', '')}.json"))
        u = K['ust'][max(d for d in K['ust'] if d <= C)]
        data['USA'] = {'2Y': [u['2 Yr'], None, None, None, None, None], '5Y': [u['5 Yr'], None, None, None, None, None], '10Y': [u['10 Yr'], None, None, None, None, None]}
        extra = v.get('pap_extra', '')
        pap = dict(date=f"{dmy(C)} closes (PAP/Bloomberg table published {pt['published']}{extra}; US = US Treasury {dmy(C)} curve; live US/Japan quotes excluded)",
                   cols=["close", "1D", "5D", "1M", "3M", "12M"], url=pt['url'], data=data, row_stamps=stamps, published=pt['published'])
        s = v['irs_src']
        hdr = dt.date.fromisoformat(C).strftime('%d.%m.%Y')
        irs = dict(pillars=v['irs'], header=hdr, src_label=f"LSEG end-of-day interbank bid rates in the Erste Bank Polska Codziennik of {dmy(R)}",
                   published=f"read from the Erste Codziennik of {dmy(R)} (table headed {hdr})", short='LSEG bid via Erste', missing_note='7Y not available.',
                   audit_note='Only the cut-off-day levels are used; bid side (~1-2bp below mid); 7Y not available.')
        irs.update(ERSTE.get(R, {}))
        fra = v['fra']; cds = v['cds5y']; spr = v['pl_bund_10y']
        if R in DERIVED_SPREAD:  # spread rebuilt from a later daily's change column: not quoted
            spr = None
        pols = sorted((d, x) for d, x in FX['polstr'].items() if x['published_by_convention'] < R)
        pd_, px = pols[-1]
        if len(pols) > 1 and pd_[5:7] != (dt.date.fromisoformat(pd_) + dt.timedelta(days=3)).isoformat()[5:7] and px['polstr'] < pols[-2][1]['polstr'] - 0.25:
            pd_, px = pols[-2]  # month-end liquidity dip: use the prior index date (as at year-end)
        spec = dict(report_date=R, market_cutoff=C, info_cutoff=I, settlement_note="normal T+2",
                    wibor=f['wibor'], polstr=dict(date=pd_, value=px['polstr']), irs=irs, fra=fra, cds5y=cds, pl_bund_10y=spr,
                    euribor=f['euribor'], pribor=f['pribor'], bubor=f['bubor'], fx=f['nbp_fx'],
                    fpc={t: dict(close=x['close'], vol=x['vol'], traded=x['traded'], last_trade_date=x.get('last_trade_date')) for t, x in f['fpc'].items()},
                    pap=pap, pap_close=v['pap_close'])
        if R == '2026-06-01':
            spec['index_portfolios'] = str(REPO / 'data/snapshots/_inputs/2026-05/index_portfolios_2026-05-29.json')
        if R in ADD:
            spec['bonds_static_add'] = ADD[R]
        spec.update(FD.get('_all', {}))
        spec.update(FD.get(R, {}))
        json.dump(spec, open(J / f"specs/{R}.json", 'w'), indent=1, ensure_ascii=False)
        print(R, C, 'polstr', pd_, px['polstr'], 'irs', irs['pillars'], 'fra', fra.get('1x4'), fra.get('9x12'), 'pap rows', len(data))
