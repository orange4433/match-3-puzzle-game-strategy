# Match-Three Search Agents

Algorithms and data-structures coursework implementing a competitive match-three game with an **alpha-beta agent**, a **Monte Carlo tree-search agent**, a board simulator and replay visualization.

## Full report

[Project report (PDF)](paper/report.pdf) · [DOCX](paper/report.docx) · [Markdown with illustrations](paper/report.md)

## Contents

| Path | Purpose |
| --- | --- |
| `code/player1.py` | Alpha-beta search and tactical heuristics |
| `code/player2.py` | Monte Carlo tree search with rollout policies |
| `code/board.py` | Board generation, legal moves, eliminations and refill logic |
| `code/interaction.py` | Turn-taking, scoring, safety wrapper and replay logging |
| `code/greedy_agent.py` | Greedy baseline |
| `code/local_debugger.py` | Runs the two submitted agents in both orders |
| `data/replay1.json` | An archived match replay |
| `visualization/main.html` | Standalone replay viewer |

## Running

Use Python 3.11 and install `requirements.txt`. From `code/`, run:

```text
python local_debugger.py
```

This runs complete games and writes replay JSON. Original rules allow up to 100 turns per player and enforce a total time budget. The protocol class spelling `Plaser` is preserved because the runner expects it.

Open `visualization/main.html` in a browser and select the archived replay or a newly generated JSON file using its local file control. The viewer includes its ECharts dependency. `7.html` and `gameinfo7.html` are historical server templates; their Django-style asset placeholders require the original course platform.

## Validation and scope

Preparation checks cover board generation, an alpha-beta successor evaluation, one MCTS move and a short match using the greedy agents. A full tournament was not rerun. See `VALIDATION.md` for the actual result.

Only the core submitted agents, simulator, report, sample replay and viewer are retained. Experimental variants and unrelated course files are excluded. Comments and this README are in English; original game UI text and the full report are preserved. Third-party ECharts retains its embedded license notice.
