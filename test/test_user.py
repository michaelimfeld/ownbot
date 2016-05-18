# -*- coding: utf-8 -*-
"""
    Provides a unit test class for the ownbot.user module.
"""
from unittest import TestCase
from mock import patch

from ownbot.user import User


class TestUser(TestCase):  # pylint: disable=too-many-public-methods
    """
        Provides unit tests for the ownbot.user module.
    """

    @staticmethod
    def __get_test_instance(username, user_id, group=None):
        """Returns a patched User instance"""
        with patch("ownbot.user.UserManager") as usrmgr_mock:
            return User(username, user_id, group=group), usrmgr_mock

    def test_save_no_group(self):
        """
            Test save user if user has no group
        """
        user, _ = self.__get_test_instance("@foouser", 1337)
        self.assertFalse(user.save())

    def test_save(self):
        """
            Test save user if user has group
        """
        user, usrmgr_mock = self.__get_test_instance(
            "@foouser", 1337, group="foogroup")
        usrmgr_mock.return_value.add_user.return_value = True
        self.assertTrue(user.save())
        self.assertTrue(usrmgr_mock.return_value.add_user.called)

    def test_has_access_is_in_group(self):
        """
            Test has access if passed user is in group
        """
        user, usrmgr_mock = self.__get_test_instance(
            "@foouser", 1337, group="foogroup")
        usrmgr_mock.return_value.user_is_in_group.return_value = True
        with patch.object(user, "save"):
            user.has_access("foogroup")

    def test_has_access_is_not_in_group(self):
        """
            Test has access if passed user is not in group
        """
        user, usrmgr_mock = self.__get_test_instance(
            "@foouser", 1337, group="bargroup")
        usrmgr_mock.return_value.user_is_in_group.return_value = False
        usrmgr_mock.return_value.verify_user.return_value = False
        with patch.object(user, "save"):
            user.has_access("foogroup")
