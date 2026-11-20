import json
from pathlib import Path

tasks = [{"title": "Read", "done": False}]
path = Path("tasks.json")
path.write_text(json.dumps(tasks), encoding="utf-8")

print(path.exists())
