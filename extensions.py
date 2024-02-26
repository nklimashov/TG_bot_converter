import requests
import json

from config import values_name


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Введены одинаковые валюты {base}.')

        try:
            base_ticker = values_name[base]
        except KeyError:
            raise APIException(f'Неверное значение {base}.')

        try:
            quote_ticker = values_name[quote]
        except KeyError:
            raise APIException(f'Неверное значение {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверное значение {amount}.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/c46ef31a3c3daaf7851a2834/pair/'
                         f'{base_ticker}/{quote_ticker}/{amount}')
        total_quote = json.loads(r.content)['conversion_result']
        return total_quote
