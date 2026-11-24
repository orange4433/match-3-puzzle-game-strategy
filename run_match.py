"""Simulate one local match and open its offline replay viewer."""
from pathlib import Path
import argparse
import contextlib
import json
import random
import sys
import webbrowser

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))


def replay_html(record):
    """Reuse the bundled viewer without a server or a file-selection step."""
    html = (ROOT / "visualization" / "main.html").read_text(encoding="utf-8")
    for asset in ["./lib/echarts.min.js", "Styles/style.css",
                  "Scripts/main.js", "Scripts/demo.js", "Scripts/Ribbon.js"]:
        html = html.replace(f'"{asset}"', f'"../visualization/{asset.removeprefix("./")}"')
    payload = json.dumps(record, ensure_ascii=False).replace("<", "\\u003c")
    boot = '''
    <script type="application/json" id="match-record">PAYLOAD</script>
    <script>
      const matchRecord = JSON.parse(document.getElementById('match-record').textContent);
      initialization(matchRecord);
      updateChooser(fileChooser);
    </script>
'''.replace("PAYLOAD", payload)
    return html.replace("</body>", boot + "</body>")


def run_match(seed, open_browser=True):
    import group13_agent
    import greedy_agent
    from interaction import Game_play

    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)
    print(f"Running Team 13 vs Greedy baseline (seed={seed})...")
    random.seed(seed)
    with (output / "match.log").open("w", encoding="utf-8") as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            game = Game_play(group13_agent, greedy_agent, order=0, seed=seed)
            record = game.start_game()
    record["teamNames"] = ["第13组策略", "贪心基线"]
    record["seed"] = seed
    replay = output / "replay.json"
    game.save_log(str(replay))
    record = json.loads(replay.read_text(encoding="utf-8"))
    if record["errorStatus"] != -1:
        raise RuntimeError(f"Match failed; see {output / 'match.log'} and {replay}")
    if not record["frames"] or len(record["frames"]) != record["totalFrames"]:
        raise ValueError("The game runner produced an incomplete replay.")
    viewer = output / "match.html"
    viewer.write_text(replay_html(record), encoding="utf-8")
    print(f"Completed {game.turn} turns. Scores: Team 13 {game.score[0]}, Greedy {game.score[1]}.")
    print(f"Replay viewer: {viewer}")
    print(f"Replay data:   {replay}")
    if open_browser and not webbrowser.open(viewer.as_uri()):
        print("Open outputs/match.html in your browser to watch the match.")
    return viewer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42, help="Board/random seed (default: 42).")
    parser.add_argument("--no-browser", action="store_true", help="Generate the replay without opening a browser.")
    args = parser.parse_args()
    try:
        run_match(args.seed, open_browser=not args.no_browser)
    except ImportError as error:
        parser.exit(1, f"Missing dependency: {error}. Run: python -m pip install -r requirements.txt\n")
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
