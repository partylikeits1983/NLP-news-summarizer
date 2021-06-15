from datetime import date, time, tzinfo, timezone, datetime
import datetime
import pytz
import schedule
import time

import csv
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import logging

import os
from os import listdir
from os.path import isfile, join

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = 'your token'

today = date.today()

bot = telegram.Bot(TOKEN)


def start(update: Update, context: CallbackContext) -> None:

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    keyboard = [['/update', '/info']]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


    bot.sendMessage(update.message.chat_id, text='This python script scrapes all text from news articles on cointelegraph.com'
                              ' and then uses https://huggingface.co/transformers/ to summarize the text.'
                              ' planned features include adding PDF support through LaTex for readability'
                              ' the point of this bot is to distill a large amount of complex information.'
                              ' the NLP models are pretty good for summarization as you will be able to tell.'
                              ' Articles are updated every 12 hours', reply_markup=reply_markup)


    from datetime import datetime
    user = update.message.from_user
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    fullname = "{} {}".format(first_name, last_name)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logfile = [dt_string, chat_id, fullname, username, 'update']

    with open('/home/ubuntu/Desktop/telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: Start". format(dt_string, first_name, last_name , username, chat_id))


def news(update: Update, context: CallbackContext) -> None:

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    # list files for loop
    path = '/home/ubuntu/Desktop/articles/summaries/'

    files = os.listdir(path)

    for f in files:
        p = path + f
        file = open(p, "r")
        filestr = file.read()
        bot.sendMessage(update.message.chat_id, text=filestr)


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("your token", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("update", news))


    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
