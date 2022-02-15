from bot_token import token
from telebot import TeleBot, types
import time
from my_scripts import misc_func as mf
from my_scripts.coords_and_img import LOCAL_BUTTON

V_TB = 'v0.05'

bot = TeleBot(token)
checking = False

kb = types.ReplyKeyboardMarkup(True)
kb.row('/screen', '/info', '/pause')

kb_checking = types.ReplyKeyboardMarkup(True)
kb_checking.row('/screen', '/info')
kb_checking.row('/pause')


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
            info = file.read().split(' ')
            data['ore'] = info[5]
            data['status'] = info[7]
            data['cargo'] = info[9]
            data['minus'] = info[13]
            data['neutral'] = info[15]
            data['drill_status'] = info[17]
        line = ''
        for name, value in data.items():
            line += f'{name} : {value}\n'

        bot.send_message(message.chat.id, line)
    except FileNotFoundError:
        message('No data')


@bot.message_handler(commands=['screen'])
def output_data(message):
    mf.screen_shot()
    bot.send_photo(message.chat.id, photo=open(f'img/target_img.png', 'rb'))


@bot.message_handler(commands=['checking'])
def output_data(message):
    global checking
    checking = True
    timer = 5
    bot.send_message(message.chat.id, 'START CHECKING', reply_markup=kb_checking)
    while checking:
        data = {'status': 'None',
                'minus': 'None',
                'neutral': 'None'}
        try:
            with open('save.txt', encoding='utf-8', mode='r') as file:
                info = file.read().split(' ')
                data['status'] = info[7]
                data['minus'] = info[13]
                data['neutral'] = info[15]
        except FileNotFoundError:
            message('No data')
        if data['minus'] == 'True' or data['neutral'] == 'True':
            mf.screen_shot()
            bot.send_photo(message.chat.id, photo=open(f'img/target_img.png', 'rb'))
            timer = 15
        else:
            timer = 5
        time.sleep(timer)


@bot.message_handler(commands=['stop_checking'])
def output_data(message):
    global checking
    checking = False
    bot.send_message(message.chat.id, 'STOP CHECKING', reply_markup=kb)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, photo=open(f'img/bg.png', 'rb'), reply_markup=kb)


@bot.message_handler(commands=['pause'])
def pause(message):
    x, y, x1, y1 = LOCAL_BUTTON
    x = x + x1 // 2
    y = y + y1 // 2
    mf.click_queue([x, y])


def bot_process():
    bot.polling()
