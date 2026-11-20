import json
with open("user.json", "r", encoding = "utf - 8") as file:
data = json.load(file)
print(data)
import json
data = {"name": "Ana", "age": 30}
with open("user.json", "w", encoding = "utf - 8") as file:
json.dump(data, file, ensure_ascii = False, indent = 2)
