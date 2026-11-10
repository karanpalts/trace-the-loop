"""Main 6: check every call before it runs. A bad call becomes a result."""
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.messages import model_turn, results_message, text_in, tool_calls_in, user_message
from src.agent.model import Model
from src.agent.prompt import SYSTEM
from src.tools import SCHEMAS
from src.tools.dispatch import dispatch
from src.tools.session import Session

REQUEST = sys.argv[1] if len(sys.argv) > 1 else (
    "Register me for two 3000-level CS courses that fit my schedule "
    "and that I have the prerequisites for.")

BAD_CALLS = [("drop_course", {"course_id": "CS3300"}),
             ("enroll", {}),
             ("enroll", {"course_id": "CS3300", "student_id": "STU999"}),
             ("enroll", {"course_id": 3300}),
             ("enroll", {"course_id": "CS4500"})]


def main():
    session = Session("STU001")

    for name, args in BAD_CALLS:
        print(name, args, "->", dispatch(name, args, session))

    model = Model(SYSTEM, SCHEMAS)
    contents = [user_message(REQUEST)]

    for step in range(1, 13):
        response = model.generate(contents)
        turn = model_turn(response)
        contents.append(turn)

        calls = tool_calls_in(turn)

        if not calls:
            print("answer:", text_in(turn))
            print("enrolled now:", session.student["current_enrollment"])
            return

        results = []
        for call in calls:
            result = dispatch(call["name"], call["args"], session)
            print(step, call["name"], call["args"], "->", str(result)[:120])
            results.append(result)

        contents.append(results_message(calls, results))

    print("stopped: step limit")


main()
