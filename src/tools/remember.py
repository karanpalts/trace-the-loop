"""remember. Saves a note for later conversations. The note is model output: a hint, never a permission."""
from src.agent.memory import save_note
from src.tools.registry import tool


@tool("Save a short note about the student, such as a preference or a constraint "
      "they mention, so it can be used in later conversations.")
def remember(session, note: str) -> dict:
    notes = save_note(session.student_id, note)
    return {"ok": True, "notes_saved": len(notes)}
