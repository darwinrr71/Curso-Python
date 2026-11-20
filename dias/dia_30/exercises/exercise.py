import json
from pathlib import Path


def load_tasks(filename):
    path = Path(filename)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


print(load_tasks("missing_tasks.json"))
