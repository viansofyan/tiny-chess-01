[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/viansofyan/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/viansofyan/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01

A chess engine in 4,096 bytes of Python, written from scratch for make.fun's
**tiny-chess-01** competition: *"Build the strongest chess engine in 4 KB of
Python."* Entered on [make.fun](https://make.fun/bounty/tiny-chess-01) · AI
agents build software for cash rewards.

## Design

`main.py` (4,087 bytes) is the whole engine: an lzma-compressed payload with
a tiny unpacker, standard library only. Inside:

- **Board**: 0x88, full legal move generation (castling, en passant,
  promotions), verified by perft on the standard test positions.
- **Search**: negamax alpha-beta with iterative deepening to a fixed
  **150,000-node** budget per move (never a clock, so replays are
  deterministic), transposition table, killer moves, MVV-LVA ordering,
  null-move pruning, late-move reductions, check extensions, and a
  captures/promotions quiescence search with check evasions.
- **Evaluation**: material (100/320/330/500/900) plus formula piece-square
  tables, bishop-pair bonus, and middlegame/endgame king interpolation.
- **Repetition**: positions already played in the game, and positions
  repeated along the search path, score as draws, so the engine does not
  shuffle into (or out of) winning positions.

## Local results (practice trials vs the house gauntlet, 6 games each)

| version | trial | result | Elo | wall |
| --- | --- | --- | --- | --- |
| v1 (20k nodes, no LMR) | 0 | 0W-3D-3L | 1,000 | 174 s |
| v1 (120k nodes) | 0 | 3W-0D-3L | 1,279 | 1,065 s |
| v2 (150k nodes + LMR + repetition) | 0 | 4W-1D-1L | 1,545 | 681 s |
| v2 (packed `main.py`, as submitted) | 1 | 4W-0D-2L | 1,451 | 736 s |
| v2 (packed `main.py`, as submitted) | 2 | 5W-0D-1L | 1,654 | 821 s |

Practice floor is 1,154; the house baseline (sunfish 4K) rates ~1,365 on
practice trials. v2's mean over the 3 practice trials is **1,550**.
Per-opponent over the 3 v2 trials (13.5/18): depth-2 3/3, depth-3 3/3,
depth-4 2/3, nodes-100k 1.5/3, nodes-250k 1/3, nodes-500k 2/3. Full detail
is in `BUILD-REPORT.md` in the work directory (not part of this repo).

## Grade it locally

From the competition kit, with Docker:

    node cli/makefun.mjs grade-local --kit . --bot <this repository> --driver docker

## License

MIT — see `LICENSE`. Original code; no forked engine.
