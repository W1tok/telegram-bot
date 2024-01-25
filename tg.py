from unittest.mock import call
import math
import requests
import telebot
from telebot import types
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from telebot.types import InlineKeyboardMarkup

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
    # Создаем кнопку для отправки номера телефона
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

# def get_user_location(message):
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = KeyboardButton("Отправить местоположение", request_location=True)
#     keyboard.add(button)
#
#     bot.send_message(message.chat.id, "Пожалуйста, отправьте свое местоположение.", reply_markup=keyboard)
#     time.sleep(10)
#     latitude = message.location.latitude
#     longitude = message.location.longitude
#     return latitude, longitude
#
#
#


@bot.message_handler(commands=['buy'])
def buy(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Отправить геолокацию", request_location=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, "Пожалуйста, отправьте свою геолокацию, нажав на кнопку", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    jr = 1
    keyboard = types.ReplyKeyboardMarkup()
    lat = message.location.latitude
    lon = message.location.longitude
    mas = ["Аптеки", "Фаст-Фуды", "Магазины"]
    bot.send_message(message.chat.id, 'Теперь выберем категорию мест, которые вы хотите найти')
    for i in mas:
        keyboard.add(InlineKeyboardButton(text=f"{i}", callback_data=f"{i}"))
        bot.send_message(message.chat.id, f"вариант{jr}",reply_markup=keyboard )
        jr +=1
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call,message):


    user_id = call.from_user.id
    chat_id = message.chat.id
    option = call.data


    bot.send_message(chat_id,
                      "Теперь давайте определимся c конкретным местом(филлиалом).Для этого напишите название места или филлиала")
    mesto = message.text

    bot.send_message(chat_id, "В каком радиусе вы хотите сделать поиск")
    radius = message.text
    url = f"https://nominatim.openstreetmap.org/search?format=json&lat={lat}&lon={lon}&{radius}&q={option + mesto}"

    # Отправляем запрос и оплучаем  ответ в формате json
    respone = requests.get(url)
    data = respone.json()

    # Формируем ответ
    if len(data) > 0:
        keyboard = InlineKeyboardMarkup()
        for i in data:
            place_lat = i['lat']
            place_lon = i['lon']

            # Вычисляем расстояние от пользователя до места
            distance = calculate_distance(lat, lon, float(place_lat), float(place_lon))

            button_text = f"{i['place_name']} ({round(distance, 2)} км)"
            keyboard.add(InlineKeyboardButton(button_text, callback_data=f"{place_lat},{place_lon}"))

        bot.send_message(chat_id, "Выберете место", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'Место не найдено')


def calculate_distance(lat1, lon1, lat2, lon2):
    distance = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
    return distance


bot.polling()
