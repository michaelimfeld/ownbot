# -*- coding: utf-8 -*-
"""
    Provides a unit test class for the ownbot.admincommands module.
"""
from datetime import datetime
from unittest import TestCase
from mock import patch, Mock

from telegram import Bot, Update, Message, User, Chat
from telegram.ext import Dispatcher


# Patch decorators before module load
def dummy_decorator(*_):
    """Returns a dummy decorator"""

    def decorate(func):
        """Decorator func"""

        def call(*args, **kwargs):
            """Call func"""
            return func(*args, **kwargs)

        return call

    return decorate


import ownbot.auth
ownbot.auth.requires_usergroup = dummy_decorator

from ownbot.admincommands import AdminCommands


class TestAdminCommands(TestCase):  # pylint: disable=too-many-public-methods
    """
        Provides unit tests for the ownbot.admincommands module.
    """

    @staticmethod
    def __get_dummy_update():
        """Returns a dummy update instance"""
        user = User(1337, "@foouser")
        chat = Chat(1, None)
        message = Message(1, user, datetime.now(), chat)
        return Update(1, message=message)

    def test_init(self):
        """
            Test init function of admincommands class
        """
        with patch("ownbot.admincommands.UserManager"):
            dispatcher = Mock(spec=Dispatcher)
            AdminCommands(dispatcher)
            self.assertTrue(dispatcher.add_handler.called)

    def test_admin_help(self):
        """
            Test admin help command
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        AdminCommands._AdminCommands__admin_help(  # pylint: disable=no-member, protected-access
            bot, update)
        self.assertTrue(bot.sendMessage.called)

    def test_get_users_no_config(self):
        """
            Test get users command if no users are registered
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            usrmgr_mock.return_value.config = {}
            AdminCommands._AdminCommands__get_users(  # pylint: disable=no-member, protected-access
                bot, update)
        self.assertTrue(bot.sendMessage.called)

    def test_get_users(self):
        """
            Test get users command
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            config = {"foogroup": {"users": [{"id": 1337,
                                              "username": "@foouser"}],
                                   "unverified": ["@baruser"]}}
            usrmgr_mock.return_value.config = config
            AdminCommands._AdminCommands__get_users(  # pylint: disable=no-member, protected-access
                bot, update)
        self.assertTrue(bot.sendMessage.called)

    def test_adduser_no_args(self):
        """
            Test adduser command if the wrong number of args is passed
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        AdminCommands._AdminCommands__add_user(  # pylint: disable=no-member, protected-access
            bot, update, [])
        bot.sendMessage.assert_called_with(
            chat_id=1, text="Usage: adduser <user> <group>")

    def test_adduser_usr_already_in_grp(self):
        """
            Test adduser command if user is already in group
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            usrmgr_mock.return_value.add_user.return_value = False
            AdminCommands._AdminCommands__add_user(  # pylint: disable=no-member, protected-access
                bot, update, ["@foouser", "foogroup"])
            bot.sendMessage.assert_called_with(
                chat_id=1,
                text="The user '@foouser' is already in the group 'foogroup'!")

    def test_adduser(self):
        """
            Test adduser command
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            usrmgr_mock.return_value.add_user.return_value = True
            AdminCommands._AdminCommands__add_user(  # pylint: disable=no-member, protected-access
                bot, update, ["@foouser", "foogroup"])
        bot.sendMessage.assert_called_with(
            chat_id=1,
            text="Added user '@foouser' to the group 'foogroup'.")

    def test_rmuser_no_args(self):
        """
            Test rmuser command if the wrong number of args is passed
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        AdminCommands._AdminCommands__rm_user(  # pylint: disable=no-member, protected-access
            bot, update, [])

        bot.sendMessage.assert_called_with(chat_id=1,
                                           text="Usage: rmuser <user> <group>")

    def test_rmuser_usr_not_in_grp(self):
        """
            Test rmuser command if user is not in group
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            usrmgr_mock.return_value.rm_user.return_value = False
            AdminCommands._AdminCommands__rm_user(  # pylint: disable=no-member, protected-access
                bot, update, ["@foouser", "foogroup"])
            bot.sendMessage.assert_called_with(
                chat_id=1,
                text="The user '@foouser' could not"\
                " be found in the group 'foogroup'!")

    def test_rmuser(self):
        """
            Test rmuser command
        """
        bot = Mock(spec=Bot)
        update = self.__get_dummy_update()

        with patch("ownbot.admincommands.UserManager") as usrmgr_mock:
            usrmgr_mock.return_value.rm_user.return_value = True
            AdminCommands._AdminCommands__rm_user(  # pylint: disable=no-member, protected-access
                bot, update, ["@foouser", "foogroup"])
            bot.sendMessage.assert_called_with(
                chat_id=1,
                text="Removed user '@foouser' from the group 'foogroup'.")
