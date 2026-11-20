Test simple

from services import add_task
def test_add_task():
tasks = []
add_task(tasks, "Study Python")

assert len(tasks) == 1 assert tasks[0].title == "Study Python" assert tasks[0].done is False
