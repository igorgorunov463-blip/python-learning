def calculate_salary():
    try:
        # Программа просит зарплату
        salary = float(input("Введи свою зарплату в рублях: "))
        tax = float(input("Введи процент налога (например, 13): "))
        
        # Считаем зарплату после налога
        tax_amount = salary * (tax / 100)
        net_salary = salary - tax_amount
        
        print(f"Твоя зарплата после вычета налога: {round(net_salary, 2)} руб.")
        
    except ValueError:
        # Если ввели не число, а текст, срабатывает этот блок
        print("Ошибка! Нужно вводить только числа, без букв и пробелов.")
        print("Давай попробуем еще раз...")
        calculate_salary() # Функция вызывает саму себя, чтобы начать заново

# Запускаем программу
calculate_salary()