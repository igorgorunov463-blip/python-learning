import os
from dotenv import load_dotenv

# Эта команда загружает данные из файла .env в систему
load_dotenv()

# Теперь мы можем достать секрет по имени
secret_key = os.getenv("MY_SECRET_KEY")

if secret_key:
    print(f"Успех! Мы нашли секретный ключ: {secret_key}")
    print("Теперь мы можем безопасно использовать его для подключения к базе данных или API.")
else:
    print("Ключ не найден. Проверь файл .env")

# --- ЧТЕНИЕ ДОКУМЕНТАЦИИ ---
print("\n--- Разбор чужого кода ---")
# Представь, что мы прочитали документацию библиотеки math и нашли функцию sqrt (квадратный корень)
import math

# В документации написано: math.sqrt(x) возвращает квадратный корень из x
try:
    number = float(input("Введи число для вычисления корня: "))
    result = math.sqrt(number)
    print(f"Квадратный корень из {number} равен {result}")
except ValueError:
    print("Ошибка! Нельзя извлечь корень из отрицательного числа.")