# news-image-20261121 — BUILD REPORT (round 1)

## Entry

- `main.py` (Python 3.13 stdlib only) draws a newspaper-style poster and
  writes `/output/entry.png`: **29,387 bytes, 1024x1024, PNG valid,
  deterministic** (two runs byte-identical via `cmp`).
- Design: navy header "SATURDAY / 21 NOVEMBER 2026 / THE WORLD IN ONE DAY"
  + 2x3 card grid (tag chip + headline + deck + pictogram) + footer
  "WORLD NEWS – 21 NOVEMBER 2026 – MAKE.FUN". 5x5 bitmap font written
  from scratch; manual PNG encoder (zlib/struct).
- Image viewed twice: date prominent, all 6 headlines fit in 2 lines,
  no garbled text.

## Stories (all verified as Saturday 21 November 2026)

1. IRAN STRIKES US BASES IN BAHRAIN — Tehran says it hit two US bases;
   Bahrain reports a fire at a civilian site, no injuries.
   (oneturn.news/day/2026-11-21)
2. RUSSIAN MISSILE HITS KRYVYI RIH — strike on Zelensky's hometown kills
   two (a paramedic and a boy of 7); missiles also land in Poland.
   (oneturn.news, virginiatimesnow.com)
3. MEXICO CAPTURES CARTEL BOSS — FBI most-wanted Fausto Isidro Meza Flores
   seized in Sinaloa; clashes leave at least 11 dead.
   (oneturn.news, virginiatimesnow.com)
4. NASDAQ PLUNGES 5.3% IN AI SELLOFF — US stocks fall into correction;
   worst week since 2020. (virginiatimesnow.com, medium.com)
5. COP31 TALKS PAST DEADLINE — UN climate summit in Antalya goes into
   overtime with no agreement on fossil fuels.
   (oneturn.news, virginiatimesnow.com)
6. GTA VI SELLS $2.36 BILLION ON DAY ONE — an estimated 24.6 million
   copies sold on launch day. (virginiatimesnow.com)

## Files

`main.py`, `README.md` (3 make.fun badge lines verified byte-for-byte),
`LICENSE` (MIT, SPDX), `.makefun/owner.json` (wallet
`5rM8m83Gjp53ACVY6fzE1HJCWeH34wAtb7F2Pxviec2s`), `BUILD-REPORT.md`.

## Verification

- Kit local check: **4 passed, 1 failed** — fail only `transcripts_present`
  (no `--transcripts`; parent's job at bundle), 14 skipped, 5 at submission.
- Determinism: two runs byte-identical.

## Revision evidence (thinking_revised)

- `main.py` written in 6 appends (6 messages) + **1 edit after the first
  run**: shortened 3 headlines (Mexico, Nasdaq, COP31) that were truncated
  at the 2-line cap, after viewing the screenshot. main.py was
  written/edited by 7 messages.
