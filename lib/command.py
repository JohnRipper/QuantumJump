import re

from lib.objects import Message


def makeCommand(name: str, description: str, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f.__command__ = True
        f.__command_name__ = name
        f.description = description
        return f

    return wrap


command_pattern = "{}(\w+)(\\b.*)"


class Command:
    def __init__(self, prefix: str, data: Message):
        self.prefix = prefix
        self.name, self.message = re.search(
            command_pattern.format(self.prefix),
            data.message).groups()
        self.message = self.message.lstrip()
