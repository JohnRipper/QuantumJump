from lib.objects import  Message


def makeCommand(name: str, description: str, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f.__command__ = True
        f.__command_name__ = name
        f.description = description
        return f
    return wrap


class Command:
    def __init__(self, prefix: str, data: Message):
        self.prefix = prefix

        # requires a trailing space to prevent split from breaking on empty message field.
        self.name, self.message = f'{data.message}{" "}'.split(' ', 1)
        # clean up the trailing spaces.
        self.message = self.message.strip()
        self.name = self.name[len(prefix):]

