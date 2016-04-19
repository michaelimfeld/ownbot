# -*- coding: utf-8 -*-
"""
    Provides the ownbot User class.
"""
from ownbot.usermanager import UserManager


class User(object):
    """Represents a telegram user.

        Args:
            user_id (str): The user's unique id.
            first_name (Optional[str]): The user's fist_name.
            last_name (Optional[str]): The user's last_name.
            group (Optional[str]): The user's group.
    """

    def __init__(self, user_id, first_name=None, last_name=None, group=None):
        self.__id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__group = group
        self.__usermanager = UserManager()

    def save(self):
        """Saves the user's data.

            Saves the users's data to the configuration
            file.

            Returns:
                bool: True if the user was saved, otherwise False
        """
        config = self.__usermanager.users

        if self.__fist_name and self.__last_name and self.__group:
            return False

        if not config.get(self.__group):
            config[self.__group] = {}

        user_config = {}
        user_config["first_name"] = self.__first_name
        user_config["last_name"] = self.__last_name
        config[self.__group][self.__id] = user_config
        self.__usermanager.users = config
        return True

    def has_access(self, group):
        """Checks if the user is in given group.

            Returns True if given user has access rights
            to the given group.

            Args:
                group (str): The group's name.

            Returns:
                bool: True if user is in the given group, otherwise False.
        """
        if not getattr(self, group) and not getattr(self, "admins"):
            return False

        is_in_group = self.__id in getattr(self, group)
        is_admin = self.__id in getattr(self, "admins")
        return is_in_group or is_admin

    def group_empty(self, group):
        """Checks if the given group contains any users.

            Checks if there's at least one user, which is member of the
            given group.

            Returns:
                bool: True if at least one user is in the given group.

        """
        if not getattr(self, group):
            return True
        return False

    def __getattr__(self, name):
        """Returns a configuration attribute.

            Returns the configuration attribute value from
            the given key.

            Args:
                name (str): The attribute's name.

            Returns:
                str: The attribute's value if it exists,
                    otherwise an empty str.

        """
        return self.__usermanager.users.get(name, {})
