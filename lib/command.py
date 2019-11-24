class Command:
    @classmethod
    def makeCommand(cls, fun):
        def wrapper(self, *args, **kwargs):
            self.write(*args, **kwargs)
            return fun(self, *args, **kwargs)
        return wrapper

    def write(self, *args, **kwargs):
        # do shit.
        print(args, kwargs)

