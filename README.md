# Strategy Development for a Match-3 Puzzle Game

Team 13's Data Structures and Algorithms course project: **score-difference lookahead with deliberate non-scoring exchanges**, extended to three-ply alpha-beta search and tactical endgame rules.

## Actual project report

[Team 13 course report (PDF)](paper/pkudsa-group13.pdf) · [Original DOCX](paper/pkudsa-group13.docx)

The report is the original `pkudsa-group13(2).docx`, titled “数据结构与算法课程实习作业报告”. It describes multi-level greedy search, score-difference evaluation, board-preserving exchanges, alpha-beta pruning and the team's course competition. Its text is preserved in the original language.

## Main result and decision rule

**[code/group13_agent.py](code/group13_agent.py)** is the Team 13 entry recovered from the course competition-code archive, originally named `group_2023_13_230603_192731.py`. English comments replace the Chinese comments; the executable syntax tree is unchanged.

The strategy follows this progression:

1. `greedy_1` evaluates the total cascade score after each scoring exchange.
2. `greedy_2` evaluates our immediate score minus the opponent's best available reply score, and chooses the exchange with the largest difference.
3. `alpha_beta_pruning` searches three plies (our move, the opponent's reply, our next move). It considers the five highest-scoring children on our turn and three on the opponent's turn, with alpha-beta cutoffs.
4. `select` can decline a poor evaluated continuation: `finder` locates a same-color adjacent exchange, leaving the board unchanged and passing the unfavorable position to the opponent. Fallbacks, repeated-position handling, the time budget and the final round modify this rule.
5. When ahead and very few scoring actions remain, `killer_search` looks for a move that ends the game.

The archived entry uses a six-by-six active board and the course protocol spelling `Plaser`. It is a team project; the report credits Wenzhe Sheng, Yi Kang and Lixiao Liang for program design/implementation, and Feng Xiao and Yuchang Chen for report writing, with all five participating in testing.

## Version distinction

The report records a tuned net-score threshold of **-4**. The recovered competition entry uses **6** for its ordinary three-ply pass decision and includes a pass-bypass rule in sparse positions. These are distinct preserved artifacts. Their parameters have not been changed to manufacture agreement; see [SOURCE_NOTES.md](SOURCE_NOTES.md).

## Contents

| Path | Purpose |
| --- | --- |
| `code/group13_agent.py` | Primary archived Team 13 competition agent: one-/two-ply scoring helpers, three-ply search and tactical rules |
| `code/greedy_agent.py` | Course-provided greedy baseline |
| `code/board.py`, `interaction.py`, `exception_manager.py`, `eraserconfig.py` | Course simulator and runner support |
| `code/local_debugger.py` | Runs the recovered Team 13 agent against the greedy baseline in both orders |
| `data/replay1.json` | Sample replay; generation and validation status are documented in `VALIDATION.md` |
| `visualization/main.html` | Standalone replay viewer |
| `paper/pkudsa-group13.docx`, `.pdf` | The actual Team 13 project report |

## Running

Use Python 3.11 and install `requirements.txt`. From `code/`, run `python local_debugger.py`. This runs two complete games and writes `replay1.json` and `replay2.json` in that directory. The baseline opponent and starting order are explicit imports in the runner.

Open `visualization/main.html` in a browser and load a replay JSON using its file control. `7.html` and `gameinfo7.html` are historical server templates requiring the original course platform. ECharts retains its embedded license notice.

Run strategy checks from the repository root with `python -m unittest discover -s tests -v`. See [VALIDATION.md](VALIDATION.md) for the actual execution results and their limits.

## Attribution and archive scope

The simulator and baseline originate from the course framework; the report documents the team's strategy contributions. The unrelated Monte Carlo agent and the story previously mislabeled as a project report have been removed from the current archive. This repository does not claim every local experimental file as the final submitted implementation. Original source folders remain untouched.
