main.py

from services import add_task, list_tasks
from storage import load_tasks, save_tasks


def main():
    tasks = load_tasks("tasks.json")

    while True:
        print("\n1. Add task")
        print("2. List tasks")
        print("3. Save and exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            title = input("Task title: ").strip()
            add_task(tasks, title)
        elif option == "2":
            list_tasks(tasks)
        elif option == "3":
            save_tasks(tasks, "tasks.json")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
