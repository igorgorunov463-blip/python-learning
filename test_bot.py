import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

TOKEN = "8850649932:AAEqXDFZ9_d2cKLKSLufhNHixzqLrvPvz8M"
bot = telebot.TeleBot(TOKEN)

# Ссылки на книги (для теста)
BOOKS = {
    "book1": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "book2": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "book3": "http://books.toscrape.com/catalogue/soumission_998/index.html"
}

def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3.2", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["response"]
        return "Не удалось получить ответ от ИИ."
    except Exception as e:
        return f"Ошибка ИИ: Убедись, что Ollama запущена."

@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем клавиатуру с кнопками
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📘 Книга 1", callback_data="book1")
    btn2 = types.InlineKeyboardButton("📗 Книга 2", callback_data="book2")
    btn3 = types.InlineKeyboardButton("📕 Книга 3", callback_data="book3")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, "Привет! Выбери книгу, чтобы узнать её цену и мнение ИИ:", reply_markup=markup)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in BOOKS:
        url = BOOKS[call.data]
        bot.answer_callback_query(call.id, "Загружаю данные...")
        bot.send_message(call.message.chat.id, "Ищу цену и спрашиваю ИИ... ⏳")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            
            price_element = soup.find("p", class_="price_color")
            title_element = soup.find("h1")
            title = title_element.get_text() if title_element else "Неизвестная книга"
            
            if price_element:
                clean_price = "".join(c for c in price_element.get_text() if c.isdigit() or c == ".")
                bot.send_message(call.message.chat.id, f"📚 {title}\n💰 Цена: £{clean_price}\n\n🤖 Спрашиваю ИИ...")
                
                prompt = f"Книга '{title}' стоит £{clean_price}. Стоит ли её покупать? Дай краткий ответ (до 3 предложений)."
                ai_answer = ask_ai(prompt)
                bot.send_message(call.message.chat.id, f"🤖 Мнение ИИ:\n{ai_answer}")
            else:
                bot.send_message(call.message.chat.id, "Не удалось найти цену.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Ошибка: {e}")

print("Бот с кнопками запущен...")
bot.infinity_polling()