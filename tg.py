from unittest.mock import call

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('6786523965:AAEK-NVDmwdS5TXPX1M9nX3-yDlHRtiMHGo')
ret = ""

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
    bot.send_message(chat_id, 'Отправьте нам свой номер телефона')
    #Создаем кнопку для отправки номера телефона
    button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, "Нажмите кнопку, чтобы отправить номер телефона", reply_markup=keyboard)
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


# @bot.message_handler(commands=['buy'])
# def buy(message, requests=None):
#     bot.send_message(message.chat.id,'Для того что бы найти магазины рядом с вами отправьте нам свою геолокацию')
#     # Создаем кнопку с запросом геолокации
#     button = types.KeyboardButton(text="Отправить геолокацию", request_location=True)
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     keyboard.add(button)
#
#     # Отправляем сообщение с кнопкой пользователю
#     bot.send_message(message.chat.id, "Нажмите кнопку, чтобы отправить геолокацию", reply_markup=keyboard)
#
#
#     search_query = message.text  # запрос пользователя
#     api_url = 'https://catalog.api.2gis.ru/3.0/items'  # URL API 2GIS
#
#     # Получение местоположения пользователя
#     lat = message.location.latitude
#     lon = message.location.longitude
#
#     # Параметры запроса
#     params = {
#         'q': search_query,
#         'type': 'branch',
#         'key': '',
#         'version': '1.3',
#         'fields': 'items.point',
#         'point': f'{lat},{lon}',  # добавляем параметр с координатами пользователя
#         'radius': 5000  # указываем радиус поиска в метрах
#     }
#
#     response = requests.get(api_url, params=params)
#
#     if response.status_code == 200:
#         data = response.json()
#
#         # Обработка полученных мест
#         for item in data['result']['items']:
#             name = item['name']
#             lat, lon = item['point']['lat'], item['point']['lon']
#
#             # Отправка места пользователю
#             bot.send_message(message.chat.id, f'{name}: {lat}, {lon}')
#     else:
#         bot.send_message(message.chat.id, 'Произошла ошибка при поиске места')


@bot.message_handler(commands=['buy'])
def buy(message):
    keyboard = InlineKeyboardMarkup()
    mas = ["Аптеки","Фаст-Фуд","Магазины"]
    chat_id = message.chat.id
    bot.send.message(chat_id, 'Отправь свое местоположение для поиска подходящего места')
    # Получаем координаты пользователя
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send.message(chat_id, 'Теперь выберем категорию мест, которые вы хотите найти')
    for i in mas:
        i = types.InlineKeyboardButton(text=f"{i}", callback_data=f"{i}")
        keyboard.add(i)







bot.polling()