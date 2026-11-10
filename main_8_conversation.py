"""Main 8: keep the conversation. The loop ends, and the chat goes on."""
from dotenv import load_dotenv
load_dotenv()

from src.agent.loop import run
from src.agent.model import Model
from src.agent.prompt import CHAT_SYSTEM
from src.agent.trace import Trace, show_turn
from src.tools import SCHEMAS
from src.tools.session import Session


def main():
    session = Session("STU001")
    model = Model(CHAT_SYSTEM, SCHEMAS)
    trace = Trace(on_turn=show_turn)
    contents = []

    while True:
        request = input("\nyou (blank to quit): ").strip()
        if not request:
            break
        answer = run(model, request, session, trace, contents=contents)
        print("\nagent:", answer)

    print("enrolled now:", session.student["current_enrollment"])


main()
