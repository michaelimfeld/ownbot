# -*- coding: utf-8 -*-
"""
    Provides the ownbot User class.
"""
from ownbot.usermanager import UserManager


class User(object):
    """Represents a telegram user.

        Args:
            name (str): The user's unique telegram username.
            user_id (str): The user's unique telegram id.
            group (Optional[str]): The user's group.
    """

    def __init__(self, name, user_id, group=None):
        self.__name = name
        self.__id = user_id
        self.__group = group
        self.__usermanager = UserManager()

    def save(self):
        """Saves the user's data.

            Saves the users's data to the configuration
            file.

            Returns:
                bool: True if the user was saved, otherwise False
        """
        if not self.__group:
            return False

        self.__usermanager.add_user(self.__name,
                                    self.__group,
                                    user_id=self.__id)
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
        is_in_group = self.__usermanager.user_is_in_group(group,
                                                          user_id=self.__id)
        is_admin = self.__usermanager.user_is_in_group("admin",
                                                       user_id=self.__id)

        if is_in_group or is_admin:
            self.save()
            return True

        is_admin = self.__usermanager.verify_user(self.__id, self.__name,
                                                  "admin")
        is_in_group = self.__usermanager.verify_user(self.__id, self.__name,
                                                     group)

        return is_admin or is_in_group
