"""search_courses. Read-only: the catalog, filtered."""
from src.tools.catalog import COURSES
from src.tools.registry import tool

FIELDS = ("id", "name", "level", "credits", "prereqs", "schedule")


@tool("Search the course catalog by department, optionally filtered by level "
      "(for example 3000 for 3000-level courses).")
def search_courses(session, department: str, level: int | None = None) -> list:
    matches = []
    for course in COURSES.values():
        if course["department"].upper() != department.upper():
            continue
        if level is not None and course["level"] != level:
            continue
        matches.append({field: course[field] for field in FIELDS})
    return matches
