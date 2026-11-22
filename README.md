[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jackflank4-lang/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jackflank4-lang/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121/reward?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# news-image-20261121

Sum up 21 November's world news in one image — a make.fun bounty entry.

`main.py` (Python 3.13 standard library only) draws a newspaper-style poster
and writes `/output/entry.png` (1024x1024, deterministic, 29,387 bytes).

## The day: Saturday 21 November 2026

1. **CONFLICT — BAHRAIN:** Iran strikes US bases in Bahrain; Bahrain reports a fire at a civilian site, no injuries.
2. **WAR — UKRAINE:** Russian missile hits Kryvyi Rih, Zelensky's hometown; two killed, missiles also land in Poland.
3. **JUSTICE — MEXICO:** Mexico captures FBI most-wanted cartel boss Fausto Isidro Meza Flores ("Chapo Isidro") in Sinaloa; clashes leave at least 11 dead.
4. **MARKETS — NEW YORK:** Nasdaq plunges 5.3% as the AI sell-off deepens; US stocks fall into correction.
5. **CLIMATE — TURKEY:** COP31 climate talks in Antalya run past deadline with no agreement on fossil fuels.
6. **CULTURE — GAMES:** GTA VI sells an estimated $2.36 billion on day one (24.6 million copies).

Sources: oneturn.news/day/2026-11-21, virginiatimesnow.com daily recap 21 Nov 2026,
Medium strategic brief 21 Nov 2026, ubstandard.com world news.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png`. Two runs are byte-identical.

## License

MIT — see LICENSE.
