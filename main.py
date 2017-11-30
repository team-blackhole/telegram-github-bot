#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sys import path
from configparser import ConfigParser
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
path.append("src/")
from src.GitApi import GitHub
import grequests

# Bot Configuration
config = ConfigParser()
config.read_file(open('config.ini'))

# Connecting the telegram API
# Updater will take the information and dispatcher connect the message to
# the bot
print(config['DEFAULT']['token'])
up = Updater(token="token")
job = up.job_queue
dispatcher = up.dispatcher

# Github wekhooks
async_list = []


# Home function
def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "What would you like to do? \n"
    msg += "/listing + username - List your repositories \n"
    msg += "/info + username - shows your information \n"
    msg += "Ex: /listing HeavenH | /info HeavenH"

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def end(bot, update):
    print("end")
    exit(0)

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


def check_github_push(chat_id):
    print("checking")

    if is_github_listening != True:
        return

    print(action_item)
    if async_list == []:
        return
    else:
        bot.send_message(chat_id=chat_id,
                text='Event: ',
                parse_mode=ParseMode.MARKDOWN)



def listening(bot, update):
    print("listen")
    # gh = GitHub()
    # print(args)
    bot.send_message(chat_id=update.message.chat_id,
                    text='Start listening repositories...:',
                    parse_mode=ParseMode.MARKDOWN)
    is_github_listening = True

    action_item = grequests.get("https://github.com/", hooks = {'response' : check_github_push(chat_id)})
    

    # Add the task to our list of things to do via async

    

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('end', end))
dispatcher.add_handler(CommandHandler('listing', listing, pass_args=True))
dispatcher.add_handler(CommandHandler('listen', listening))

# job.run_repeating(check_github_push(update.message.chat_id, interval=1, first=0))

# dispatcher.add_handler(CommandHandler('info', info, pass_args=True))

# Start the program
up.start_polling()
up.idle()

# Developed by Heaven, Jr750ac, Pedro Souza, Israel Sant'Anna all rights
# reserved