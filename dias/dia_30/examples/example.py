def add_task(tasks, title):
    tasks.append({"title": title, "done": False})


def test_add_task():
    tasks = []
    add_task(tasks, "Study Python")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Study Python"
    assert tasks[0]["done"] is False


test_add_task()
print("tests passed")
