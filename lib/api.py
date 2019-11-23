import json
import re as regex
from aiohttp import ClientSession

from lib.exceptions import HttpStatus


class Session:
    connect_sid = ""


class Api:
    def __init__(self):
        self.session = ClientSession()

    async def Post(self):
        pass

    async def login(self, username: str, password: str):
        print(username)

        result = await self.session.post('https://jumpin.chat/login',
                                         data={
                                             "action": "login",
                                             "username": username,
                                             "password": password
                                         })
        if result.status != 200:
            raise HttpStatus(code=result.status)

        data = {}
        resp = await self.session.post('https://jumpin.chat/api/user/session')
        print(await resp.text())
        data = json.loads(await resp.text())

        await self.session.get('https://jumpin.chat/tech')
        r = await self.session.get(
            f"https://jumpin.chat/socket.io/?token={data.get('token')}&EIO=3&transport=polling&t=Muk-CB0"
        )

        print(await r.text())
        pattern = r"(?<=\"sid\":\")(.*?)(?=\",)"
        io = regex.search(pattern, await r.text())
        # # hmm cookies.
        # cookie: SimpleCookie
        # pattern = r"(?<=jic.activity=)(.*?)(?=;)"
        # print(self.session.cookie_jar.__dict__)
        # for cookie  in self.session.cookie_jar:
        #     print(cookie)
        #     if a := regex.search(pattern, cookie.__repr__()):
        #         token = a[1]

        url = f"wss://jumpin.chat/socket.io/?token={data.get('token')}&EIO=3&transport=websocket&sid={io[0]}"
        return url
