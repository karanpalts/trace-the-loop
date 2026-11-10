"""Main 1: ask the model. It returns text, and nothing happens."""
import sys

from dotenv import load_dotenv
load_dotenv()

from src.agent.messages import model_turn, text_in, user_message
from src.agent.model import Model
from src.tools.session import Session

SYSTEM = "You are the course registration assistant for a university."
REQUEST = sys.argv[1] if len(sys.argv) > 1 else "Enroll me in CS3300."


def main():
    session = Session("STU001")
    model = Model(SYSTEM)
    contents = [user_message(REQUEST)]

    response = model.generate(contents)
    turn = model_turn(response)

    print(text_in(turn))
    print("enrolled now:", session.student["current_enrollment"])


main()
