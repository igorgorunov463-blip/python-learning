import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

TOKEN = "8850649932:AAEqXDFZ9_d2cKLKSLufhNHixzqLrvPvz8M"
bot = telebot.TeleBot(TOKEN)

BOOKS = {
    "book1": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "book2": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
}

def ask_ai(title, price):
    url = "http://localhost:11434/api/generate"
    prompt = f"Книга '{title}' стоит {price}. Стоит ли её покупать? Дай краткий ответ (до 3 предложений)."
    try:
        response = requests.post(url, json={"model": "llama3.2", "prompt": prompt, "stream": False}, timeout=60)
        return response.json()["response"] if response.status_code == 200 else "ИИ не ответил."
    except:
        return "Ошибка ИИ. Убедись, что Ollama запущена."

# --- ПАРСЕР ДЛЯ ЛЮБОГО САЙТА ---
def get_price_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Пытаемся найти цену по разным популярным классам и тегам
    price_element = soup.find("p", class_="price_color") # books.toscrape
    if not price_element:
        price_element = soup.find(class_="price") # общий класс
    if not price_element:
        price_element = soup.find(itemprop="price") # микроразметка
    if not price_element:
        price_element = soup.find(class_="product-price")

    # Название товара
    title_element = soup.find("h1")
    title = title_element.get_text(strip=True) if title_element else "Товар без названия"
    
    if price_element:
        # Очищаем от мусора, оставляем цифры и точки/запятые
        raw_price = price_element.get_text()
        clean_price = "".join(c for c in raw_price if c.isdigit() or c in ".,")
        return title, clean_price
    return title, None

# --- ГЛАВНОЕ МЕНЮ ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📘 Книга 1", callback_data="book1")
    btn2 = types.InlineKeyboardButton("📗 Книга 2", callback_data="book2")
    btn3 = types.InlineKeyboardButton("🔗 Своя ссылка", callback_data="custom_link")
    btn4 = types.InlineKeyboardButton("❓ Помощь", callback_data="help")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Выбери товар из списка или отправь свою ссылку:", reply_markup=main_menu())

# --- ОБРАБОТКА КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in BOOKS:
        process_url(call.message.chat.id, BOOKS[call.data])
    elif call.data == "custom_link":
        bot.send_message(call.message.chat.id, "Отправь мне ссылку на товар с любого сайта (начинающуюся с http):")
    elif call.data == "help":
        text = "ℹ️ **Как это работает:**\n1. Нажми на книгу или отправь свою ссылку.\n2. Бот парсит цену с сайта.\n3. Локальный ИИ (Ollama) говорит, стоит ли покупать.\n\n⚠️ Если ссылка на крупный маркетплейс (Ozon, WB, Amazon), они могут блокировать парсеры."
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# --- ОБРАБОТКА ТЕКСТА (СВОЯ ССЫЛКА) ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith("http"):
        process_url(message.chat.id, message.text.strip())
    else:
        bot.reply_to(message, "Пожалуйста, отправь ссылку (начинающуюся с http) или нажми /start.")

# --- ЛОГИКА ПАРСИНГА И ОТВЕТА ---
def process_url(chat_id, url):
    bot.send_message(chat_id, "Ищу цену... ⏳")
    try:
        title, price = get_price_from_url(url)
        if price:
            bot.send_message(chat_id, f"📦 {title}\n💰 Цена: {price}\n\n🤖 Спрашиваю ИИ...")
            ai_answer = ask_ai(title, price)
            bot.send_message(chat_id, f"🤖 Мнение ИИ:\n{ai_answer}")
        else:
            bot.send_message(chat_id, "❌ Не удалось найти цену на этой странице. Возможно, сайт блокирует парсинг или структура нестандартная.")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Ошибка: {e}")

print("Мульти-бот запущен...")
bot.infinity_polling()