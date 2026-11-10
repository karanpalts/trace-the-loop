"""Main 5: repeat until a turn names no tool. This is the agent."""
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.messages import model_turn, results_message, text_in, tool_calls_in, user_message
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.tools import SCHEMAS, TOOLS
from src.tools.session import Session

REQUEST = sys.argv[1] if len(sys.argv) > 1 else (
    "Register me for two 3000-level CS courses that fit my schedule "
    "and that I have the prerequisites for.")


def main():
    session = Session("STU001")
    model = Model(SYSTEM, SCHEMAS)
    contents = [user_message(REQUEST)]

    for step in range(1, 13):
        # SAMPLE: send everything so far; one inference.
        response = model.generate(contents)
        turn = model_turn(response)
        contents.append(turn)

        # PARSE: did this turn name any tools?
        calls = tool_calls_in(turn)

        # STOP: a turn that names no tool is the answer.
        if not calls:
            print("answer:", text_in(turn))
            print("enrolled now:", session.student["current_enrollment"])
            return

        # INVOKE: run each one, here, in this process.
        results = []
        for call in calls:
            result = TOOLS[call["name"]](session, **call["args"])
            print(step, call["name"], call["args"], "->", str(result)[:120])
            results.append(result)

        # APPEND: the next turn reads these.
        contents.append(results_message(calls, results))

    # LIMIT: your code ends the run, whatever was sampled.
    print("stopped: step limit")


main()
