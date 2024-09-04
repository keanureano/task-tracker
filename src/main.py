import sys
import database as db
from datetime import datetime


def add(args):
    if len(args) < 1:
        print("Usage: task-cli add <description>")
        sys.exit(1)

    tasks = db.get_all()

    new_task = {
        "id": 1 if not tasks else max(task["id"] for task in tasks) + 1,
        "description": args[0],
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    tasks.append(new_task)
    tasks = db.add(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    match command:
        case "add":
            add(args)


if __name__ == "__main__":
    main()
