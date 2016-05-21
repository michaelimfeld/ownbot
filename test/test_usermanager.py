# -*- coding: utf-8 -*-
"""
    Provides a unit test class for the ownbot.usermanager module.
"""
import io

from unittest import TestCase
from mock import patch

from ownbot.usermanager import UserManager


class TestUserManager(TestCase):  # pylint: disable=too-many-public-methods
    """
        Provides unit tests for the ownbot.usermanager module.
    """

    @staticmethod
    def __get_dummy_object():
        """Returns a dummy usermanager object."""
        with patch("os.mkdir"):
            return UserManager()

    @staticmethod
    def __set_config(usrmgr, config):
        """Sets the config attribute of the passed usermanager instance"""
        with patch.object(usrmgr, "_UserManager__save_config"):
            usrmgr.config = config

    def test_init(self):
        """
            Test the init function of the usermanager
        """
        with patch("os.path.exists", return_value=False),\
                patch("os.mkdir") as mkdir_mock:
            mkdir_mock.return_value = True
            UserManager()
            self.assertTrue(mkdir_mock.called)

    def test_get_set_config(self):
        """
            Test getting and setting the config attribute
        """
        usrmgr = self.__get_dummy_object()
        config = {"hello": {}, "world": {}}
        with patch.object(usrmgr, "_UserManager__save_config"):
            usrmgr.config = config

        with patch.object(usrmgr, "_UserManager__load_config"):
            self.assertEqual(usrmgr.config, config)

    def test_load_config_no_file(self):
        """
            Test loading of the config attr if the config file does not exist
        """
        usrmgr = self.__get_dummy_object()
        with patch("os.path.exists", return_value=False):
            self.assertEqual(usrmgr.config, {})

    def test_load_config_empty_file(self):
        """
            Test loading of the config attr if the config file is empty
        """
        usrmgr = self.__get_dummy_object()
        with patch("os.path.exists", return_value=True),\
                patch("ownbot.usermanager.open") as open_mock:

            open_mock.return_value = io.BytesIO(b"")

            self.assertEqual(usrmgr.config, {})
            self.assertTrue(open_mock.called)

    def test_load_config(self):
        """
            Test loading of the config attribute
        """
        usrmgr = self.__get_dummy_object()
        with patch("os.path.exists", return_value=True),\
                patch("ownbot.usermanager.open") as open_mock:

            open_mock.return_value = io.BytesIO(b"""
foogroup:
  unverified:
    - '@foouser'""")

            expected_config = {"foogroup": {"unverified": ["@foouser"]}}

            self.assertEqual(usrmgr.config, expected_config)
            self.assertTrue(open_mock.called)

    def test_save_config(self):
        """
            Test save config
        """
        usrmgr = self.__get_dummy_object()
        with patch("ownbot.usermanager.open"):
            usrmgr.config = {}

    def test_userid_is_verified_grp(self):
        """
            Test user id is verified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337, "username": "@foo"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.userid_is_verified_in_group("foogroup", 1337)
            self.assertTrue(result)

    def test_userid_is_not_verified_grp(self):
        """
            Test user id is not verified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337, "username": "@foo"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.userid_is_verified_in_group("foogroup", 1234)
            self.assertFalse(result)

    def test_username_is_verified_grp(self):
        """
            Test username is verified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337, "username": "@foo"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.username_is_verified_in_group("foogroup", "@foo")
            self.assertTrue(result)

    def test_usernm_is_not_verified_grp(self):
        """
            Test username is not verified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337, "username": "@foo"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.username_is_verified_in_group("foogroup", "@bar")
            self.assertFalse(result)

    def test_user_is_unverified_grp(self):
        """
            Test username is unverified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foo"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.user_is_unverified_in_group("foogroup", "@foo")
            self.assertTrue(result)

    def test_user_is_not_unverified_grp(self):
        """
            Test username is not unverified in group check
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foo"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.user_is_unverified_in_group("foogroup", "@bar")
            self.assertFalse(result)

    def test_user_is_in_group_no_args(self):
        """
            Test user is in group check if needed args are not passed
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foo"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.user_is_in_group("foogroup")
            self.assertFalse(result)

    def test_user_is_in_group_username(self):
        """
            Test user is in group check if username is passed
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foo"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.user_is_in_group("foogroup", username="@foo")
            self.assertTrue(result)

    def test_user_is_in_group_userid(self):
        """
            Test user is in group check if userid is passed
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337, "username": "@foo"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.user_is_in_group("foogroup", user_id=1337)
            self.assertTrue(result)

    def test_verify_user_no_verify(self):
        """
            Test verify user if passed user is not unverified in group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": []}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"):
            result = usrmgr.verify_user(1337, "@foouser", "foogroup")
            self.assertFalse(result)

    def test_verify_user(self):
        """
            Test verify user if passed user is unverified in group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foouser"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.verify_user(1337, "@foouser", "foogroup")
            self.assertTrue(result)
            expected_config = {
                "foogroup": {"users": [{"id": 1337,
                                        "username": "@foouser"}]}
            }
            self.assertEqual(usrmgr.config, expected_config)

    def test_add_user_already_in_grp(self):
        """
            Test adduser if the user is already in the passed group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foouser"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.add_user("@foouser", "foogroup")
            self.assertFalse(result)

    def test_add_user_unverified(self):
        """
            Test adduser if only the user's name is passed
        """
        usrmgr = self.__get_dummy_object()
        self.__set_config(usrmgr, {})

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.add_user("@foouser", "foogroup")
            self.assertTrue(result)
            expected_config = {"foogroup": {"unverified": ["@foouser"]}}
            self.assertEqual(usrmgr.config, expected_config)

    def test_add_user_verified(self):
        """
            Test adduser if the username and the user_id is passed
        """
        usrmgr = self.__get_dummy_object()
        self.__set_config(usrmgr, {})

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.add_user("@foouser", "foogroup", user_id=1337)
            self.assertTrue(result)
            expected_config = {
                "foogroup": {"users": [{"id": 1337,
                                        "username": "@foouser"}]}
            }
            self.assertEqual(usrmgr.config, expected_config)

    def test_rm_user_not_in_grp(self):
        """
            Test rm user if the user is not in passed group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foouser"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.rm_user("@baruser", "foogroup")
            self.assertFalse(result)

    def test_rm_user_verified_in_grp(self):
        """
            Test rm user if the user is verified in passed group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337,
                                          "username": "@foouser"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.rm_user("@foouser", "foogroup")
            self.assertTrue(result)
            self.assertEquals(usrmgr.config, {})

    def test_rm_user_unverified_in_grp(self):
        """
            Test rm user if the user is unverified in passed group
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foouser"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.rm_user("@foouser", "foogroup")
            self.assertTrue(result)
            self.assertEquals(usrmgr.config, {})

    def test_group_is_empty(self):
        """
            Test group is empty check if group is not empty
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"unverified": ["@foouser"]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.group_is_empty("foogroup")
            self.assertFalse(result)

    def test_get_users(self):
        """
            Test get users
        """
        usrmgr = self.__get_dummy_object()
        config = {"foogroup": {"users": [{"id": 1337,
                                          "username": "@foouser"}]}}
        self.__set_config(usrmgr, config)

        with patch.object(usrmgr, "_UserManager__load_config"),\
                patch.object(usrmgr, "_UserManager__save_config"):
            result = usrmgr.get_users("foogroup")
            self.assertEqual(result, [{"id": 1337, "username": "@foouser"}])
