"""get_seats_remaining. Read-only: how many seats are left?"""
from src.tools.catalog import COURSES
from src.tools.registry import tool


@tool("Get the number of seats remaining in a course.")
def get_seats_remaining(session, course_id: str) -> dict:
    if course_id not in COURSES:
        return {"error": f"Course not found: {course_id}"}
    c = COURSES[course_id]
    return {"course_id": course_id, "remaining": c["capacity"] - c["enrolled_count"]}
