import requests
from bs4 import BeautifulSoup
import csv

URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def fetch(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text

def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    quotes = []
    for block in soup.select("div.quote"):
        quotes.append({
            "text": block.select_one(".text").get_text(strip=True),
            "author": block.select_one(".author").get_text(strip=True),
        })
    return quotes

def save_to_csv(data: list[dict], path: str = "data.csv") -> None:
    if not data:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Сохранено в {path}")

if __name__ == "__main__":
    print("Загружаем страницу...")
    html = fetch(URL)
    print("Парсим данные...")
    data = parse(html)
    save_to_csv(data)
    
    for q in data[:2]:
        print(f"{q['author']}: {q['text'][:50]}...")
    print(f"Всего обработано цитат: {len(data)}")