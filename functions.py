# Создаем функцию с помощью ключевого слова def
def calculate_budget(income, rent, food):
    """Эта функция считает остаток денег. (Это документация функции)"""
    expenses = rent + food
    remainder = income - expenses
    
    # Функция возвращает результат с помощью return
    return remainder

def check_goal(remainder):
    """Функция проверяет, достаточно ли денег"""
    if remainder >= 50000:
        return "Ты откладываешь отлично! Питер ждет."
    else:
        return "Нужно больше зарабатывать или меньше тратить."

# --- Вызываем функции ---
print("--- Тест бюджета 1 ---")
# Передаем данные в функцию (120к доход, 40к аренда, 20к еда)
money_left = calculate_budget(120000, 40000, 20000)
print("Остаток:", money_left)

# Передаем результат в другую функцию
status = check_goal(money_left)
print("Вердикт:", status)

print("\n--- Тест бюджета 2 ---")
money_left_2 = calculate_budget(100000, 30000, 25000)
print("Остаток:", money_left_2)
print("Вердикт:", check_goal(money_left_2))

# --- Функция с аргументом по умолчанию ---
def greet(name="Друг"):
    print(f"Привет, {name}! Готов учить Python?")

print("\n--- Приветствия ---")
greet("Сергей") # Передали имя
greet()         # Не передали имя, сработает значение по умолчанию