import sqlite3

# 1. Подключаемся к базе. Если файла нет, он создастся.
conn = sqlite3.connect("startup.db")
cursor = conn.cursor() # Курсор — это "рука", которой мы делаем запросы

# 2. Создаем таблицу для пользователей
# AUTOINCREMENT значит, что ID будет расти сам (1, 2, 3...)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user'
)
""")
conn.commit() # Обязательно сохраняем изменения!

# 3. Функция для добавления пользователя
def add_user(name, email, role="user"):
    try:
        cursor.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", (name, email, role))
        conn.commit()
        print(f"✅ Пользователь {name} добавлен!")
    except sqlite3.IntegrityError:
        print(f"❌ Ошибка: Пользователь с email {email} уже существует.")

# 4. Добавляем несколько пользователей
print("--- Добавление пользователей ---")
add_user("Сергей", "sergey@startup.com", "admin")
add_user("Иван", "ivan@startup.com")
add_user("Анна", "anna@startup.com")
add_user("Дубликат", "sergey@startup.com") # Вызовет ошибку, так как email занят

# 5. Читаем данные из базы
print("\n--- Список всех пользователей ---")
cursor.execute("SELECT id, name, email, role FROM users")
all_users = cursor.fetchall()

for user in all_users:
    print(f"ID: {user[0]} | Имя: {user[1]} | Email: {user[2]} | Роль: {user[3]}")

# 6. Закрываем соединение (хороший тон)
conn.close()