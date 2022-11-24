import telebot
from config import keys, TOKEN
from extensions import Converter,ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать:'
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text
    text = 'Выберите валюту, в которую конвертровать:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text
    text = 'Выберите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = int(message.text)
    try:
        new_price = Converter.convert(base, sym, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена{amount} {base} в {sym} : {new_price}'
        bot.send_message(message.chat.id, text)


bot.polling()

