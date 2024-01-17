import telebot
from telebot import types
bot = telebot.TeleBot('6786523965:AAEK-NVDmwdS5TXPX1M9nX3-yDlHRtiMHGo')

class User:
    def __init__(self, name, phone_number, telegram_id):
        self.name = name
        self.phone_number = phone_number
        self.telegram_id = telegram_id

users = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет! Для начала работы с ботом, пожалуйста, предоставьте следующую информацию:')
    bot.send_message(chat_id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, handle_name, chat_id)

def handle_name(message, chat_id):
    name = message.text
    bot.send_message(chat_id, 'Введите ваш номер телефона:')
    bot.register_next_step_handler(message, handle_phone_number, chat_id, name)

def handle_phone_number(message, chat_id, name):
    phone_number = message.text
    bot.send_message(chat_id, 'Введите ваш ID аккаунта Telegram:')
    bot.register_next_step_handler(message, handle_telegram_id, chat_id, name, phone_number)

def handle_telegram_id(message, chat_id, name, phone_number):
    telegram_id = message.text
    user = User(name, phone_number, telegram_id)
    users[chat_id] = user

    bot.send_message(chat_id, 'Регистрациия закончена.Благодарим вас за предоставленную информацию!')


