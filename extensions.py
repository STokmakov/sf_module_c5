import json                               # Для парсинга полученных ответов подключаем встроенную библиотеку JSON
import requests                           # подключаем библиотеку requests для получения курса валют по API
from config import exchanges, KEYCONVERT  # импортируем значения констант из файла config

class APIException(Exception):
    """ Класс иcключений APIException"""
    pass


class Convertor:
    """ Класс Convertor"""
    @staticmethod
    def get_price(base, quote, amount):   # метод вывода цены валюты
        try:
            base_key = exchanges[base.lower()]
        except KeyError: # исключение для первой валюты
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[quote.lower()]
        except KeyError: # исключение для второй валюты
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == sym_key:  # если ввели одинаковые валюты
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError: # исключение для неправильного ввода колличества
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f" https://v6.exchangerate-api.com/v6/{KEYCONVERT}/pair/{base_key}/{sym_key}") # получаем значение курса валюты по API
        resp = json.loads(r.content) # получаем значение с использованием библиотеки json для удобного представления
        new_price = resp['conversion_rate'] * amount # вычисляем цену
        new_price = round(new_price, 3) # округляем значение с помощью встроенной функции round()
        message =  f"Цена {amount} {base} в {quote} : {new_price}" # формируем сообщение для пользователя
        return message # возвращаем сообщение в переменной massage
