# -*- coding: utf-8 -*-
"""
    Provides a unit test class for the ownbot.auth module.
"""
from datetime import datetime
from unittest import TestCase
from mock import patch, Mock
from imp import reload

from telegram import Bot, Update, User, Chat, Message

import ownbot.auth
# Is needed otherwise the decorators would be patched
# by the test_admincommands' dummy decorator.
reload(ownbot.auth)


class TestAuth(TestCase):  # pylint: disable=too-many-public-methods
    """
        Provides unit tests for the ownbot.auth module.
    """

    @staticmethod
    def __get_dummy_update():
        """Returns a dummy update instance"""
        user = User(1337, "@foouser")
        chat = Chat(1, None)
        message = Message(1, user, datetime.now(), chat)
        return Update(1, message=message)

    def test_requires_usergroup_no_acc(self):
        """
            Test requires usergroup decorator if the user has no access
        """
        with patch("ownbot.auth.User") as user_mock:
            user_mock.return_value.has_access.return_value = False

            @ownbot.auth.requires_usergroup("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)
                return True

            bot_mock = Mock(spec=Bot)
            update = self.__get_dummy_update()
            called = my_command_handler(bot_mock, update)

            self.assertIsNone(called)

    def test_requires_usergroup_acc(self):
        """
            Test requires usergroup decorator if the user has access
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:
            user_mock = user_mock.return_value
            user_mock.has_acces.return_value = True

            @ownbot.auth.requires_usergroup("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)
                return True

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            called = my_command_handler(bot_mock, update_mock)

            self.assertTrue(called)

    def test_requires_usergroup_self(self):
        """
            Test requires usergroup decorator with self as first argument.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock:
            user_mock = user_mock.return_value
            user_mock.has_acces.return_value = True

            @ownbot.auth.requires_usergroup("foo")
            def my_command_handler(self, bot, update):
                """Dummy command handler"""
                print(self, bot, update)
                return True

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            called = my_command_handler(None, bot_mock, update_mock)

            self.assertTrue(called)

    def test_assign_first_to(self):
        """
            Test assign first to decorator.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock,\
                patch("ownbot.auth.UserManager") as usrmgr_mock:

            user_mock = user_mock.return_value
            usrmgr_mock.return_value.group_is_empty.return_value = True

            @ownbot.auth.assign_first_to("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(bot_mock, update_mock)

            self.assertTrue(usrmgr_mock.return_value.group_is_empty.called)
            self.assertTrue(user_mock.save.called)

    def test_assign_first_to_not_first(self):
        """
            Test assign first to decorator if the users is not first.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock,\
                patch("ownbot.auth.UserManager") as usrmgr_mock:

            user_mock = user_mock.return_value
            usrmgr_mock.return_value.group_is_empty.return_value = False

            @ownbot.auth.assign_first_to("foo")
            def my_command_handler(bot, update):
                """Dummy command handler"""
                print(bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(bot_mock, update_mock)

            self.assertTrue(usrmgr_mock.return_value.group_is_empty.called)
            self.assertFalse(user_mock.save.called)

    def test_assign_first_to_with_self(self):
        """
            Test assign first to decorator with self as first argument.
        """
        with patch("ownbot.auth.User") as user_mock,\
                patch("test_auth.Update") as update_mock,\
                patch("ownbot.auth.UserManager") as usrmgr_mock:

            user_mock = user_mock.return_value
            usrmgr_mock.return_value.group_is_empty.return_value = True

            @ownbot.auth.assign_first_to("foo")
            def my_command_handler(self, bot, update):
                """Dummy command handler"""
                print(self, bot, update)

            bot_mock = Mock(spec=Bot)
            update_mock = Update(1337)
            my_command_handler(None, bot_mock, update_mock)

            self.assertTrue(usrmgr_mock.return_value.group_is_empty.called)
            self.assertTrue(user_mock.save.called)
