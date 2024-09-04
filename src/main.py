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
    tasks = db.write(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")


def list(args):
    tasks = db.get_all()
    categorized_tasks = {}

    for task in tasks:
        categorized_tasks.setdefault(task["status"], []).append(task)

    if len(args) < 1:
        for status, tasks in categorized_tasks.items():
            if not tasks:
                continue
            for task in tasks:
                print(f"[{task['status']}] {task['id']}: {task['description']}")
        sys.exit(0)

    status = args[0]

    if status not in categorized_tasks:
        print(f"Unknown status: {status}")
        print("Usage: task-cli list <status>")
        sys.exit(1)

    for task in categorized_tasks[status]:
        print(f"[{task['status']}] {task['id']}: {task['description']}")


def update(args):
    if len(args) < 2:
        print("Usage: task-cli update <id> <description>")
        sys.exit(1)

    task_id = int(args[0])
    task_description = args[1]
    tasks = db.get_all()

    is_task_found = False

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = task_description
            task["updatedAt"] = datetime.now().isoformat()
            is_task_found = True
            break

    if not is_task_found:
        print(f"Task not found (ID: {task_id})")
        sys.exit(1)

    tasks = db.write(tasks)
    print(f"Task updated successfully (ID: {task_id})")


def mark(args):
    if len(args) < 1:
        print("Usage: task-cli mark-<status> <id>")
        sys.exit(1)

    try:
        task_status = args[0].split("mark-")[1]
        if not task_status:
            raise IndexError
    except IndexError:
        print("Usage: task-cli mark-<status> <id>")
        sys.exit(1)

    task_id = int(args[1])
    tasks = db.get_all()
    is_task_found = False

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = task_status
            task["updatedAt"] = datetime.now().isoformat()
            is_task_found = True
            break

    if not is_task_found:
        print(f"Task not found (ID: {task_id})")
        sys.exit(1)

    tasks = db.write(tasks)
    print(f"Task marked as {task_status} successfully (ID: {task_id})")


def delete(args):
    if len(args) < 1:
        print("Usage: task-cli delete <id>")
        sys.exit(1)

    task_id = int(args[0])
    tasks = db.get_all()

    is_task_found = False

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            is_task_found = True
            break

    if not is_task_found:
        print(f"Task not found (ID: {task_id})")
        sys.exit(1)

    tasks = db.write(tasks)
    print(f"Task deleted successfully (ID: {task_id})")


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    match command:
        case "add":
            add(args)
        case "list":
            list(args)
        case "update":
            update(args)
        case "delete":
            delete(args)
        case cmd if cmd.startswith("mark"):
            mark([cmd, *args])
        case _:
            print(f"Unknown command: {command}")
            print("Usage: task-cli <command> [options]")
            sys.exit(1)


if __name__ == "__main__":
    main()
