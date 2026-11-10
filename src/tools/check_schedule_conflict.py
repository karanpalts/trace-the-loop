"""check_schedule_conflict. Read-only: do these courses fit together?"""
from src.tools.catalog import COURSES, overlap
from src.tools.registry import tool


@tool("Check whether a list of proposed course ids conflict in time with the "
      "student's current enrollment or with each other.")
def check_schedule_conflict(session, course_ids: list[str]) -> dict:
    unknown = [c for c in course_ids if c not in COURSES]
    if unknown:
        return {"error": f"Course not found: {', '.join(unknown)}"}
    courses = session.student["current_enrollment"] + course_ids
    conflicts = []
    for i, first in enumerate(courses):
        for second in courses[i + 1:]:
            if overlap(COURSES[first]["schedule"], COURSES[second]["schedule"]):
                conflicts.append([first, second])
    return {"ok": not conflicts, "conflicts": conflicts}
