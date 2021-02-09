import config
import telebot
import requests
import json
import random
import data_storage
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
URL = data_storage.URL
quotes = data_storage.QUOTE_STORAGE
thinking = data_storage.THINKING


def send_sticker(path, msg_cht_id, directory="{}"):
    sticker = open(directory.format(path), "rb")
    bot.send_sticker(msg_cht_id, sticker)


def get_weather_forecast(city, url=URL):
    data = json.loads(requests.get(url.format(city)).content)
    if data["cod"] == "404":
        result = "Wrong city name"
    else:
        temperature = str(int(data["main"]["temp"]) - 273)
        wind = str(data["wind"]["speed"])
        weather_type = data["weather"][0]["main"]
        result = "Temperature: {} celsius degrees\nWind {} m/s\nGenerally: {}".format(temperature, wind, weather_type)
    return result


@bot.message_handler(commands=["start"])
def welcome(message):
    send_sticker("hello.tgs", message.chat.id)
    # make a keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Weather forecast")
    button2 = types.KeyboardButton("Get new knowledge")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Welcome, {0.first_name}\nMy name is <b>{1.first_name}</b>, I will help"
                                      " you to find weather forecast and some other things."
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def answer_messages(message):  # Название функции не играет никакой роли
    if message.chat.type == "private":
        if message.text == "Weather forecast":
            bot.send_message(message.chat.id, "Give me city name, please, starting with !")
        elif message.text[0] == "!":
            city = message.text[1:]
            answer = get_weather_forecast(city=city)
            if answer == "Wrong city name":
                send_sticker("wrongans.tgs", message.chat.id)
            elif answer.endswith("Rain"):
                send_sticker("rain.tgs", message.chat.id)
            elif answer.endswith("Clear"):
                send_sticker("clear.tgs", message.chat.id)
            bot.send_message(message.chat.id, answer)

        elif message.text == "Get new knowledge":
            send_sticker(thinking[random.randint(0, len(thinking) - 1)], message.chat.id)
            bot.send_message(message.chat.id, quotes[random.randint(0, len(quotes) - 1)])

        else:
            bot.send_message(message.chat.id, "Wrong command")


bot.polling(none_stop=True)

