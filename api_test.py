import requests # Импортируем установленную библиотеку

print("--- Запрос к интернету ---")

# Мы обращаемся к бесплатному API, который отдает случайные факты о котах (шутка для примера)
url = "https://catfact.ninja/fact"

# Отправляем GET-запрос (как когда ты открываешь сайт в браузере)
response = requests.get(url)

# Проверяем, что сайт ответил успешно (код 200 = OK)
if response.status_code == 200:
    # Превращаем ответ в словарь (как мы делали с файлами)
    data = response.json() 
    
    # Достаем факт по ключу "fact"
    fact = data["fact"]
    print("Случайный факт о котах:")
    print(fact)
else:
    print("Ошибка! Сайт не ответил.")

print("\n--- Погода в Саратове (и Питере) ---")
# Другой API: погода. (Не требует ключа, просто координаты)
# Координаты: Саратов (51.5, 46.0) и Питер (59.9, 30.3)
url_weather = "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=46.0&current_weather=true"

response_weather = requests.get(url_weather)
if response_weather.status_code == 200:
    weather_data = response_weather.json()
    temp = weather_data["current_weather"]["temperature"]
    wind = weather_data["current_weather"]["windspeed"]
    print(f"Сейчас в Саратове: {temp}°C, ветер {wind} км/ч.")