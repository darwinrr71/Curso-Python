tasks = [
    {"title": "Read", "done": False},
    {"title": "Practice", "done": True},
]

for index, task in enumerate(tasks, start=1):
    mark = "x" if task["done"] else " "
    print(f"{index}. [{mark}] {task['title']}")
