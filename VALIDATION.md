# Validation

## Source checks

- The primary agent was recovered from Team 13's `group_2023_13_230603_192731.py` competition entry.
- Only 17 Chinese comments were translated. Python AST equality with the original archived entry passed, including runtime strings and executable expressions.
- `paper/pkudsa-group13.docx` is byte-identical to the original `pkudsa-group13(2).docx`. The PDF was exported from this read-only copy.
- All retained Python files compile and their actual comments are in English.

## Strategy checks

`python -m unittest discover -s tests -v` passed five checks:

1. The two-ply score difference matches an independent enumeration using the course simulator's cascades and best opponent reply, on the fixed seed-42 board.
2. A low-valued search continuation can select a same-color exchange that leaves the full board unchanged.
3. The sparse-position override can accept the searched action instead of passing.
4. A three-ply tree adds our first score, subtracts the opponent's reply and adds our second score; it can reject the move with the largest immediate score.
5. HTML-like text in replay metadata stays inside the JSON payload rather than becoming an executable script.

## Complete local games

The recovered agent and course greedy baseline completed both seed-42 games without runner errors:

| Slot 0 | Slot 1 | Total turns | Score in slot order |
| --- | --- | --- | --- |
| Team 13 agent | Greedy baseline | 200 | 2967 : 1858 |
| Greedy baseline | Team 13 agent | 200 | 1670 : 3072 |

`data/replay1.json` was regenerated from the first game above. It is not an unverified replay attributed to an arbitrary player file.

## Offline replay viewer

`python run_match.py --no-browser` and the Windows `run_match.cmd --no-browser` entry point both completed a full seed-42 match, including when the launcher was invoked from outside the repository. The result was 200 turns, with Team 13 scoring 2967 and the baseline scoring 1858.

The generated `outputs/match.html` was opened in a separate headless Edge profile using the actual local-file URL. Checks passed for automatic replay loading, team names, rendered pieces, pause, previous/next frame, jump bounds, invalid playback speeds and automatic stopping at the last frame. The final displayed scores matched the game runner, and no JavaScript runtime errors were observed. The viewer uses bundled local assets.

These are local sanity checks against one baseline and seed, not a rerun of the historical ladder or knockout competition. The report's -4 threshold and the archived agent's 6 threshold remain unchanged and are documented as a version difference.
