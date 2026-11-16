import requests
from bs4 import BeautifulSoup

print("--- Парсер заголовков новостей ---")

# 1. Заходим на сайт (используем сайт с новостями, например, Habr или Lenta)
# Для примера возьмем страницу с цитатами (она не блокирует парсеры)
url = "https://quotes.toscrape.com/"

# Отправляем запрос
response = requests.get(url)

if response.status_code == 200:
    # 2. Скармливаем HTML-код библиотеке BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 3. Ищем нужные элементы на странице.
    # В HTML у каждой цитаты есть класс "text" и "author".
    quotes = soup.find_all("div", class_="quote")
    
    print(f"Найдено цитат: {len(quotes)}\n")
    
    # 4. Перебираем каждую цитату и вытаскиваем текст
    for i, quote in enumerate(quotes, 1):
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        
        print(f"{i}. {text}")
        print(f"   Автор: {author}\n")
        
else:
    print("Не удалось загрузить сайт. Код ошибки:", response.status_code)