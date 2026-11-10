"""The boundary. A tool call is model output, so it is checked like any input."""
from src.tools.registry import SCHEMAS, TOOLS

PYTHON_TYPES = {"integer": int, "number": (int, float), "boolean": bool,
                "string": str, "array": list}


def dispatch(name, args, session):
    # Errors are returned as results: the next turn reads them.
    if name not in TOOLS:
        return {"error": f"Unknown tool: {name}. Available tools: {', '.join(TOOLS)}"}
    schema = next(s for s in SCHEMAS if s["name"] == name)
    problem = validate(args, schema)
    if problem:
        return {"error": f"Invalid call to {name}: {problem}"}
    try:
        return TOOLS[name](session, **args)
    except Exception as e:
        return {"error": f"{name} failed: {type(e).__name__}: {e}"}


def validate(args, schema):
    spec = schema["parameters"]
    missing = [a for a in spec["required"] if a not in args]
    unknown = [a for a in args if a not in spec["properties"]]
    if missing:
        return f"missing argument(s): {', '.join(missing)}"
    if unknown:
        return f"unknown argument(s): {', '.join(unknown)}"
    for name, value in args.items():
        expected = spec["properties"][name]["type"]
        if not isinstance(value, PYTHON_TYPES[expected]):
            return f"{name} must be {expected}, got {type(value).__name__}"
