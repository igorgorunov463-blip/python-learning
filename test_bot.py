import telebot
import requests
from bs4 import BeautifulSoup

# Твой токен
TOKEN = "8850649932:AAEqXDFZ9_d2cKLKSLufhNHixzqLrvPvz8M"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на книгу с сайта books.toscrape.com, и я скажу её цену.")

@bot.message_handler(func=lambda message: True)
def get_book_price(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "Пожалуйста, отправь правильную ссылку.")
        return

    bot.reply_to(message, "Ищу цену... ⏳")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("p", class_="price_color")
        
        if price_element:
            raw_price = price_element.get_text()
            clean_price = "".join(char for char in raw_price if char.isdigit() or char == ".")
            bot.reply_to(message, f"💰 Цена этой книги: £{clean_price}")
        else:
            bot.reply_to(message, "Не удалось найти цену.")
            
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

print("Бот-парсер запущен...")
bot.infinity_polling()