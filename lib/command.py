import re

from lib.objects import Message


def makeCommand(name: str, description: str, **attrs):
    def wrap(f):
        f.__command__ = True
        f.__command_name__ = name
        f.__description__ = description
        return f
    return wrap


command_pattern = "{}(\w+)(\\b.*)"


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
