import json
from pathlib import Path

path = Path("topics.json")
topics = ["Python", "Testing"]
path.write_text(json.dumps(topics, ensure_ascii=False), encoding="utf-8")

with path.open("r", encoding="utf-8") as file:
    print(json.load(file))
