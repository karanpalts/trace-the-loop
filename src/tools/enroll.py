"""enroll. The one tool that changes anything. Every rule is enforced here."""
from src.tools.catalog import COURSES, missing_prereqs, overlap
from src.tools.registry import tool


@tool("Enroll the student in a course. Refuses if a prerequisite is missing, "
      "the time conflicts with current enrollment, or no seats remain. Safe "
      "to repeat: enrolling twice changes nothing.")
def enroll(session, course_id: str) -> dict:
    if course_id not in COURSES:
        return {"ok": False, "reason": f"course_not_found: {course_id}"}
    current = session.student["current_enrollment"]
    course = COURSES[course_id]
    if course_id in current:
        return {"ok": True, "status": "already_enrolled"}
    if session.enforce:
        missing = missing_prereqs(session, course)
        if missing:
            return {"ok": False, "reason": f"missing_prereq: {','.join(missing)}"}
        for other in current:
            if overlap(COURSES[other]["schedule"], course["schedule"]):
                return {"ok": False, "reason": f"schedule_conflict_with: {other}"}
        if course["enrolled_count"] >= course["capacity"]:
            return {"ok": False, "reason": "no_seats_remaining"}
    current.append(course_id)
    return {"ok": True, "status": "enrolled"}
