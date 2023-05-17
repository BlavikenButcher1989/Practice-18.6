import telebot
from extensions import APIException, Converter
from configs import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def echo_test(message):
    text = 'Для того, чтобы узнать стоимость валюты, введите:\n<имя валюты, цену которой вы хотите узнать>\
    <имя валюты, в которую хотите перевести>\
    <количество первой валюты> \nПример: Доллар Рубль 100 \nЧтобы увидеть список валют, введите: \n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()