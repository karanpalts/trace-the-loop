"""Main 4: send the results back, and get an answer."""
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.messages import model_turn, results_message, text_in, tool_calls_in, user_message
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.tools import SCHEMAS, TOOLS
from src.tools.session import Session

REQUEST = sys.argv[1] if len(sys.argv) > 1 else "How many seats are left in CS2100 and CS2200?"


def main():
    session = Session("STU001")
    model = Model(SYSTEM, SCHEMAS)
    contents = [user_message(REQUEST)]

    response = model.generate(contents)
    turn = model_turn(response)
    contents.append(turn)

    calls = tool_calls_in(turn)
    results = []
    for call in calls:
        result = TOOLS[call["name"]](session, **call["args"])
        print(call["name"], call["args"], "->", str(result)[:200])
        results.append(result)
    contents.append(results_message(calls, results))

    response = model.generate(contents)
    turn = model_turn(response)

    print("answer:", text_in(turn))
    print("wants to call next:", [c["name"] for c in tool_calls_in(turn)])
    print("enrolled now:", session.student["current_enrollment"])


main()
