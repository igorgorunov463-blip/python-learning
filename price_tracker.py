import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from datetime import datetime
from time import sleep
import random

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("price_tracker.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def get_price(url, retries=3):
    """Получение цены с повторными попытками"""
    for attempt in range(1, retries + 1):
        try:
            # ВАЖНО: добавляем response.encoding = 'utf-8'
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'  # Принудительно ставим правильную кодировку
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            price_element = soup.find("p", class_="price_color")
            
            if not price_element:
                logging.warning(f"Элемент цены не найден (попытка {attempt})")
                continue
            
            # Магия очистки: оставляем только цифры и точку
            raw_price = price_element.get_text()
            clean_price = "".join(char for char in raw_price if char.isdigit() or char == ".")
            
            return float(clean_price)
            
        except (requests.RequestException, ValueError) as e:
            logging.warning(f"Ошибка при попытке {attempt}: {e}")
            sleep(random.uniform(1, 3))
            
    logging.error("Не удалось получить цену после всех попыток")
    return None

def save_history(price, url):
    """Сохранение полной истории цен с датой и статистикой"""
    filename = "price_history.json"
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    
    if url not in data:
        data[url] = {"history": [], "last_price": None}
    
    item = data[url]
    old_price = item["last_price"]
    
    item["history"].append({
        "date": datetime.now().isoformat(timespec="seconds"),
        "price": price
    })
    item["last_price"] = price
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return old_price, item["history"]

def analyze_history(history):
    """Анализ: минимум, максимум, тренд, процент изменения"""
    if not history:
        return None
    
    prices = [h["price"] for h in history]
    stats = {
        "min": min(prices),
        "max": max(prices),
        "avg": round(sum(prices) / len(prices), 2),
        "count": len(prices),
        "trend": prices[-1] - prices[0] if len(prices) > 1 else 0,
    }
    return stats

def notify(title, message):
    """Уведомление в консоль + опционально Windows toast"""
    print(f"\n🔔 {title}")
    print(f"   {message}")
    try:
        # На Mac эта библиотека не сработает (она для Windows), 
        # но код не упадет из-за try/except
        from win10toast import ToastNotifier  
        ToastNotifier().show_toast(title, message, duration=5, threaded=True)
    except ImportError:
        pass 

def get_product_title(url):
    """Заодно вытащим название товара — для красоты"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")
        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else "Неизвестный товар"
    except Exception:
        return "Неизвестный товар"

# === Основная логика ===
if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    
    title = get_product_title(url)
    logging.info(f"Проверяем: {title}")
    
    current_price = get_price(url)
    
    if current_price is None:
        logging.error("Не удалось получить цену, выходим.")
    else:
        old_price, history = save_history(current_price, url)
        stats = analyze_history(history)
        
        print(f"\n📚 {title}")
        print(f"💰 Текущая цена: £{current_price}")
        
        if stats:
            print(f"📊 Мин: £{stats['min']} | Макс: £{stats['max']} | "
                  f"Средняя: £{stats['avg']} | Записей: {stats['count']}")
        
        if old_price is not None:
            diff = current_price - old_price
            diff_pct = (diff / old_price) * 100
            
            print(f"🕐 Прошлая цена: £{old_price} (изменение: {diff:+.2f}, {diff_pct:+.1f}%)")
            
            if diff < 0:
                notify("🎉 Цена упала!", f"{title}: £{old_price} → £{current_price} (-{abs(diff_pct):.1f}%)")
            elif diff > 0:
                notify("📈 Цена выросла", f"{title}: £{old_price} → £{current_price} (+{diff_pct:.1f}%)")
            else:
                print("➡️ Цена не изменилась.")
        else:
            print("✅ Это первое сохранение цены. Начинаем следить!")