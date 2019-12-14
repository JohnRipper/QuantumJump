import re
from enum import Enum

from lib.objects import Message, Role, User


def makeCommand(aliases: [], description: str, role: Role = None, **attrs):
    def wrap(f):
        f.__command__ = True
        f.__command_name__ = aliases
        f.__description__ = description
        if role:
            f.__role__ = role
            f.__restricted__ = True
        else:
            f.__restricted__ = False
        return f
    return wrap


command_pattern = r"{}(\w+)(\\b.*)"


class Command:
    def __init__(self, prefix: str, data: Message):
        self.prefix = prefix
        self.data = data
        self.name = None
        self.message = data.message

        parsed = re.search(
            command_pattern.format(self.prefix),
            data.message)
        if parsed is not None:
            self.name, self.message = parsed.groups()
            self.message = self.message.lstrip()



