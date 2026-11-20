from dataclasses import dataclass


@dataclass
class Task:
    title: str
    done: bool = False


def add_task(tasks, title):
    tasks.append(Task(title=title))


tasks = []
add_task(tasks, "Write services")
print(tasks)
