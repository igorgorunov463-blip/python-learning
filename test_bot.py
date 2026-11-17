import telebot
import requests
from bs4 import BeautifulSoup
import json

TOKEN = "8850649932:AAEqXDFZ9_d2cKLKSLufhNHixzqLrvPvz8M"
bot = telebot.TeleBot(TOKEN)

# Функция для общения с локальной нейросетью Ollama
def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Не удалось получить ответ от ИИ."
    except Exception as e:
        return f"Ошибка подключения к ИИ: {e}. Убедись, что Ollama запущена."

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на книгу с сайта books.toscrape.com, и я скажу её цену и попрошу ИИ оценить покупку.")

@bot.message_handler(func=lambda message: True)
def get_book_price(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "Пожалуйста, отправь правильную ссылку.")
        return

    bot.reply_to(message, "Ищу цену и спрашиваю ИИ... ⏳")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("p", class_="price_color")
        
        # Пытаемся найти название книги
        title_element = soup.find("h1")
        title = title_element.get_text() if title_element else "Неизвестная книга"
        
        if price_element:
            raw_price = price_element.get_text()
            clean_price = "".join(char for char in raw_price if char.isdigit() or char == ".")
            
            # Отправляем цену пользователю
            bot.reply_to(message, f"📚 {title}\n💰 Цена: £{clean_price}\n\n🤖 Спрашиваю ИИ, стоит ли покупать...")
            
            # Формируем запрос к ИИ
            prompt = f"Ты эксперт по книгам. Пользователь хочет купить книгу '{title}' за £{clean_price}. Стоит ли она этих денег? Дай очень краткий и четкий ответ (максимум 3 предложения)."
            
            # Получаем ответ от ИИ и отправляем
            ai_answer = ask_ai(prompt)
            bot.reply_to(message, f"🤖 Мнение ИИ:\n{ai_answer}")
            
        else:
            bot.reply_to(message, "Не удалось найти цену на этой странице.")
            
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

print("Умный бот запущен...")
bot.infinity_polling()