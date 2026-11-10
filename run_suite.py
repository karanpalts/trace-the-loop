"""Run the trajectory suite.

  uv run run_suite.py --replay            # the committed recording: no key, no model
  uv run run_suite.py --runs 5            # live; every task five times
  uv run run_suite.py --runs 5 --record   # live, and save it as data/fixtures/
  uv run run_suite.py --runs 5 --no-enforce   # the rule lives only in the instructions
"""
import argparse, json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from src.agent.model import Recording, Replay
from src.agent.prompt import SYSTEM
from src.tools import SCHEMAS
from src.harness.suite import load_tasks, report, run_task

parser = argparse.ArgumentParser()
parser.add_argument("--runs", type=int, default=5)
parser.add_argument("--replay", action="store_true")
parser.add_argument("--record", action="store_true")
parser.add_argument("--no-enforce", action="store_true")
parser.add_argument("--slice")
parser.add_argument("--out")
args = parser.parse_args()

FIX = Path("data/fixtures")
tasks = [t for t in load_tasks() if not args.slice or t["slice"] == args.slice]
rows = []
for t in tasks:
    if args.replay:
        for path in sorted(FIX.glob(f"{t['id']}-run-*.json")):
            rows.append(run_task(Replay(json.loads(path.read_text()), SYSTEM, SCHEMAS), t))
        continue
    for k in range(1, args.runs + 1):
        p = Recording(SYSTEM, SCHEMAS)
        rows.append(run_task(p, t, enforce=not args.no_enforce))
        print(f"{t['id']} run {k}: {'ok ' if rows[-1]['success'] else 'FAIL'} {rows[-1]['steps']} steps {rows[-1]['added']}", flush=True)
        if args.record:
            FIX.mkdir(parents=True, exist_ok=True)
            (FIX / f"{t['id']}-run-{k}.json").write_text(json.dumps(p.responses))
report(rows)
if args.out:
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(rows, indent=1))
