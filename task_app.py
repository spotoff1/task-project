
import argparse
import json
import os

DATA_FILE = "tasks.json"
DEFAULT_PRIORITY = "normal"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title, priority=DEFAULT_PRIORITY):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "title": title, "status": "open", "priority": priority})
    save_tasks(tasks)
    print(f"Добавлена задача #{new_id}: {title}")


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    for t in tasks:
        print(f'#{t["id"]} [{t["status"]}] {t["title"]} ({t["priority"]})')


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            save_tasks(tasks)
            print(f"Задача #{task_id} выполнена")
            return
    print(f"Задача #{task_id} не найдена")


def main():
    parser = argparse.ArgumentParser(description="Учёт задач")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("--priority", default=DEFAULT_PRIORITY)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=["open", "done"])

    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.priority)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "done":
        complete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

VALID_PRIORITIES = {"low", "normal", "high"}


def validate_priority(priority):
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Недопустимый приоритет: {priority}")
    return priority
