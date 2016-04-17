#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Provides a simple private telegram bot example.

    Provides an example telegram-bot using the
    authentication decorators from private-telegram-bot.
"""

from telegram.ext import Updater

from ownbot.auth import requires_usergroup, assign_first_to

TOKEN = open("token.txt").read().strip()


# The first client who sends the '/start' command will be added
# to the admins group.
@assign_first_to("admins")
# If a user wants to execute the '/start' command he has to be
# a member of the 'users' group. Otherwise the decorator will not
# execute the handler function.
@requires_usergroup("users")
def start_handler(bot, update):
    """Handles the command '/start'.

        Sends a Hello World message to the client.
    """
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello World")


def main():
    """
        Simple private telegram bot example.
    """
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler("start", start_handler)
    updater.start_polling()

if __name__ == "__main__":
    main()
