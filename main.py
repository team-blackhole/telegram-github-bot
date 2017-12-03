#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sys import path
from configparser import ConfigParser
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
path.append("src/")
from src.GitApi import GitHub
from flask import Flask, request
import subprocess
import urllib

# Bot Configuration
config = ConfigParser()
config.read_file(open('config.ini'))

up = Updater(token=config['DEFAULT']['token'])
PORT = config['DEFAULT']['port']
job = up.job_queue
dispatcher = up.dispatcher


# Home function
def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "I notify selected github push alarms!\n"
    msg += "/listen - Start notify in this room \n"

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))


# Function to list the repositories
def listing(bot, update, args):
    gh = GitHub()
    for user in args:
        bot.send_message(chat_id=update.message.chat_id,
                         text='{0} Listing the user repositories '
                         .format('\U0001F5C4') +
                         '[{0}](https://github.com/{0}) {1}'.format(
                             user, Emoji.WHITE_DOWN_POINTING_BACKHAND_INDEX),
                         parse_mode=ParseMode.MARKDOWN)

        bot.send_message(chat_id=update.message.chat_id,
                         text=gh.get_repos(user))


def add_chat_id(chat_id):
    response = urllib.request.urlopen(url='http://127.0.0.1:{0}/add/{1}'.format(PORT, chat_id), timeout=5)
    print(response)


def listening(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text='Start listening repositories...',
                    parse_mode=ParseMode.MARKDOWN)
    is_github_listening = True
    add_chat_id(update.message.chat_id)
    return
    
    
# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('listing', listing, pass_args=True))
dispatcher.add_handler(CommandHandler('listen', listening))


# Start the program
up.start_polling()
proc = subprocess.Popen(["python", "push_server.py"])

