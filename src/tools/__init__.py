"""Importing a tool's file registers it. To add a tool: add a file, add it here."""
from src.tools import (search_courses, get_course_details, get_my_record,
                       check_prereqs, check_schedule_conflict,
                       get_seats_remaining, enroll)
from src.tools.registry import SCHEMAS, TOOLS
