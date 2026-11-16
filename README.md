# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/besan11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/besan11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB chess engine for the make.fun tiny-chess-01 bounty: the strongest chess engine in 4,096 bytes of Python.

## Run it

```sh
python3 main.py
```

## Engine

`main.py` is the whole engine (4,031 bytes, LZMA-packed from `engine.py`).
0x88 board, negamax alpha-beta with iterative deepening to a fixed node
budget (60,000 nodes/move, deterministic — no clock, no unseeded
randomness, so replays play the same moves). Transposition table with
Zobrist keys, killer + history move ordering, MVV-LVA captures, promotion
ordering, quiescence over captures/promotions (all evasions in check).
Evaluation: material + piece-square tables, bishop-pair bonus, tapered
king (middlegame safety blended into endgame centralisation by game
phase), insufficient-material and repetition/fifty-move draws scored 0.

`engine.py` is the readable source the packed `main.py` was compressed
from (kit `makefun compress`).

## Size rule

- `main.py` is at most 4,096 bytes as committed, Python 3.13, stdlib only.
- The rest of the tree (README, LICENSE) is at most 8,192 bytes in all.

## Local results (practice trials, 6 games each)

| trial | points | Elo |
|-------|--------|-----|
| 0 | 2.0/6 | 1099 |
| 1 | 2.5/6 | 1191 |
| 2 | 1.5/6 | 997 |
| mean | 2.0/6 | ~1096 |

Practice floor is 1154 Elo (2.5/6). The engine sits just below it on
average and clears it on some instances. It beats the depth-2 and
depth-3 house engines most games and takes games off depth-4 and the
node-limited engines, but does not match the sunfish 4 KB baseline
(mean ~1365 Elo).

---

<sub>Entered on [make.fun](https://make.fun/?ref=jpgk45b3&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
