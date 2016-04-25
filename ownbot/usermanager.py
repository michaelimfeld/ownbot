# -*- coding: utf-8 -*-
"""
    Provides the ownbot UserManager class.
"""
import os
import yaml


class UserManager(object):  # pylint: disable=too-few-public-methods
    """
        Provides functions to save and load
        ownbot users.
    """
    CONFIG_DIR_PATH = os.path.join(
        os.path.expanduser("~"),
        ".ownbot"
    )
    USERS_CONF_PATH = os.path.join(
        os.path.expanduser("~"),
        ".ownbot",
        "users.yml"
    )

    UNVERIFIED = "unverified"
    VERIFIED = "users"

    def __init__(self):
        self.__config = None

        # create config dir if it doesn't already exist
        if not os.path.exists(self.CONFIG_DIR_PATH):
            os.mkdir(self.CONFIG_DIR_PATH)

    def __load_config(self):
        """Loads the configuration file.

            Loads all usergroups and users as a dict from
            the configuration file into the config attribute.
        """
        if not os.path.exists(self.USERS_CONF_PATH):
            self.__config = {}
            return

        with open(self.USERS_CONF_PATH, "r") as config_file:
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
        with open(self.USERS_CONF_PATH, "w+") as config_file:
            config_file.write(
                yaml.dump(self.__config)
            )

    @property
    def config(self):
        """
            Returns the user configuration.
        """
        self.__load_config()
        return self.__config

    @config.setter
    def config(self, config):
        """
            Sets the user configuration.
        """
        self.__config = config
        self.__save_config()

    def is_in_group(self, user_id, group):
        """
            Checks if a user is in a specific
            group.

            Args:
                user_id (str): The user's unique id.
                group (str): The group to look for the user.

            Returns:
                bool: True if the user id was found in
                    the given group, otherwise False.
        """
        self.__load_config()

        if group not in self.__config or \
           self.VERIFIED not in self.__config[group]:
            return False

        usr_in_group = self.__config[group][self.VERIFIED][:] = [
            usr for usr in self.__config[group][self.VERIFIED]
            if usr.get("id") == user_id
        ]
        return bool(usr_in_group)

    def verify_user(self, user_id, username, group):
        """Verifies a user.

            Checks if a username is in the
            unverified list and if so, adds him
            to the verified users.

            Args:
                user_id (str): The user's unique id.
                username (str): The user's name.
                group (str): The group's name.
        """
        self.__load_config()

        if group not in self.__config \
           or self.UNVERIFIED not in self.__config[group] \
           or username not in self.__config[group][self.UNVERIFIED]:
            return False

        self.__config[group][self.UNVERIFIED].remove(username)

        if not self.VERIFIED in self.__config[group]:
            self.__config[group][self.VERIFIED] = []

        self.__config[group][self.VERIFIED].append(
            {
                "id": user_id,
                "username": username
            }
        )
        return True


    def add_user(self, username, group, user_id=None):
        """
            Adds a user to the unverified users in a
            group.

            Args:
                username (str): The user's name.
                group (str): The user's group.
                user_id (Optional[str]): The user's id.

            Note:
                Adding a user or adding a user to a group
                is the same.

                If the optional user_id is passed, the user
                automatically gets added to the verfied users
                of the group.

            Returns:
                bool: True if the user was added to the
                    group, otherwise False.
        """
        self.__load_config()
        if not group in self.__config:
            self.__config[group] = {}

        if user_id:
            if self.VERIFIED not in self.__config[group]:
                self.__config[group][self.VERIFIED] = []

            self.__config[group][self.VERIFIED].append(
                {
                    "id": user_id,
                    "username": username
                }
            )
            self.__save_config()
            return True

        if not self.UNVERIFIED in self.__config[group]:
            self.__config[group][self.UNVERIFIED] = []

        self.__config[group][self.UNVERIFIED].append(username)
        self.__save_config()
        return True

