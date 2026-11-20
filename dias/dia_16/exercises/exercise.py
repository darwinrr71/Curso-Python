from pathlib import Path

path = Path("students.txt")
path.write_text("Ana\nLuis\nEva\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as file:
    print([line.strip() for line in file if line.strip()])
