"""The model: one HTTP POST. No SDK, so that this file is the wire format."""
import json, os, time, urllib.error, urllib.request

URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")


class Model:
    def __init__(self, system, tools=None):
        self.system = system
        self.tools = tools

    def request_for(self, contents, tool_mode=None):
        request = {"systemInstruction": {"parts": [{"text": self.system}]}}
        if self.tools:
            request["tools"] = [{"functionDeclarations": self.tools}]
        if tool_mode:
            request["toolConfig"] = {"functionCallingConfig": {"mode": tool_mode}}
        request["contents"] = contents
        return request

    def generate(self, contents, tool_mode=None):
        return self.post(self.request_for(contents, tool_mode))

    def post(self, request, attempts=6):
        body = json.dumps(request).encode()
        headers = {"Content-Type": "application/json",
                   "x-goog-api-key": os.environ["GEMINI_API_KEY"]}
        started = time.monotonic()
        for attempt in range(attempts):
            try:
                req = urllib.request.Request(URL.format(model=MODEL), body, headers)
                with urllib.request.urlopen(req, timeout=60) as r:
                    response = json.load(r)
                # Added by us; not part of the wire format.
                response["latency_ms"] = int((time.monotonic() - started) * 1000)
                return response
            except urllib.error.HTTPError as e:
                if e.code not in (429, 500, 503) or attempt == attempts - 1:
                    raise RuntimeError(f"{e.code}: {e.read().decode()[:400]}")
            time.sleep(min(2 ** attempt, 30))


class Recording(Model):
    """The live model, keeping every response so a run can be replayed."""

    def __init__(self, system, tools):
        super().__init__(system, tools)
        self.responses = []

    def post(self, request):
        response = super().post(request)
        self.responses.append(response)
        return response


class Replay(Model):
    """The same loop with recorded responses: no model, no key."""

    def __init__(self, responses, system, tools):
        super().__init__(system, tools)
        self.responses = iter(responses)

    def post(self, request):
        return dict(next(self.responses))
