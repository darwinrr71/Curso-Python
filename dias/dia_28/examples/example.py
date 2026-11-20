from dataclasses import dataclass


@dataclass
class Task:
    title: str
    done: bool = False


print(Task("Study Python"))
