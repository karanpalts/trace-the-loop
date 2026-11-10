"""The trajectory suite: run tasks to the end, and score the state they leave behind."""
import json, math
from pathlib import Path

from src.agent.loop import STOPPED, run
from src.agent.trace import Trace
from src.tools.session import SEED, Session

TASKS = Path(__file__).parents[2] / "data" / "suite" / "tasks.jsonl"
BEFORE = set(SEED["STU001"]["current_enrollment"])


def load_tasks():
    return [json.loads(l) for l in TASKS.read_text().splitlines() if l.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p, d = k / n, 1 + z * z / n
    mid, half = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, mid - half), min(1.0, mid + half))


def run_task(model, task, enforce=True, max_steps=12):
    """One run of one task. Success is read from the enrollment table, not from the text."""
    session = Session("STU001", enforce=enforce)
    trace = Trace()
    answer = run(model, task["request"], session, trace, max_steps)
    turns = trace.turns
    added = sorted(set(session.student["current_enrollment"]) - BEFORE)
    calls = [c for t in turns for c in t["calls"]]
    return {"task": task["id"], "slice": task["slice"], "added": added,
            "success": added in [sorted(a) for a in task["accept"]],
            "status": "step_limit" if answer == STOPPED else "answered",
            "steps": len(turns), "tool_calls": len(calls),
            "tool_errors": sum(1 for c in calls if isinstance(c["result"], dict) and "error" in c["result"]),
            "prompt_tokens": sum(t["prompt_tokens"] for t in turns),
            "output_tokens": sum(t["output_tokens"] for t in turns),
            "per_step_prompt": [t["prompt_tokens"] for t in turns],
            "tools": [c["name"] for c in calls], "text": answer}


def report(rows):
    def line(name, rs):
        k, n = sum(r["success"] for r in rs), len(rs)
        lo, hi = wilson(k, n)
        steps = sorted(r["steps"] for r in rs)
        toks = sum(r["prompt_tokens"] + r["output_tokens"] for r in rs) / n
        print(f"  {name:12s} {k:3d}/{n:<3d} {100*k/n:5.0f}%  ({100*lo:3.0f}-{100*hi:3.0f}%)   "
              f"median steps {steps[n//2]:2d}, max {steps[-1]:2d}   mean tokens {toks:7.0f}")
    print("\n  slice        success        95% interval")
    for s in dict.fromkeys(r["slice"] for r in rows):
        line(s, [r for r in rows if r["slice"] == s])
    line("all", rows)
    errs, calls = sum(r["tool_errors"] for r in rows), sum(r["tool_calls"] for r in rows)
    print(f"\n  tool calls {calls}, returned an error {errs}; runs that hit the step limit "
          f"{sum(r['status'] == 'step_limit' for r in rows)}")
    failed = [r for r in rows if not r["success"]]
    for r in failed[:12]:
        print(f"  failed {r['task']}: added {r['added']}, {r['steps']} steps, {r['tools']}")
