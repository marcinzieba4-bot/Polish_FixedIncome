"""Assemble April 2026 day specs (market part) from the agents' fixings.json + curves.json; merge facts from facts_days.json.
Same rules as build_specs_mar.py; April specifics: 31 Mar index portfolios from the 1 Apr spec, PS0731 added to the
fixed-rate universe from the 9 Apr spec (first BondSpot fixing on 8 Apr), Easter (no session 3 and 6 Apr)."""
import json, datetime as dt, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user-Polish-FixedIncome/24a3fc3c-8e3f-5cce-b7fb-dcdc0e9e199e/scratchpad')
REPO = pathlib.Path('/home/user/Polish_FixedIncome')
FX = json.load(open(SP / 'agent_apr_fix/fixings.json'))
CV = {**json.load(open(SP / 'agent_apr_curves1/curves.json')), **json.load(open(SP / 'agent_apr_curves2/curves.json'))}
FD = json.load(open(SP / 'apr/facts_days.json')) if (SP / 'apr/facts_days.json').exists() else {}
J = SP / 'apr'
PLN = dict(PL='Polska', HU='Węgry', CZ='Czechy', TR='Turcja', IE='Irlandia', IT='Włochy', PT='Portugalia', ES='Hiszpania', DE='Niemcy', FR='Francja', UK='Wielka Brytania')
def dmy(d):
    d = dt.date.fromisoformat(d); return f"{d.day} {d:%b %Y}"
DAYS = [('2026-04-01', '2026-03-31', '2026-03-31'), ('2026-04-02', '2026-04-01', '2026-04-01'), ('2026-04-07', '2026-04-02', '2026-04-06'),
        ('2026-04-08', '2026-04-07', '2026-04-07'), ('2026-04-09', '2026-04-08', '2026-04-08'), ('2026-04-10', '2026-04-09', '2026-04-09'),
        ('2026-04-13', '2026-04-10', '2026-04-12'), ('2026-04-14', '2026-04-13', '2026-04-13'), ('2026-04-15', '2026-04-14', '2026-04-14'),
        ('2026-04-16', '2026-04-15', '2026-04-15'), ('2026-04-17', '2026-04-16', '2026-04-16'), ('2026-04-20', '2026-04-17', '2026-04-19'),
        ('2026-04-21', '2026-04-20', '2026-04-20'), ('2026-04-22', '2026-04-21', '2026-04-21'), ('2026-04-23', '2026-04-22', '2026-04-22'),
        ('2026-04-24', '2026-04-23', '2026-04-23'), ('2026-04-27', '2026-04-24', '2026-04-26'), ('2026-04-28', '2026-04-27', '2026-04-27'),
        ('2026-04-29', '2026-04-28', '2026-04-28'), ('2026-04-30', '2026-04-29', '2026-04-29')]
# Erste dailies that are not a plain "R-dated daily, table headed C" read (see research/notes_curves*.md)
_d = lambda R_, daily, how: dict(src_label=f"LSEG end-of-day interbank bid rates in the Erste Bank Polska Codziennik of {daily}" + how,
                                 published=f"read from the Erste Codziennik of {daily}" + how, audit_note="Only cut-off-day levels are used; bid side (~1-2bp below mid); 7Y not available." + how)
ERSTE = {
 '2026-04-07': _d('2026-04-07', '3 Apr 2026', " (Good Friday issue, tables headed 02.04.2026 = C; the 7 Apr issue is headed 06/04, after C, and is not used)"),
 '2026-04-09': _d('2026-04-09', '9 Apr 2026', " (FRA, CDS and spread read directly; its IRS table repeated the 7 Apr table, so the 8 Apr IRS levels are the 10 Apr issue's 09/04 levels minus its change column, +-1bp)"),
 '2026-04-14': _d('2026-04-14', '15 Apr 2026', " (the 14 Apr issue reprinted the 10 Apr tables and no issue carries a table headed 13.04: 13 Apr levels = the 15 Apr issue's 14.04 levels minus its change column, +-1bp; CDS and the 10Y spread not quoted)"),
 '2026-04-23': _d('2026-04-23', '24 Apr 2026', " (there is no 23 Apr issue: 22 Apr levels = the 24 Apr issue's 23.04 levels minus its change column, +-1bp; only the 22 Apr closes are read; CDS and the 10Y spread not quoted)"),
}
DERIVED_SPREAD = {'2026-04-14', '2026-04-23'}
PS0731 = dict(bonds=[dict(ticker='PS0731', isin='PL0000118998', coupon=4.0, maturity='2031-07-25')],
              note="PS0731 (4.00%, 25 Jul 2031; first issued 18 Mar 2026) added from the 8 Apr 2026 close, its first BondSpot fixing.")
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
        if R == '2026-04-01':
            spec['index_portfolios'] = str(REPO / 'data/snapshots/_inputs/2026-04/index_portfolios_2026-03-31.json')
        if R == '2026-04-09':
            spec['bonds_static_add'] = PS0731
        spec.update(FD.get('_all', {}))
        spec.update(FD.get(R, {}))
        json.dump(spec, open(J / f"specs/{R}.json", 'w'), indent=1, ensure_ascii=False)
        print(R, C, 'polstr', pd_, px['polstr'], 'irs', irs['pillars'], 'fra', fra.get('1x4'), fra.get('9x12'), 'pap rows', len(data))
