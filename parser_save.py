import requests
from bs4 import BeautifulSoup
import json # Импортируем модуль для работы с JSON

print("--- Парсер с сохранением в файл ---")

url = "https://quotes.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    
    # Создаем пустой список, куда будем складывать данные
    data_to_save = []
    
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        
        # Создаем словарь для одной цитаты
        quote_dict = {
            "text": text,
            "author": author
        }
        # Добавляем словарь в общий список
        data_to_save.append(quote_dict)
        
    # Сохраняем список в JSON-файл
    filename = "quotes.json"
    with open(filename, "w", encoding="utf-8") as file:
        # indent=4 делает файл красивым (с отступами), ensure_ascii=False сохраняет русские буквы
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        
    print(f"Успех! Сохранено {len(data_to_save)} цитат в файл {filename}.")
else:
    print("Ошибка загрузки сайта.")