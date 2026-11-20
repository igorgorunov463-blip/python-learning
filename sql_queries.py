import sqlite3

conn = sqlite3.connect("startup.db")
cursor = conn.cursor()

print("--- 1. Все пользователи ---")
cursor.execute("SELECT * FROM users") # * означает "все столбцы"
for row in cursor.fetchall():
    print(row)

print("\n--- 2. Только админы ---")
# WHERE означает "где". Мы ищем тех, у кого роль = 'admin'
cursor.execute("SELECT name, email FROM users WHERE role = 'admin'")
for row in cursor.fetchall():
    print(f"Админ: {row[0]}, Почта: {row[1]}")

print("\n--- 3. Сортировка по имени (А-Я) ---")
# ORDER BY сортирует. ASC - по возрастанию, DESC - по убыванию
cursor.execute("SELECT name FROM users ORDER BY name ASC")
for row in cursor.fetchall():
    print(row[0])

print("\n--- 4. Поиск по email (частичное совпадение) ---")
# LIKE ищет по шаблону. % означает "любые символы"
cursor.execute("SELECT name, email FROM users WHERE email LIKE '%startup%'")
for row in cursor.fetchall():
    print(f"{row[0]} (email: {row[1]})")

conn.close()