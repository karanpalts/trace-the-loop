"""Run the agent on one request and watch each turn.

  uv run ask.py "Enroll me in CS3300."
  uv run ask.py "..." --max-steps 2      # stop after two turns
  uv run ask.py "..." --no-enforce       # take the rules out of enroll
  uv run ask.py "..." --tool-mode NONE   # no tool runs, whatever comes back
"""
import argparse

from dotenv import load_dotenv
load_dotenv()

from src.agent.loop import run
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.agent.trace import Trace, show_turn
from src.tools import SCHEMAS
from src.tools.session import Session


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--max-steps", type=int, default=12)
    parser.add_argument("--no-enforce", action="store_true")
    parser.add_argument("--tool-mode", choices=["AUTO", "ANY", "NONE"])
    args = parser.parse_args()

    session = Session("STU001", enforce=not args.no_enforce)
    answer = run(Model(SYSTEM, SCHEMAS), args.request, session, Trace(show_turn), args.max_steps,
                 tool_mode=args.tool_mode)

    print(f"\nanswer: {answer}")
    print(f"enrolled now: {session.student['current_enrollment']}")
