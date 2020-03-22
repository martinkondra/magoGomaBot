# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Martin Kondra"

import telegram
import logging
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler
from telegram.error import NetworkError, Unauthorized
from time import sleep
from silabas import *

start_message = "Soy el mago goma y mi palabra es: "

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=start_message)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="WTF?!.")


updater = Updater(token='')
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.stop()
# updater.idle()
print('end')


def main():
    """Run the bot."""
    global update_id
    global match, current_syl
    bot = telegram.Bot(token='')
    #logger.info("Bot started as @{}".format(updater.bot.username))

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

#current_syl = {}
#pickle.dump(current_syl, open('current_syl.p', "wb"))
current_syl = pickle.load(open("current_syl.p", "rb"))
used = {}

ganaste = 'Ganaste! Envia /start para la revancha'
perdiste = 'Perdiste! Presiona /start para un nuevo match'
perdiste_used = 'Perdiste! Esa palabra ya fue usada. Presiona /start para un nuevo match'
perdiste_notword = 'Perdiste! Esa palabra no existe. Presiona /start para un nuevo match'

def echo(bot):
    global update_id
    global current_syl, used
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        username = update.message.from_user.username
        #user_id = update.message.from_user.id
        message_id = update.message.message_id
        chat_id = update.message.chat.id
        print(username, chat_id, message_id)
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            if update.message.text == '/start':
                used[username] = []
                word = random.choice(words)
                print('bot: ' + word)
                current_syl[username] = get_last(word)
                #update.message.reply_text(start_message + word)
                bot.sendMessage(chat_id=chat_id, text=(start_message + word))
                #print(current_syl)
            else:
                word = update.message.text.lower()
                print('user: ' + word)
                valid = validate(word, current_syl[username], used[username])
                if not valid:
                    #update.message.reply_text('Perdiste! Presiona /start para un nuevo match')
                    bot.sendMessage(chat_id=chat_id, text=(perdiste))
                    return
                elif valid=='used':
                    #update.message.reply_text('Perdiste! Esa palabra ya fue usada. Presiona /start para un nuevo match')
                    bot.sendMessage(chat_id=chat_id, text=(perdiste_used))
                    return
                elif valid == 'notword':
                    #update.message.reply_text('Perdiste! Esa palabra no existe. Presiona /start para un nuevo match')
                    bot.sendMessage(chat_id=chat_id, text=(perdiste_notword))
                    return
                current_syl[username] = get_last(word)
                answer = choose_word(current_syl[username])
                print('bot: ' + str(answer))
                if answer==False:
                    #update.message.reply_text('Ganaste! Envia /start para la revancha')
                    bot.sendMessage(chat_id=chat_id, text=(ganaste))
                else:
                    current_syl[username] = get_last(answer)
                    #update.message.reply_text(answer)
                    bot.sendMessage(chat_id=chat_id, text=(answer))
    pickle.dump(current_syl, open('current_syl.p', "wb"))


if __name__ == '__main__':
    main()