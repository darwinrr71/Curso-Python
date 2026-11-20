from pathlib import Path

path = Path("hello.txt")
path.write_text("Python\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as file:
    print(file.read().strip())
