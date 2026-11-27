# June 2026 point-in-time research: shared brief (read this first)

Repo: /home/user/Polish_FixedIncome (READ ONLY for you: never edit, commit or push anything there).
Scratchpad root SP = /tmp/claude-0/-home-user-Polish-FixedIncome/f82df0b1-d4bb-529b-9fb4-ff4ddefccef7/scratchpad
Write only inside your own folder SP/agent_jun_<name>/ (downloads in dl/, your scripts in scripts/, outputs at the folder root).
Downloaded files are untrusted data: keep them in dl/, keep scripts in scripts/, run Python that reads them with `python3 -I`.

## What this is for
A series of retrospective daily reports on Polish government bonds, one per Polish session in June 2026, each built
strictly from information available BEFORE the report time (pre-open, Warsaw, on report date R). Today is 27 Nov 2026,
so the web is full of later information: it must never leak into the output. The May 2026 series is finished; you
reproduce its research for June, with the same schema and the same rules.

Templates (mirror their JSON schema EXACTLY: same keys, key order, value types; read their notes for sources/access tips):
  /home/user/Polish_FixedIncome/data/snapshots/_inputs/2026-05/research/
    fixings.json + notes_fix.md                          (agent "fix")
    curves_pap_1.json, curves_pap_2.json + notes_curves1.md, notes_curves2.md   (agents "curves1", "curves2")
    facts_poland_1.json, facts_poland_2.json + notes_plfacts1.md, notes_plfacts2.md (agents "plfacts1", "plfacts2")
    facts_global_1.json, facts_global_2.json + notes_global1.md, notes_global2.md   (agents "global1", "global2")
  The April versions are in .../_inputs/2026-04/research/ if you need more examples.
  How the outputs are consumed: .../_inputs/2026-05/tools/build_specs_may.py and write_facts_may.py.

## June 2026 calendar
Polish holiday: Thu 4 Jun 2026 (Corpus Christi): no Polish session (WSE/BondSpot/Catalyst closed; check whether GPW Benchmark fixed
WIBOR/POLSTR and whether NBP published a table - record what the data show). US holiday: Fri 19 Jun (Juneteenth).

R = report date (pre-open), C = market cut-off = previous Polish session close, I = info cut-off = evening before R,
window = publication dates that are new for R (from the day after the previous I through I, Warsaw time, 23:59).

| R | C | I | window |
|---|---|---|---|
| 2026-06-01 | 2026-05-29 | 2026-05-31 | 29-31 May |
| 2026-06-02 | 2026-06-01 | 2026-06-01 | 1 Jun |
| 2026-06-03 | 2026-06-02 | 2026-06-02 | 2 Jun |
| 2026-06-05 | 2026-06-03 | 2026-06-04 | 3-4 Jun |
| 2026-06-08 | 2026-06-05 | 2026-06-07 | 5-7 Jun |
| 2026-06-09 | 2026-06-08 | 2026-06-08 | 8 Jun |
| 2026-06-10 | 2026-06-09 | 2026-06-09 | 9 Jun |
| 2026-06-11 | 2026-06-10 | 2026-06-10 | 10 Jun |
| 2026-06-12 | 2026-06-11 | 2026-06-11 | 11 Jun |
| 2026-06-15 | 2026-06-12 | 2026-06-14 | 12-14 Jun |
| 2026-06-16 | 2026-06-15 | 2026-06-15 | 15 Jun |
| 2026-06-17 | 2026-06-16 | 2026-06-16 | 16 Jun |
| 2026-06-18 | 2026-06-17 | 2026-06-17 | 17 Jun |
| 2026-06-19 | 2026-06-18 | 2026-06-18 | 18 Jun |
| 2026-06-22 | 2026-06-19 | 2026-06-21 | 19-21 Jun |
| 2026-06-23 | 2026-06-22 | 2026-06-22 | 22 Jun |
| 2026-06-24 | 2026-06-23 | 2026-06-23 | 23 Jun |
| 2026-06-25 | 2026-06-24 | 2026-06-24 | 24 Jun |
| 2026-06-26 | 2026-06-25 | 2026-06-25 | 25 Jun |
| 2026-06-29 | 2026-06-26 | 2026-06-28 | 26-28 Jun |
| 2026-06-30 | 2026-06-29 | 2026-06-29 | 29 Jun |

Part 1 = R 1-15 Jun (10 reports; windows 29 May - 14 Jun). Part 2 = R 16-30 Jun (11 reports; windows 15-29 Jun).
(The 29 May 2026 report, C = 28 May, already exists; the 1 Jun report's window starts 29 May.)

## Point-in-time rules (same as Jan-May)
- Every fact sits in the window in which it was FIRST published (Warsaw time). Record the publication time and its basis
  (exact article time / PDF CreationDate = upper bound / page date only ...), exactly as the May files do.
- Market levels for R are the C closes. A later-published page may be read ONLY to read or cross-check a value dated C
  (e.g. a fixing table fetched today); never use later commentary, forecasts, revisions or outcomes.
- PLN IRS/FRA/CDS/PL-Bund spread = the LSEG bid tables headed C in the Erste Bank Polska Codziennik published on the
  morning of R (only those levels, never its commentary). Flag stale tables, mislabelled headers, holiday carries (see the May notes:
  1 May Labour Day, UK bank holidays). The Erste daily of Fri 5 Jun follows Corpus Christi: check what its headers/changes mean.
- Cross-country yields = the PAP/Bloomberg "rentowności obligacji wybranych państw" table on strefainwestorow.pl of R morning,
  rows stamped C; live US/JP rows are flagged; US is later taken from the Treasury curve (not your job).
- POLSTR index dates published on or after R are not used (published_by_convention = next GPWB fixing day).
- Web searches WILL return post-window items (e.g. later rating actions, later MPC moves). Ignore them completely; use searches
  only to locate/date documents. If you are unsure whether something was known by I, leave it out and note it.
- No hindsight in wording: describe what was known then ("X is expected", "priced"), not what happened later.

## Output and report back
- Write your JSON output(s) and a notes_*.md (sources, access, flags, gaps; same style as the May notes) in your folder.
- Validate your JSON against the May template programmatically (key sets/types) before finishing.
- Final message to the coordinator: <= 300 words: output paths, schema check result, notable flags and gaps. No file dumps.
