def add_task(tasks: list[str], title: str) -> list[str]:
    tasks.append(title)
    return tasks


items: list[str] = []
print(add_task(items, "Study imports"))
