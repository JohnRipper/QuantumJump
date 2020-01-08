import json
import re as regex

from aiohttp import ClientSession

from lib.exceptions import HttpStatus
from lib.objects import Session


class UrlBuilder:
    LOGIN = "https://jumpin.chat/login"
    LOGOUT = "https://jumpin.chat/logout"
    SESSION = "https://jumpin.chat/api/user/session"
    _room = "https://jumpin.chat/api/rooms/{room}"
    _sio = "https://jumpin.chat/socket.io/?token={token}&EIO=3&transport=polling&t=Muk-CB0"
    _wss = "wss://jumpin.chat/socket.io/?token={token}&EIO=3&transport=websocket&sid={io}"

    def sio(self, token):
        return self._sio.format(token=token)

    def wss(self, token, io):
        return self._wss.format(token=token, io=io)

    def room(self, room):
        return self._room.format(room=room)


class Http:
    def __init__(self):
        self._session = None
        self.login_data = None
        self.urls = UrlBuilder()

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()
        # Todo check if session is valid or reset
        if self._session.closed:
            self._session = ClientSession()
        return self._session

    # wrapped methods
    async def post(self, url: str = None, data: dict = None):
        result = await self.session.post(url=url, data=data)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    async def get(self, url: str = None):
        result = await self.session.get(url=url)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    # jumpin api stuff.
    async def logout(self):
        await self.post(url=self.urls.LOGOUT)

    async def get_login_session(self) -> Session:
        resp = await self.post(self.urls.SESSION)
        data = json.loads(await resp.text())
        if data.get("user", False):
            print("Logged in successfully.")
        else:
            # guest does not have a user object associated with the token.
            print("Logged  not successful. Attempting guest mode.")
        self.login_data = Session(**data)

        return self.login_data

    async def get_sio_sid(self):
        r = await self.get(self.urls.sio(token=self.login_data.token))
        pattern = r"(?<=\"sid\":\")(.*?)(?=\",)"
        io = regex.search(pattern, await r.text())
        return io[0]

    async def print_cookies(self):
        print(self.session.cookie_jar.__dict__)

    async def get_wss(self):
        await self.get_login_session()
        return self.urls.wss(token=self.login_data.token,
                             io=await self.get_sio_sid())

    async def login(self, username: str, password: str):
        await self.post(url=self.urls.LOGIN,
                        data={
                            "action": "login",
                            "username": username,
                            "password": password
                        })
        # todo check if successful

    async def getroominfo(self, room: str) -> dict:
        action = await self.get(url=self.urls.room(room=room))
        return await action.json()
