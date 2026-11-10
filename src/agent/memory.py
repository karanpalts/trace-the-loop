"""Prompt memory: notes kept in a file, put into the instructions when a conversation starts."""
import json
from pathlib import Path

FOLDER = Path(__file__).parents[2] / "data" / "memory"
MAX_NOTES = 20   # memory is part of every request, so it is bounded


def path_for(student_id):
    return FOLDER / f"{student_id}.json"


def load_notes(student_id):
    path = path_for(student_id)
    return json.loads(path.read_text()) if path.exists() else []


def save_note(student_id, note):
    notes = (load_notes(student_id) + [note])[-MAX_NOTES:]
    FOLDER.mkdir(parents=True, exist_ok=True)
    path_for(student_id).write_text(json.dumps(notes, indent=2))
    return notes


def with_notes(system, notes):
    if not notes:
        return system
    remembered = "\n".join(f"- {note}" for note in notes)
    return f"{system}\n\nNotes from earlier conversations:\n{remembered}"
