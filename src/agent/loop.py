"""The agent. One line involves the model. Everything else is your program."""
from src.agent.messages import (model_message, model_turn, results_message, text_in,
                                tool_calls_in, user_message)
from src.tools.dispatch import dispatch

STOPPED = "(stopped by the step limit)"
NO_ANSWER = "(no answer: the turn had no text)"


def run(model, request, session, trace, max_steps=12, contents=None, tool_mode=None):
    contents = [] if contents is None else contents
    contents.append(user_message(request))

    for step in range(1, max_steps + 1):
        # SAMPLE: send everything so far; one inference.
        response = model.generate(contents, tool_mode)
        turn = model_turn(response)

        # PARSE: did this turn name any tools?
        calls = tool_calls_in(turn)

        # TOOLS OFF: nothing runs, whatever was sampled.
        if tool_mode == "NONE":
            calls = []

        # STOP: a turn that runs no tool is the answer, if it has any text.
        if not calls:
            trace.record(step, response, [], [])
            answer = text_in(turn)
            if not answer:
                return NO_ANSWER
            contents.append(model_message(answer))
            return answer

        # INVOKE: validate each call and run it, here, in this process.
        results = [dispatch(c["name"], c["args"], session) for c in calls]

        # APPEND: the next turn reads these.
        contents.append(turn)
        contents.append(results_message(calls, results))
        trace.record(step, response, calls, results)

    # LIMIT: your code ends the run, whatever was sampled.
    return STOPPED
