"""Main 2: tell the model about the tools. It names one, and nothing runs."""
import json
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.messages import model_turn, tool_calls_in, user_message
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.tools import SCHEMAS

REQUEST = sys.argv[1] if len(sys.argv) > 1 else "How many seats are left in CS2100 and CS2200?"


def main():
    model = Model(SYSTEM, SCHEMAS)
    contents = [user_message(REQUEST)]

    response = model.generate(contents)
    turn = model_turn(response)

    calls = tool_calls_in(turn)
    print(json.dumps(calls, indent=2))
    print("Nothing has been run.")


main()
