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
    def users(self):
        """
            Returns the user configuration.
        """
        self.__load_config()
        return self.__config

    @users.setter
    def users(self, config):
        """
            Sets the user configuration.
        """
        self.__config = config
        self.__save_config()
