# -*- coding: utf-8 -*-
"""Provides decorator functions for user authentication.
"""
from user import User

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
        def call(bot, update):
            user = User(update.message.from_user.id)
            if not user.has_access(group):
                return
            result = func(bot, update)
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
        def call(bot, update):
            user = User(
                update.message.from_user.id,
                first_name=update.message.from_user.first_name,
                last_name=update.message.from_user.last_name,
                group=group
            )
            # Save the user as an admin if there isn't already
            # an admin.
            if user.group_empty(group):
                user.save()
                message = "Hello {0}! "\
                        "You have been added to the {1} group."\
                        .format(
                            update.message.from_user.first_name,
                            group
                        )
                bot.sendMessage(chat_id=update.message.chat_id, text=message)

            result = func(bot, update)
            return result
        return call
    return decorate
