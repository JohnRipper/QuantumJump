class Error(Exception):
    def __init__(self, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {message}")
        else:
            print(self.__class__.__name__)


class InvalidLogin(Error):
    pass


class HttpStatus(Exception):
    def __init__(self, code: int, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {code}:{message}")
        else:
            print(f"{self.__class__.__name__}: {code}")
