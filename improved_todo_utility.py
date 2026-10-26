"""
Improved To-Do List Utility
Week 4: Proposing Code Improvements and Feature Enhancements

A beginner-friendly command-line task manager with:
- Add, list, complete, and delete tasks
- Persistent storage in a local JSON file
- Input validation and clear messages
- A small, modular structure for easier maintenance

Run:
    python improved_todo_utility.py
"""

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[dict[str, Any]]:
    """Load tasks from JSON. Start with an empty list if no file exists."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            print("Warning: task file format was unexpected. Starting with an empty list.")
            return []
        return data
    except (json.JSONDecodeError, OSError) as error:
        print(f"Warning: could not read saved tasks ({error}). Starting with an empty list.")
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> bool:
    """Save tasks to JSON and report whether saving succeeded."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)
        return True
    except OSError as error:
        print(f"Error: tasks could not be saved ({error}).")
        return False


def show_tasks(tasks: list[dict[str, Any]]) -> None:
    """Display all tasks, including their status."""
    if not tasks:
        print("\nYour task list is empty.")
        return

    print("\n--- Your Tasks ---")
    for index, task in enumerate(tasks, start=1):
        status = "Done" if task.get("completed", False) else "Pending"
        print(f"{index}. [{status}] {task.get('title', '(untitled)')}")


def add_task(tasks: list[dict[str, Any]]) -> None:
    """Ask for a task title and add it when it is not blank."""
    title = input("Enter task description: ").strip()
    if not title:
        print("Task was not added: description cannot be blank.")
        return
    tasks.append({"title": title, "completed": False})
    if save_tasks(tasks):
        print("Task added and saved.")


def get_task_index(tasks: list[dict[str, Any]], prompt: str) -> int | None:
    """Get a valid zero-based task index, or None if the input is invalid."""
    if not tasks:
        print("There are no tasks to update.")
        return None
    raw_value = input(prompt).strip()
    try:
        index = int(raw_value) - 1
    except ValueError:
        print("Please enter a whole number from the task list.")
        return None
    if index < 0 or index >= len(tasks):
        print(f"Please enter a number between 1 and {len(tasks)}.")
        return None
    return index


def complete_task(tasks: list[dict[str, Any]]) -> None:
    """Mark a selected task as completed."""
    show_tasks(tasks)
    index = get_task_index(tasks, "Task number to mark complete: ")
    if index is None:
        return
    tasks[index]["completed"] = True
    if save_tasks(tasks):
        print("Task marked as complete.")


def delete_task(tasks: list[dict[str, Any]]) -> None:
    """Delete a selected task after confirmation."""
    show_tasks(tasks)
    index = get_task_index(tasks, "Task number to delete: ")
    if index is None:
        return
    title = tasks[index].get("title", "(untitled)")
    confirm = input(f'Delete "{title}"? Type y to confirm: ').strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return
    removed = tasks.pop(index)
    if save_tasks(tasks):
        print(f'Task deleted: {removed.get("title", "(untitled)")}')


def print_menu() -> None:
    """Print the available commands."""
    print(
        "\n=== To-Do List ===\n"
        "1. View tasks\n"
        "2. Add task\n"
        "3. Mark task complete\n"
        "4. Delete task\n"
        "5. Exit"
    )


def main() -> None:
    """Run the interactive application loop."""
    tasks = load_tasks()
    print("Welcome to the To-Do List Utility.")
    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye. Your saved tasks will be available next time.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
