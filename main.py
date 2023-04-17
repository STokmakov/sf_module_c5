import telebot                                  # подключаем библиотеку pyTelegramBotAPI
from extensions import APIException, Convertor  # импортируем классы из файла extensions
from config import TOKEN, exchanges             # импортируем значения констант из файла config
import traceback                                # подключаем модуль для печати или получения обратной трассировки стека

bot = telebot.TeleBot(TOKEN) # подключаем бот с использованием TOKEN

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message): # метод для вывода справки при вводе команд /start или /help
    text1 = "Пример перевода валют:"
    bot.send_message(message.chat.id, text1)
    img = open('primer.png', 'rb')
    bot.send_photo(message.chat.id, img)
    text2 = "Введите команду /values, чтобы узнать перечень поддерживаемых валют:"
    bot.send_message(message.chat.id, text2)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # метод для вывода значений валют из файла config
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message): # метод для вывода результата конвертации
    values = message.text.split(' ')
    try: # обрабатываем исключения
        if len(values) != 3: # если больше трех параметров
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:  # если не верно записали команду
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:     # остальные варианты исключений
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message, answer) # вывод

bot.polling() # Старт  постоянной обработки информации, приходящей с серверов Telegram от бота:
