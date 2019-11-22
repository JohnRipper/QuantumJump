class Error(Exception):
    def __init__(self, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {message}")
        else:
            print(self.__class__.__name__)


class InvalidLogin(Error):
    pass


class HttpStatus(Error):
    def __init__(self, message: str = None, code: int = 0):
        if message:
            print(f"{self.__class__.__name__}: {message}")
        else:
            print(self.__class__.__name__)
