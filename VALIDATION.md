# Validation

## Source checks

- The primary agent was recovered from Team 13's `group_2023_13_230603_192731.py` competition entry.
- Only 17 Chinese comments were translated. Python AST equality with the original archived entry passed, including runtime strings and executable expressions.
- `paper/pkudsa-group13.docx` is byte-identical to the original `pkudsa-group13(2).docx`. The PDF was exported from this read-only copy.
- All retained Python files compile and their actual comments are in English.

## Strategy checks

`python -m unittest discover -s tests -v` passed four checks:

1. The two-ply score difference matches an independent enumeration using the course simulator's cascades and best opponent reply, on the fixed seed-42 board.
2. A low-valued search continuation can select a same-color exchange that leaves the full board unchanged.
3. The sparse-position override can accept the searched action instead of passing.
4. A three-ply tree adds our first score, subtracts the opponent's reply and adds our second score; it can reject the move with the largest immediate score.

## Complete local games

The recovered agent and course greedy baseline completed both seed-42 games without runner errors:

| Slot 0 | Slot 1 | Total turns | Score in slot order |
| --- | --- | --- | --- |
| Team 13 agent | Greedy baseline | 200 | 2967 : 1858 |
| Greedy baseline | Team 13 agent | 200 | 1670 : 3072 |

`data/replay1.json` was regenerated from the first game above. It is not an unverified replay attributed to an arbitrary player file.

These are local sanity checks against one baseline and seed, not a rerun of the historical ladder or knockout competition. Browser interaction was not retested. The report's -4 threshold and the archived agent's 6 threshold remain unchanged and are documented as a version difference.
