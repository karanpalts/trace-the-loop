"""The catalog and the two facts the tools compute from it."""
import json
from pathlib import Path

DATA = Path(__file__).parents[2] / "data" / "catalog"
COURSES = {c["id"]: c for c in json.loads((DATA / "courses.json").read_text())}


def minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def overlap(a, b):
    return bool(set(a["days"]) & set(b["days"])) and (
        minutes(a["start_time"]) < minutes(b["end_time"])
        and minutes(b["start_time"]) < minutes(a["end_time"]))


def missing_prereqs(session, course):
    return [p for p in course["prereqs"] if p not in session.student["completed_courses"]]
