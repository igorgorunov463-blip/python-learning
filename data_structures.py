# --- СПИСКИ (Lists) ---
print("--- 1. Списки ---")
# Список - это упорядоченный набор элементов в квадратных скобках []
skills = ["Python", "Git", "Linux"]

print("Мои навыки:", skills)
print("Первый навык:", skills[0]) # Нумерация начинается с 0!

# Добавляем новый навык в конец списка
skills.append("AI Engineering")
print("Обновленный список:", skills)

# --- СЛОВАРИ (Dictionaries) ---
print("\n--- 2. Словари ---")
# Словарь хранит данные в формате "Ключ: Значение" в фигурных скобках {}
user_profile = {
    "name": "Сергей",
    "city": "Саратов",
    "goal": "IT",
    "budget": 190000
}

print("Имя пользователя:", user_profile["name"])
print("Цель:", user_profile["goal"])

# Меняем значение по ключу
user_profile["city"] = "Санкт-Петербург"
print("Новый город:", user_profile["city"])

# --- СПИСОК СЛОВАРЕЙ (Как хранят данные в реальных базах) ---
print("\n--- 3. Список словарей ---")
projects = [
    {"title": "Парсер цен", "status": "done"},
    {"title": "Telegram-бот", "status": "in progress"},
    {"title": "RAG-система", "status": "planned"}
]

# Перебираем список проектов циклом for
for project in projects:
    print(f"Проект: {project['title']} | Статус: {project['status']}")