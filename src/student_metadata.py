"""Student identity is stored separately from folder naming."""
import json
from pathlib import Path


def read_student(folder):
    folder = Path(folder)
    metadata = folder / "student.json"
    if metadata.exists():
        return json.loads(metadata.read_text(encoding="utf-8"))
    # Legacy names are ambiguous; preserve them instead of guessing ownership.
    return {"name": folder.name.replace("_", " "), "teacher": "Unknown", "created": "Unknown"}
