# -*- coding: utf-8 -*-
"""
    Provides decorator functions for user authentication.
"""
import logging
from telegram import Bot
from ownbot.user import User
from ownbot.usermanager import UserManager


def requires_usergroup(*decorator_args):
    """Checks if the user has access to the decorated function.

        Checks if the user who sent the message is in the given
        user group thus has access to the decorated function.

        Args:
            group (str): The group's name.

        Returns:
            func: The decorater function.
    """

    def decorate(func):
        def call(*args, **kwargs):
            log = logging.getLogger(__name__)

            # Set offset to 1 if first argument is not type of
            # telegram.Bot (self passed).
            offset = 0
            if not isinstance(args[0], Bot):
                offset = 1
            update = args[1 + offset]

            username = update.message.from_user.name
            userid = update.message.from_user.id
            message = update.message.text
            user = User(username, userid)

            has_access = False
            for group in decorator_args:
                has_access = user.has_access(group) if not has_access else True

            if not has_access:
                log.warn("The user '{0}' with id '{1}' tried to"\
                         " execute the protected command '{2}'!"
                         .format(username, userid, message))
                return

            result = func(*args, **kwargs)
            return result

        return call

    return decorate


def assign_first_to(group):
    """Checks if the user should be added to the given group.

        Adds the user who sent the command to the given group
        if there isn't already a user assigned to this group.

        Args:
            group (str): The group's name.

        Returns:
            func: The decorater function.
    """

    def decorate(func):
        def call(*args, **kwargs):
            offset = 0
            # Set offset to 1 if first argument is not type of
            # telegram.Bot.
            if not isinstance(args[0], Bot):
                offset = 1

            bot = args[0 + offset]
            update = args[1 + offset]

            user = User(update.message.from_user.name,
                        user_id=update.message.from_user.id,
                        group=group, )
            if UserManager().group_is_empty(group):
                user.save()
                message = "Hello {0}! "\
                        "You have been added to the '{1}' group."\
                        .format(
                            update.message.from_user.first_name,
                            group
                        )
                bot.sendMessage(chat_id=update.message.chat_id, text=message)

            result = func(*args, **kwargs)
            return result

        return call

    return decorate
