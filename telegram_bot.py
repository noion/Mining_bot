from bot_token import token
from queue import Queue
import telebot

V_TB = 'v0.01'

bot = telebot.TeleBot(token)

def message(text, commands=None):
    @bot.message_handler(commands=commands)
    def send_message(message):
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['info'])
def output_data(message):
    data = {'status': 'None',
            'info': 'None',
            'minus': 'None',
            'neutral': 'None',
            'cargo_info': 'None',
            'drill_status': 'None',
            'ore': 'None', }
    try:
        with open('save.txt', encoding='utf-8', mode='r') as file:
            # number_info = sum(1 for line in file)
            # if number_info > 0:
            info = file.read().split(' ')
            data['ore'] = info[5]
            data['status'] = info[7]
            data['cargo'] = info[9]
            data['minus'] = info[13]
            data['neutral'] = info[15]
            data['drill_status'] = info[17]
            # else:
            #     bot.send_message(message.chat.id, "Записей нет")

        for name, value in data.items():
            line = f'{name} : {value}'
            bot.send_message(message.chat.id, line)
    except FileNotFoundError:
        message('No data')


def bot_process():
    message("What's againe?", ['start'])
    bot.polling()

