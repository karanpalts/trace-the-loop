"""Who is asking. Set by the program from the login. Never in the context."""
import copy, json
from dataclasses import dataclass, field
from pathlib import Path

DATA = Path(__file__).parents[2] / "data" / "catalog"
SEED = {s["id"]: s for s in json.loads((DATA / "students.seed.json").read_text())["students"]}


@dataclass
class Session:
    student_id: str
    enforce: bool = True    # the lab turns this off in one experiment
    students: dict = field(default_factory=lambda: copy.deepcopy(SEED))

    @property
    def student(self):
        return self.students[self.student_id]
