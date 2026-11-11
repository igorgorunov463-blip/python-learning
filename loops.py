print("--- 1. Цикл for (считаем до 5) ---")
# range(1, 6) означает: взять числа от 1 до 5 (6 не включается)
for i in range(1, 6):
    print("Шаг номер", i)

print("\n--- 2. Цикл while (ждем правильный пароль) ---")
password = ""
# Цикл будет работать, пока пароль НЕ равен "python123"
while password != "python123":
    password = input("Введи пароль (подсказка: python123): ")
    if password != "python123":
        print("Неверно! Попробуй еще раз.")

print("Доступ разрешен!")