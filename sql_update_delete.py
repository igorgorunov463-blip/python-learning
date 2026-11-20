import sqlite3

conn = sqlite3.connect("startup.db")
cursor = conn.cursor()

# --- UPDATE (Обновление) ---
# Допустим, Иван решил стать админом
print("--- 1. Обновляем роль Ивана на 'admin' ---")
cursor.execute("UPDATE users SET role = 'admin' WHERE name = 'Иван'")
conn.commit()
print("Роль обновлена.")

# --- SELECT (Проверяем, что обновилось) ---
cursor.execute("SELECT name, role FROM users WHERE name = 'Иван'")
print(f"Проверка: Иван теперь {cursor.fetchone()[1]}")

# --- DELETE (Удаление) ---
# Допустим, Анна удалила аккаунт
print("\n--- 2. Удаляем Анну из базы ---")
cursor.execute("DELETE FROM users WHERE name = 'Анна'")
conn.commit()
print("Анна удалена.")

# --- SELECT (Проверяем, что осталось) ---
print("\n--- 3. Оставшиеся пользователи ---")
cursor.execute("SELECT name, email FROM users")
for row in cursor.fetchall():
    print(f"Имя: {row[0]} | Email: {row[1]}")

conn.close()