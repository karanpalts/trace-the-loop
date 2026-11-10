"""The trace: one record per turn. The primary dataset of an agent."""
import json

from src.agent.messages import model_turn, text_in, tool_calls_in


def show_turn(turn):
    print(f"\nstep {turn['step']}   {turn['prompt_tokens']} tokens in, "
          f"{turn['output_tokens']} out, {turn['latency_ms']} ms")
    if turn["text"]:
        print(f"  text:   {turn['text']}")
    if turn["ignored"]:
        print(f"  named but not run: {turn['ignored']}")
    for c in turn["calls"]:
        print(f"  call:   {c['name']}({json.dumps(c['args'])})")
        print(f"  result: {json.dumps(c['result'])[:300]}")


class Trace:
    def __init__(self, on_turn=None):
        self.turns = []
        self.on_turn = on_turn

    def record(self, step, response, calls, results):
        usage = response.get("usageMetadata", {})
        turn = {
            "step": step,
            "model": response.get("modelVersion"),
            "prompt_tokens": usage.get("promptTokenCount", 0),
            "output_tokens": usage.get("candidatesTokenCount", 0),
            "latency_ms": response.get("latency_ms", 0),
            "calls": [{**call, "result": result} for call, result in zip(calls, results)],
            "text": text_in(model_turn(response)),
            "ignored": [c["name"] for c in tool_calls_in(model_turn(response))] if not calls else [],
        }
        self.turns.append(turn)
        if self.on_turn:
            self.on_turn(turn)
