"""check_prereqs. Read-only: does the student have the prerequisites?"""
from src.tools.catalog import COURSES, missing_prereqs
from src.tools.registry import tool


@tool("Check whether the student has completed all prerequisites for a "
      "course. Returns ok=true, or lists the missing course ids.")
def check_prereqs(session, course_id: str) -> dict:
    if course_id not in COURSES:
        return {"error": f"Course not found: {course_id}"}
    missing = missing_prereqs(session, COURSES[course_id])
    return {"ok": not missing, "missing": missing}
