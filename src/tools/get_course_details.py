"""get_course_details. Read-only: one course."""
from src.tools.catalog import COURSES
from src.tools.registry import tool


@tool("Get full details for one course by its id (for example 'CS3500').")
def get_course_details(session, course_id: str) -> dict:
    return COURSES.get(course_id) or {"error": f"Course not found: {course_id}"}
