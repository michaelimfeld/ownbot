# ownbot

[![Build Status](https://travis-ci.org/michaelimfeld/ownbot.svg?branch=master)](https://travis-ci.org/michaelimfeld/ownbot)
[![Coverage Status](https://coveralls.io/repos/github/michaelimfeld/ownbot/badge.svg?branch=master)](https://coveralls.io/github/michaelimfeld/ownbot?branch=master)
[![PyPI version](https://badge.fury.io/py/ownbot.svg)](https://badge.fury.io/py/ownbot)

> Easy to use python module to create private telegram bots using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

Ownbot provides some cool decorators to protect your command handler functions from unauthorized users!


## Install
```shell
pip install ownbot
```

## Get Started

  - The `assign_first_to` decorator adds the first user who invokes the handler method to the specified group.
  - The second decorator `requires_usergroup` lets you define which usergroups will have permission to access the handler command.

```python
from ownbot.auth import requires_usergroup, assign_first_to
(...)

@assign_first_to("admin")
@requires_usergroup("user")
def start_handler(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello World")
```

Obviously if a user is in the `admin` group he has also access to functions which are protected with the `@requires_usergroup("user")` decorator. If a group passed to this decorator does not already exist, it will be automatically created.

## How It Works
Ownbot saves new users added by Telegram username as unverified users. On first contact, when the user sends his first message to the bot, ownbot will store the user with his unique id as a verified user. A verified user will from now on always have access to his group even if he changes his username. The authorization checks are done only on the unique Telegram `user_id`! Sounds good right?

## Storage
For user/group storage ownbot uses a simple yaml file, which can be found in `$HOMEDIR/.ownbot/users.yml`. This file can be edited manually, but it is recommended to use the `AdminCommands` to add or remove users from groups.

## Admin Commands

The admin commands can be enabled by simply instantiating the `AdminCommands`
class and passing over the bot's dispatcher.

```python
from ownbot.admincommands import AdminCommands
(...)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
AdminCommands(dispatcher)
```

If the admin commands are enabled, a user who is in the `admin` group is able to perform the following actions:

| Command    | Arguments  | Description                           |
|------------|------------|---------------------------------------|
| /adminhelp | -          | Shows a list of available commands.   |
| /users     | -          | Shows a list of all registered users. |
| /adduser   | user group | Adds a user to a group.               |
| /rmuser    | user group | Removes a user from a group.          |
