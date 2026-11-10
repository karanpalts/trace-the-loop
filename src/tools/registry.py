"""The registry: a Python function becomes a declaration the model is told about."""
import inspect
from typing import get_args, get_origin, get_type_hints

TOOLS = {}      # name -> function: what your program runs
SCHEMAS = []    # the declarations: what the model is told

JSON_TYPES = {int: "integer", float: "number", bool: "boolean", str: "string"}


def tool(description):
    def register(fn):
        SCHEMAS.append(build_schema(fn, description))
        TOOLS[fn.__name__] = fn
        return fn
    return register


def build_schema(fn, description):
    hints = get_type_hints(fn)
    properties, required = {}, []
    for name, param in inspect.signature(fn).parameters.items():
        # The session is supplied by the program, never by the model.
        if name == "session":
            continue
        properties[name] = json_type(hints.get(name, str))
        if param.default is inspect.Parameter.empty:
            required.append(name)
    parameters = {"type": "object", "properties": properties, "required": required}
    return {"name": fn.__name__, "description": description, "parameters": parameters}


def json_type(t):
    if get_origin(t) is list:
        return {"type": "array", "items": json_type(get_args(t)[0])}
    inner = [a for a in get_args(t) if a is not type(None)]
    return json_type(inner[0]) if inner else {"type": JSON_TYPES.get(t, "string")}
