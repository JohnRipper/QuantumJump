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

import asyncio
import json
import time

import websockets

from lib.cog import CogManager
from lib.command import Command
from lib.http import Http
from lib.logging import QuantumLogger
from lib.objects import Message, User, UserList, BotState


class QuantumJumpBot:
    def __init__(self, settings):
        self._ws = None
        self.state = BotState(BotState.INITIALIZED)
        self.start_time = time.time()
        self.api = Http()
        self.cm = CogManager()
        self.settings = settings
        self.botconfig = self.settings.Bot
        self.ul = UserList()
        self.room = self.botconfig.roomname
        if self.settings.Bot.debug:
            self.log = QuantumLogger('QuantumJump', 10)
        else:
            self.log = QuantumLogger('QuantumJump', 19)

    async def wsend(self, data):
        if type(data) is list:
            data = f"42{json.dumps(data)}"
        elif type(data) is str:
            type_exemptions = ["2probe", "5", "2"]
            if not data.startswith("42") and data not in type_exemptions:
                data = f"42{data}"
        await self._ws.send(data)
        self.log.ws_send(data)

    async def run(self):
        enabled_modules = self.settings.Modules["enabled"]
        self.cm.load_all(enabled_modules, bot=self)
        await self.connect()

    async def disconnect(self):
        self.state = BotState.DISCONNECT
        await self._ws.close()

    async def connect(self):
        logged_in = await self.api.login(self.botconfig.username,
                                         self.botconfig.password)
        self.log.info(f"Logged in: {logged_in}")

        async with websockets.connect(
                uri=await self.api.get_wss(),
                timeout=600,
                origin="https://jumpin.chat"
        ) as self._ws:
            self.log.info("Connected to websocket.")
            self.state = BotState.RUNNING
            await self.wsend("2probe")
            async for message in self._ws:
                await self._recv(message=message)

    async def _recv(self, message: str):

        if message.isdigit():
            return
        self.log.ws_event(message)

        if message == "3probe":
            await self.wsend("5")
            roommsg = [
                "room::join",
                {"room": self.botconfig.roomname}
            ]
            await self.wsend(roommsg)
            asyncio.create_task(self.pacemaker())
            return

        data = json.loads(message[2:])

        if data[0] == "room::updateUserList":
            for user in data[1].get("users", []):
                if user:
                    self.ul.add(User(**user))
            if user:=  data[1].get("user", None):
                if user:
                    self.ul.add(User(**user))
        if data[0] == "room::updateUser":
            self.ul.update(User(**data[1].get("user", None)))

        if data[0] == "room::updateUsers":
            for user in data[1].get("users", []):
                self.ul.update(User(**user))

        #todo  update userlist when a name changes.
        if data[0] == "room::handleChange":
            # ["room::handleChange",{"userId":"5e22c017be8a4900076d3e21","handle":"Tech"}]
            pass
        if data[0] == "room::disconnect":
            self.ul.remove(User(**data[1].get("user", None)))

        if data[0] == "self::join":
            nickmsg = [
                "room::handleChange", {
                    "userId": self.api.login_data.user.get("userId"),
                    "handle": self.botconfig.nickname
                }
            ]
            await self.wsend(nickmsg)
            await self.wsend('42["room::users", {}]')

            # deprecated
            # user_list_data = await self.api.getroominfo(room=str(self.room))
            # self.ul = UserList(**user_list_data)
        if data[0] == "client::error":
            if error := data[1].get("error", False):
                if error == 'ERR_ACCOUNT_REQUIRED':
                    await self.disconnect()
                    raise Exception("Account must be signed in to join this room.")
                if error == 'ENOSESSION':
                    await self.disconnect()
                    raise Exception("Session was invalidated.")

        if data[0] == "room::message":
            prefix = self.botconfig.prefix
            sender = self.ul.get_by_id(id=data[1].get("userId"))
            # bug when user is inside room twice
            # todo take a closer look at how the data invalidates.
            if sender:
                data[1].update({"sender": sender})

                self.log.chat(msg=f"{sender.handle}|{sender.username}: {data[1].get('message')}")

            if data[1].get("message").startswith(prefix):
                c = Command(prefix=prefix, data=Message(**data[1]))
                if c.name == "reload" or c.name == "load":
                    if m := self.cm.import_module(c.message, self):
                        self.cm.add_cog(m, c.message, self)
                        await self.wsend(
                            Message.makeMsg(message=f"{c.name}ed {c.message}",
                                            room=self.room))
                    else:
                        await self.wsend(
                            Message.makeMsg(message=f"failed to {c.name} {c.message}",
                                            room=self.room))
                if c.name == "unload":
                    if self.cm.unload(c.message):
                        await self.wsend(
                            Message.makeMsg(message=f"unloaded {c.message}",
                                            room=self.room))
                    else:
                        await self.wsend(
                            Message.makeMsg(message=f"Could not unload {c.message}",
                                            room=self.room))
                if c.name == "loaded":
                    await self.wsend(
                        Message.makeMsg(message=f"modules: {self.cm.modules}, cogs:{self.cm.cogs}",
                                        room=self.room))
                await self.cm.do_command(c)
        await self.cm.do_event(data=data)

    async def pacemaker(self):
        if self.state == BotState.RUNNING:
            await asyncio.sleep(25)
            await self._ws.send("2")
            asyncio.create_task(self.pacemaker())

    def process_input(self, loop):
        prefix = self.botconfig.prefix
        while self.state == BotState.RUNNING:
            stdin = input()
            if stdin.startswith(prefix):
                asyncio.run_coroutine_threadsafe(
                    self._recv(message=Message(message=stdin).jumpson()),
                    loop=loop)
            else:
                asyncio.run_coroutine_threadsafe(
                    self.wsend(Message.makeMsg(message=stdin, room=self.room)),
                    loop=loop)
