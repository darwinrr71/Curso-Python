services.py

from models import Task

def add_task(tasks: list[Task], title: str) -> None:
    tasks.append(Task(title=title))


def list_tasks(tasks: list[Task]) -> None:
    for index, task in enumerate(tasks, start=1):
        status = "done" if task.done else "pending"
        print(f"{index}. {task.title} - {status}")


storage.py

import json
from models import Task

def save_tasks(tasks: list[Task], filename: str) -> None:
    data = [{"title": task.title, "done": task.done} for task in tasks]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
