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
    CONFIG_DIR_PATH = os.path.join(os.path.expanduser("~"), ".ownbot")
    USERS_CONF_PATH = os.path.join(
        os.path.expanduser("~"), ".ownbot", "users.yml")

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
            config_file.write(yaml.dump(self.__config))

    def __clean_config(self, group=None):
        """Removes empty values of keys in config.

            Removes all keys from the config which have
            empty lists or dicts as values.

            Args:
                group (Optional[str]): The group key to clean.
        """
        verified_present = self.VERIFIED in self.__config[group]
        unverified_present = self.UNVERIFIED in self.__config[group]

        if group:
            if unverified_present and not self.__config[group][
                    self.UNVERIFIED]:
                self.__config[group].pop(self.UNVERIFIED, None)

            if verified_present and not self.__config[group][self.VERIFIED]:
                self.__config[group].pop(self.VERIFIED, None)

        if not self.__config[group]:
            self.__config.pop(group, None)

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

    def userid_is_verified_in_group(self, group, user_id):
        """
            Checks if a user id is in a group and
            verified in that group.

            Args:
                group (str): The group to look for the user.
                user_id (str): The user's unique id.

            Returns:
                bool: True if the user was found in the
                    given group as verified, otherwise False.
        """
        self.__load_config()

        user_in_group = [
            usr for usr in self.__config.get(group, {}).get(self.VERIFIED, [])
            if usr.get("id") == user_id
        ]

        return bool(user_in_group)

    def username_is_verified_in_group(self, group, username):
        """
            Checks if a username is in a group and
            verified in that group.

            Args:
                group (str): The group to look for the user.
                username (str): The user's name.

            Returns:
                bool: True if the user was found in the
                    given group as verified, otherwise False.
        """
        self.__load_config()

        user_in_group = [
            usr for usr in self.__config.get(group, {}).get(self.VERIFIED, [])
            if usr.get("username") == username
        ]

        return bool(user_in_group)

    def user_is_unverified_in_group(self, group, username):
        """
            Checks if a user is in a group and
            verified in that group.

            Args:
                group (str): The group to look for the user.
                username (str): The user's name.

            Returns:
                bool: True if the user was found in the
                    given group as verified, otherwise False.
        """
        self.__load_config()
        unverified_users = self.__config.get(group, {}).get(self.UNVERIFIED,
                                                            [])
        return username in unverified_users

    def user_is_in_group(self, group, user_id=None, username=None):
        """
            Checks if a user is in a specific
            group.

            Args:
                group (str): The group to look for the user.
                user_id (Optional[str]): The user's unique id.
                username (Optional[str]): The user's name.

            Note:
                If the user_id is passed, only the verified users
                will be checked.
                If the username is passed instead, the verified and the
                unverified users will be checked.

            Returns:
                bool: True if the user id was found in
                    the given group, otherwise False.
        """
        self.__load_config()

        if group not in self.__config or (user_id is None and
                                          username is None):
            return False

        if user_id:
            return self.userid_is_verified_in_group(group, user_id)

        is_in_verified = self.username_is_verified_in_group(group, username)
        is_in_unverified = self.user_is_unverified_in_group(group, username)

        return is_in_verified or is_in_unverified

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

        self.__config[group][self.VERIFIED].append({
            "id": user_id,
            "username": username
        })
        self.__clean_config(group=group)
        self.__save_config()
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
                Adding a user and adding a user to a group
                is the same.

                If the optional user_id is passed, the user
                automatically gets added to the verfied users
                of the group.

            Returns:
                bool: True if the user was added to the
                    group, otherwise False.
        """
        self.__load_config()

        # Check if user is already in this group
        if self.user_is_in_group(group, username=username):
            return False

        if not self.__config.get(group, None):
            self.__config[group] = {}

        # Add the user to the verified users of the group
        # if the user_id was passed
        if user_id:
            if self.VERIFIED not in self.__config[group]:
                self.__config[group][self.VERIFIED] = []

            self.__config[group][self.VERIFIED].append({
                "id": user_id,
                "username": username
            })
            self.__save_config()
            return True

        if not self.UNVERIFIED in self.__config[group]:
            self.__config[group][self.UNVERIFIED] = []

        self.__config[group][self.UNVERIFIED].append(username)
        self.__save_config()
        return True

    def rm_user(self, username, group):
        """
            Removes a user from a group.

            Args:
                username (str): the user's name.
                group (str): The user's group.

            Returns:
                bool: True if user was removed, otherwise False.
        """
        self.__load_config()

        if not self.username_is_verified_in_group(group, username)\
           and not self.user_is_unverified_in_group(group, username):
            return False

        if self.username_is_verified_in_group(group, username):
            self.__config[group][self.VERIFIED][:] = [
                usr for usr in self.__config.get(group).get(self.VERIFIED)
                if usr.get("username") != username
            ]
            self.__save_config()

        if self.user_is_unverified_in_group(group, username):
            self.__config[group][self.UNVERIFIED].remove(username)

        self.__clean_config(group=group)
        self.__save_config()

        return True

    def group_is_empty(self, group):
        """Checks if given group is empty.

            Checks if the passed group has any users
            or is completely empty.

            Args:
                group (str): The group to be checked.

            Returns:
                bool: True if the group is emtpy, otherwise False.
        """
        self.__load_config()
        self.__config.get(group)
        return not bool(self.__config.get(group))

    def get_users(self, group):
        """Get all users from given group.

            Returns a list of all verified users
            from the given group.

            Args:
                group (str): The group.

            Returns:
                list: Verified users from given group.
        """
        self.__load_config()
        group = self.__config.get(group, {})
        return group.get(self.VERIFIED, [])
