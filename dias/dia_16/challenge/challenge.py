from pathlib import Path

path = Path("tasks.txt")
path.write_text("Study\nPractice\nReview\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as file:
    print([line.strip() for line in file if line.strip()])
