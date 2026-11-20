import json

config = {"course": "Python en 30 días", "days": 30}
print(json.dumps(config, ensure_ascii=False, indent=2))
