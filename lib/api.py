import json
import re as regex
from aiohttp import ClientSession

from lib.exceptions import HttpStatus
from lib.objects import SelfBot


class Api:
    def __init__(self):
        self.client = ClientSession()
        self._session = None

    async def post(self, url: str = None, data: dict = None):
        result = await self.client.post(url=url, data=data)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    async def get(self, url: str = None):
        result = await self.client.post(url=url)
        if result.status != 200:
            raise HttpStatus(code=result.status)
        else:
            return result

    async def session(self):
        if self._session:
            # todo get guest session by default.
            return None
        return self._session

    async def login(self, username: str, password: str):
        await self.post(url='https://jumpin.chat/login',
                        data={"action": "login",
                              "username": username,
                              "password": password})
        # todo check if successful or not. consider logging in as guest
        resp = await self.post('https://jumpin.chat/api/user/session')
        self.session = SelfBot(**json.loads(await resp.text()))
        r = await self.get(f"https://jumpin.chat/socket.io/?token={self.session.token}&EIO=3&transport=polling&t=Muk-CB0")
        pattern = r"(?<=\"sid\":\")(.*?)(?=\",)"
        io = regex.search(pattern, await r.text())
        # # hmm cookies instead?
        print(self.client.cookie_jar.__dict__)
        # for cookie  in self.session.cookie_jar:
        #     print(cookie)
        url = f"wss://jumpin.chat/socket.io/?token={self.session.token}&EIO=3&transport=websocket&sid={io[0]}"
        return url
