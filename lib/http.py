# -*- coding: utf-8 -*-
#
# Copyright 2019, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 2/8/20
# This file is part of QuantumJump.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import json
import re as regex

from aiohttp import ClientSession

from lib.exceptions import HttpStatus
from lib.logging import QuantumLogger
from lib.objects import Session
from aiohttp_socks import SocksConnector


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
        self.log = QuantumLogger("Http")
        self.connector = SocksConnector.from_url(
            "socks5://127.0.0.1:9050")

    async def close(self):
        await self.session.close()
        await self.connector.close()

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self.connector = SocksConnector.from_url(
                "socks5://127.0.0.1:9050")
            self._session = ClientSession()
        # Todo check if session is valid or reset
        if self._session.closed:
            self.connector = SocksConnector.from_url(
                "socks5://127.0.0.1:9050")
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
        result = self.urls.wss(token=self.login_data.token,
                             io=await self.get_sio_sid())
        await self.print_cookies()

        return result

    async def login(self, username: str, password: str) -> bool:
        result = await self.post(url=self.urls.LOGIN,
                                 data={
                                     "action": "login",
                                     "username": username,
                                     "password": password
                                 })
        if "connect.sid" in result.cookies:
            return True

    async def getroominfo(self, room: str) -> dict:
        action = await self.get(url=self.urls.room(room=room))
        return await action.json()
