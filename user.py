# -*- coding: utf-8 -*-
"""
    Provides the user class.
"""
import os
import yaml


class User(object):
    """Represents a telegram user.

        Args:
            user_id (str): The user's unique id.
            first_name (Optional[str]): The user's fist_name.
            last_name (Optional[str]): The user's last_name.
            group (Optional[str]): The user's group.
    """

    CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".users.yml")

    def __init__(self, user_id, first_name=None, last_name=None, group=None):
        self.__id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__group = group
        self.__config = None

    def __load_config(self):
        """Loads the configuration file.

            Loads all usergroups and users as a dict from
            the configuration file into the config attribute.
        """
        if not os.path.exists(self.CONFIG_PATH):
            self.__config = {}
            return

        with open(self.CONFIG_PATH, "r") as config_file:
            config = yaml.load(config_file)
            if not config:
                self.__config = {}
                return

            self.__config = config

    def __save_config(self):
        """Saves the configuration.

            Saves the config attribute to the configuration
            file.
        """
        with open(self.CONFIG_PATH, "w+") as config_file:
            config_file.write(
                yaml.dump(self.__config)
            )

    def save(self):
        """Saves the user's data.

            Saves the users's data to the configuration
            file.

            Returns:
                bool: True if the user was saved, otherwise False
        """
        self.__load_config()

        if self.__fist_name and self.__last_name and self.__group:
            return False

        if not self.__config.get(self.__group):
            self.__config[self.__group] = {}

        if not self.__config[self.__group].get(self.__id):
            self.__config[self.__group][self.__id] = {}

        self.__config[self.__group][self.__id]["first_name"] = self.__first_name
        self.__config[self.__group][self.__id]["last_name"] = self.__last_name
        self.__save_config()
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
        self.__load_config()
        return self.__config.get(name, {})
