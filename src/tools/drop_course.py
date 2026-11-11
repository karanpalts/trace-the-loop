from src.tools.registry import tool

@tool("Drop a course the student is currently enrolled in. Refuses if the student is not enrolled in the course.")
def drop_course(session, course_id: str) -> dict:
    current = session.student["current_enrollment"]
    
    if course_id not in current:
         return {"ok": False, "reason": f"not_enrolled_in: {course_id}"}
    
    current.remove(course_id)
    return {"ok": True, "status": "dropped"}