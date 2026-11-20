import json

data = {"name": "Ana", "age": 30}
print(json.dumps(data, ensure_ascii=False, indent=2))
