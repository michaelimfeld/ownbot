# ownbot

[![Build Status](https://travis-ci.org/michaelimfeld/ownbot.svg?branch=master)](https://travis-ci.org/michaelimfeld/ownbot)

> Easy to use python module to create private telegram bots.

## Install

```shell
git clone https://github.com/michaelimfeld/ownbot.git
pip install .
```

## Usage

Ownbot provides some cool decorators to protect your command handler functions from unauthorized users.
At the moment there are two decorators:

```python
from ownbot.auth import requires_usergroup, assign_first_to

# The first client who sends the '/start' command will be added
# to the admin group.
@assign_first_to("admin")
# If a user wants to execute the '/start' command he has to be
# a member of the 'user' group. Otherwise the decorator will not
# execute the handler function.
@requires_usergroup("user")
def start_handler(bot, update):
    """Handles the command '/start'.
        Sends a Hello World message to the client.
    """
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello World")
```

So that means only the first user who sends the '/start' command has access to that handler function.
To add users to groups you can edit the users file in ~/.ownbot/users.yml. It is planned to add admin commands, which should allow admins to manage users directly by talking to the bot.

```
admin:
  12345678: {first_name: !!python/unicode 'First', last_name: !!python/unicode 'User'}
newgroup:
  87654321: {first_name: 'Manually', last_name: 'Added'}
```

Obviously if a user is in the `admin` group he has also access to functions which are protected with the `@requires_usergroup("user")` decorator. If a group passed to this decorator does not already exist, it will be created.

Work in progress ...
