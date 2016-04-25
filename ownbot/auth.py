# -*- coding: utf-8 -*-
"""Provides decorator functions for user authentication.
"""
from telegram import Bot
from ownbot.user import User

def requires_usergroup(group):
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
            offset = 0
            # Set offset to 1 if first argument is not type of
            # telegram.Bot.
            if not isinstance(args[0], Bot):
                offset = 1

            update = args[1 + offset]

            user = User(
                update.message.from_user.name,
                update.message.from_user.id)
            if not user.has_access(group):
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

            user = User(
                update.message.from_user.name,
                user_id=update.message.from_user.id,
                group=group,
            )
            if user.group_empty(group):
                user.save()
                message = "Hello {0}! "\
                        "You have been added to the {1} group."\
                        .format(
                            update.message.from_user.first_name,
                            group
                        )
                bot.sendMessage(chat_id=update.message.chat_id, text=message)

            result = func(*args, **kwargs)
            return result
        return call
    return decorate
