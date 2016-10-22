# -*- coding: utf-8 -*-
"""
    Provides the ownbot AdminCommands class.
"""
from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler

from ownbot.auth import requires_usergroup
from ownbot.usermanager import UserManager


class AdminCommands(object):  # pylint: disable=too-few-public-methods
    """
        Provides admin command handlers for user/group
        management.

        Args:
            dispatcher (telegram.dispatcher): Command dispatcher to register the
                admin commands.
    """

    def __init__(self, dispatcher):
        self.__usermanager = UserManager()
        self.__dispatcher = dispatcher
        self.__register_handlers()

    def __register_handlers(self):
        """
            Registers the admin commands.
        """
        self.__dispatcher.add_handler(CommandHandler("adminhelp",
                                                     self.__admin_help))
        self.__dispatcher.add_handler(CommandHandler("users", self.__get_users))
        self.__dispatcher.add_handler(CommandHandler("adduser",
                                                     self.__add_user,
                                                     pass_args=True))
        self.__dispatcher.add_handler(CommandHandler(
            "rmuser", self.__rm_user, pass_args=True))

    @staticmethod
    @requires_usergroup("admin")
    def __admin_help(bot, update):
        """Command handler function for `adminhelp` command.

            Sends a list of all available commands to the
            client.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
        """
        message = """
*Available Admin Commands*
/users - Lists all registered users.
/adduser - Adds a user to a group.
/rmuser - Removes a user from a group.
        """

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=message,
                        parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    @requires_usergroup("admin")
    def __get_users(bot, update):
        """Command handler function for `users` command.

            Sends a list of all currently registered
            users.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
        """
        message = str()
        config = UserManager().config
        if not config:
            message = "No users registered"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)

        for group, data in config.items():
            message += "*{0}*\n".format(group)
            if data.get("users"):
                message += "  verified users:\n"
                for user in data.get("users"):
                    message += "    - {0} with id {1}\n" \
                            .format(user.get("username"),
                                    user.get("id"))

            if data.get("unverified"):
                message += "  unverified users:\n"
                for user in data.get("unverified"):
                    message += "    - {0}\n".format(user)

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=message,
                        parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    @requires_usergroup("admin")
    def __add_user(bot, update, args):
        """Command handler function for `adduser` command.

            Adds a telegram user to a usergroup.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
                args (list): The command's arguments.
        """
        if len(args) != 2:
            message = "Usage: adduser <user> <group>"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            return

        username = args[0]
        group = args[1]
        if not UserManager().add_user(username, group):
            message = "The user '{0}' is already in the group '{1}'!" \
                    .format(username, group)

        else:
            message = "Added user '{0}' to the group '{1}'." \
                    .format(username, group)

        bot.sendMessage(chat_id=update.message.chat_id, text=message)

    @staticmethod
    @requires_usergroup("admin")
    def __rm_user(bot, update, args):
        """Command handler function for `rmuser` command.

            Removes a telegram user from a usergroup.

            Args:
                bot (telegram.Bot): The bot object.
                update (telegram.Update): The sent update.
                args (list): The command's arguments.
        """
        if len(args) != 2:
            message = "Usage: rmuser <user> <group>"
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            return

        username = args[0]
        group = args[1]
        if UserManager().rm_user(username, group):
            message = "Removed user '{0}' from the group '{1}'.".format(
                username, group)
        else:
            message = "The user '{0}' could not be found in the group '{1}'!"\
                    .format(username, group)

        bot.sendMessage(chat_id=update.message.chat_id, text=message)
