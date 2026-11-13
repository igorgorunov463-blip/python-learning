import json # Импортируем модуль для работы с JSON-файлами

print("--- Мой трекер расходов ---")

# 1. Словари (Dictionaries). Это как список, но с ключами.
# Здесь мы храним расходы: "название": сумма
expenses = {
    "Аренда": 0,
    "Еда": 0,
    "Транспорт": 0
}

# 2. Запрашиваем данные у пользователя
print("Введи свои расходы за месяц (или 0, если не тратил):")
expenses["Аренда"] = int(input("Сколько ушло на аренду? "))
expenses["Еда"] = int(input("Сколько ушло на еду? "))
expenses["Транспорт"] = int(input("Сколько ушло на транспорт? "))

# 3. Считаем общую сумму
total_expenses = sum(expenses.values())
print(f"\nТвои общие расходы: {total_expenses} руб.")

# 4. Работа с файлами. Сохраняем данные, чтобы они не пропали.
# Мы используем JSON — это текстовый формат, который понимает Python.
filename = "my_budget.json"

# Открываем файл для записи ('w' - write)
with open(filename, "w", encoding="utf-8") as file:
    json.dump(expenses, file, ensure_ascii=False, indent=4)
    
print(f"Данные успешно сохранены в файл {filename}!")

# 5. Читаем из файла (проверяем, что сохранилось)
print("\n--- Проверка данных из файла ---")
with open(filename, "r", encoding="utf-8") as file:
    saved_data = json.load(file)
    for category, amount in saved_data.items():
        print(f"Категория: {category} | Сумма: {amount}")