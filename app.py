"""Простой трекер задач без внешних зависимостей."""

import argparse
import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks(path=TASKS_FILE):
    """Загрузить список задач или вернуть пустой список."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks, path=TASKS_FILE):
    """Сохранить задачи в удобном для чтения виде."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
        file.write("\n")


def add_task(title, path=TASKS_FILE):
    tasks = load_tasks(path)
    task = {"id": max((item["id"] for item in tasks), default=0) + 1,
            "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def complete_task(task_id, path=TASKS_FILE):
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks, path)
            return task
    return None


def print_tasks(tasks):
    if not tasks:
        print("Задач пока нет.")
        return
    for task in tasks:
        mark = "x" if task["done"] else " "
        print(f'{task["id"]}. [{mark}] {task["title"]}')


def build_parser():
    parser = argparse.ArgumentParser(description="Мини-трекер задач")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="показать задачи")

    add = commands.add_parser("add", help="добавить задачу")
    add.add_argument("title", help="текст задачи")

    done = commands.add_parser("done", help="завершить задачу")
    done.add_argument("task_id", type=int, help="номер задачи")
    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "list":
        print_tasks(load_tasks())
    elif args.command == "add":
        task = add_task(args.title)
        print(f'Добавлена задача #{task["id"]}: {task["title"]}')
    elif args.command == "done":
        task = complete_task(args.task_id)
        if task is None:
            print(f"Задача #{args.task_id} не найдена.")
        else:
            print(f'Задача #{args.task_id} завершена: {task["title"]}')


if __name__ == "__main__":
    main()
