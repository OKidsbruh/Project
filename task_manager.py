import json
import random

TASKS_FILE = "tasks.json"
tasks = []
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%_"
password = ""

for i in range(10):
    password += random.choice(characters)

print("Згенерований пароль:", password)

def check_password_strength(password):
    has_digit = False
    has_upper = False
    for char in password:
        if char.isdigit():
            has_digit = True
        if char.isupper():
            has_upper = True
    if len(password) >= 8 and has_digit and has_upper:
        return "надійний"
    elif len(password) >= 6:
        return "середній"
    else:
        return "слабкий"

def set_master_password():
    master_password = input("Введіть майстер-пароль: ")
    if len(master_password) < 8:
        print("Майстер-пароль має бути не менше 8 символів")
        return None
    return master_password

def login_gate(master_password):
    if not master_password:
        print("Майстер-пароль не встановлено. Вхід неможливий.")
        return False
    print("\nВхід до Менеджера завдань.")
    while True:
        entered = input("Введи пароль: ")
        if entered == master_password:
            print("Пароль правильний. Ласкаво просимо!")
            return True
        print("Невірний пароль, спробуй ще раз.")

def show_menu():
    print("\nМеню:")
    print("1) Додати завдання")
    print("2) Переглянути завдання")
    print("3) Видалити завдання")
    print("4) Позначити завдання виконаним")
    print("5) Вихід")
    return input("Ваш вибір: ")

def load_tasks(filename=TASKS_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks, filename=TASKS_FILE):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)

def add_task():
    text = input("Введіть текст завдання: ")
    tasks.append({"text": text, "completed": False})
    save_tasks(tasks)
    print(f"Завдання '{text}' додано.")

def mark_task_done():
    if len(tasks) == 0:
        print("Список завдань порожній.")
        return

    view_tasks()
    number = input("Введи номер виконаного завдання: ")

    if not number.isdigit():
        print("Потрібно ввести число.")
        return

    number = int(number)

    if number < 1 or number > len(tasks):
        print("Немає завдання з таким номером.")
        return

    tasks[number - 1]["completed"] = True
    save_tasks(tasks)
    print("Завдання позначено виконаним:", tasks[number - 1]["text"])

def view_tasks():
    if not tasks:
        print("Немає завдань.")
        return
    for i, task in enumerate(tasks, 1):
        status = "Виконано" if task["completed"] else "В процесі"
        print(f"{i}. {task['text']} [{status}]")

def delete_task():
    if not tasks:
        print("Немає завдань.")
        return
    view_tasks()
    number = input("Введіть номер завдання для видалення: ")
    if not number.isdigit():
        print("Потрібно ввести число.")
        return
    index = int(number) - 1
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print("Завдання видалено:", removed["text"])
    else:
        print("Немає завдання з таким номером.")

def main():
    global tasks
    tasks = load_tasks()
    master_password = set_master_password()
    if not login_gate(master_password):
        return
    while True:
        choice = show_menu()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            mark_task_done()
        elif choice == "5":
            print("Ви вийшли з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
