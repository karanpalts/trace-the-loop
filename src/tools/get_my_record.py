"""get_my_record. Read-only: the signed-in student's record."""
from src.tools.registry import tool


@tool("Get the courses the student has completed and is currently enrolled "
      "in.")
def get_my_record(session) -> dict:
    s = session.student
    return {"completed": s["completed_courses"], "current_enrollment": s["current_enrollment"]}
