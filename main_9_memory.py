"""Main 9: remember across conversations. Main 8, plus prompt memory:
notes saved to a file, and put into the instructions when a conversation starts."""
from dotenv import load_dotenv
load_dotenv()

from src.agent.loop import run
from src.agent.memory import load_notes, with_notes
from src.agent.model import Model
from src.agent.prompt import CHAT_SYSTEM
from src.agent.trace import Trace, show_turn
from src.tools import SCHEMAS
from src.tools import remember      # the new tool: importing its file registers it
from src.tools.session import Session


def main():
    session = Session("STU001")

    # MEMORY: what earlier conversations saved goes into the instructions.
    notes = load_notes(session.student_id)
    print("remembered:", notes)
    model = Model(with_notes(CHAT_SYSTEM, notes), SCHEMAS)

    trace = Trace(on_turn=show_turn)
    contents = []

    while True:
        request = input("\nyou (blank to quit): ").strip()
        if not request:
            break
        answer = run(model, request, session, trace, contents=contents)
        print("\nagent:", answer)

    print("remembered now:", load_notes(session.student_id))


main()
