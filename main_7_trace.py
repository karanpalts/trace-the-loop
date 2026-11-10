"""Main 7: record every turn. The loop moves to src/agent/loop.py, and gains a trace."""
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.loop import run
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.agent.trace import Trace, show_turn
from src.tools import SCHEMAS
from src.tools.session import Session

REQUEST = sys.argv[1] if len(sys.argv) > 1 else (
    "Register me for two 3000-level CS courses that fit my schedule "
    "and that I have the prerequisites for.")


def main():
    session = Session("STU001")
    model = Model(SYSTEM, SCHEMAS)
    trace = Trace(on_turn=show_turn)

    answer = run(model, REQUEST, session, trace)

    print("\nanswer:", answer)
    print("enrolled now:", session.student["current_enrollment"])
    print("input tokens across the run:", sum(t["prompt_tokens"] for t in trace.turns))


main()
