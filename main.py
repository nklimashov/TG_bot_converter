import telebot

from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать! \nЧтобы конвертировать валюту - введите через "пробел" 3 параметра:' \
           '\n"<имя валюты, цену на которую надо узнать> - <имя валюты, цену в которой надо узнать> - ' \
           '<количество переводимой валюты>".\n\n' \
           'Пример: "Рубли Доллары 4000"\n\nДоступные валюты можно посмотреть по команде: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для перевода валюты:'
    for key in values_name.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.lower().split(' ')

        if len(value) != 3:
            raise APIException('Неверное кол-во параметров.')

        base, quote, amount = value
        total_quote = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_quote} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
