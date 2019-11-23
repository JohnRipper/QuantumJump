import json
import re as regex
from aiohttp import ClientSession

from lib.exceptions import HttpStatus
from lib.objects import SelfBot


class UrlBuilder:
    LOGIN = "https://jumpin.chat/login"
    LOGOUT = "https://jumpin.chat/logout"
    SESSION = "https://jumpin.chat/api/user/session"
    _sio = "https://jumpin.chat/socket.io/?token={token}&EIO=3&transport=polling&t=Muk-CB0"
    _wss = "wss://jumpin.chat/socket.io/?token={token}&EIO=3&transport=websocket&sid={io}"

    def sio(self, token):
        return self._sio.format(token=token)

    def wss(self, token, io):
        return self._wss.format(token=token, io=io)


class Api:
    def __init__(self):
        self.client = ClientSession()
        self._session = None
        self.urls = UrlBuilder()

    async def post(self, url: str = None, data: dict = None):
        result = await self.client.post(url=url, data=data)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    async def get(self, url: str = None):
        result = await self.client.get(url=url)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    @property
    def session(self):
        if self._session:
            return self._session
        # todo return a guest session  by default if the session object is None.

    async def logout(self):
        await self.post(url=self.urls.LOGOUT)

    async def get_login_session(self):
        resp = await self.post(self.urls.SESSION)
        self._session = SelfBot(**json.loads(await resp.text()))
        return self._session

    async def get_sio_sid(self):
        r = await self.get(self.urls.sio(token=self._session.token))
        pattern = r"(?<=\"sid\":\")(.*?)(?=\",)"
        io = regex.search(pattern, await r.text())
        return io[0]

    async def print_cookies(self):
        print(self.client.cookie_jar.__dict__)

    async def get_wss(self):
        await self.get_login_session()
        return self.urls.wss(token=self._session.token, io=await self.get_sio_sid())

    async def login(self, username: str, password: str):
        await self.post(url=self.urls.LOGIN,
                        data={"action": "login",
                              "username": username,
                              "password": password})
        # todo check if successful






