"""Forget everything saved between runs. Only Main 9 saves anything: its notes in data/memory/."""
from src.agent.memory import FOLDER

for path in sorted(FOLDER.glob("*.json")):
    path.unlink()
    print("forgot", path.name)
print("memory is empty")
