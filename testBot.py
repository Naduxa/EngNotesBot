#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from NotifyThread import NotifyThread
import telebot
from telebot import types
import logging
import time
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

main_reply = [u'Категории', u'Время', u'Обо мне', u'Старт']

time_reply = {u'30 секунд':30, u'10 минут':600, u'полчаса':1800, u'час':3600, u'два часа':7200}
topic_reply = {}

dictionary = []

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(*[types.KeyboardButton(name) for name in main_reply])


notify_thread = NotifyThread(bot, dictionary)

DIR_DICT = 'dataDir/dictionary'

def loadDict():
    for fname in os.listdir(DIR_DICT):
        with open(DIR_DICT + '/' + fname, 'r') as f:
            name = f.readline()
            print name
            topic_reply[name.decode('utf-8').strip()] = len(dictionary)
            lines = []
            for i, l in enumerate(f):
                if i == 0:
                    continue
                lines.append(l)
            dictionary.append(lines)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе выучить!',
        reply_markup=start_keyboard)
    print (message.from_user)
    notify_thread.addUserTime(message.from_user.id, 600)
    notify_thread.addUserTopic(message.from_user.id, 0)

@bot.message_handler(content_types=['text'])
def handle_msg(message):
    text = message.text

    if (text == u'Старт'):
        print 'Yes'
        print text
        start(message)
        return
    if text == u'Назад':
        bot.send_message(message.chat.id, 'Привет!',
                         reply_markup=start_keyboard)
        return
    if text == u'Время':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in time_reply])
        bot.send_message(message.chat.id, 'Выбери промежуток времени для слов',
                     reply_markup=keyboard)

    if text == u'Категории':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in topic_reply])
        bot.send_message(message.chat.id, 'Подпишись на тему / Отпишись от тему',
                         reply_markup=keyboard)

    if text in time_reply.keys():
        notify_thread.addUserTime(message.from_user.id, time_reply[text])
        bot.send_message(message.chat.id, 'Оки!', reply_markup=start_keyboard)

    if text in topic_reply.keys():
        notify_thread.addUserTopic(message.from_user.id, topic_reply[text])
        bot.send_message(message.chat.id, 'Оки!', reply_markup=start_keyboard)
    #if text in time_reply_keyboard.keys():

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    loadDict()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(e)  # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)

if __name__ == '__main__':
    main()