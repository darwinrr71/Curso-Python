Manejar archivo inexistente

import json
from pathlib import Path
from models import Task


def load_tasks(filename: str) -> list[Task]:
    path = Path(filename)
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Task(**item) for item in data]
