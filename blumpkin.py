import asyncio
import json
import time
from enum import Enum

import websockets

from lib.http import Http
from lib.cog import CogManager
from lib.command import Command
from lib.objects import Message, User, UserList, BotState, Join


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

    async def wsend(self, data):
        if type(data) is list:
            data = "42{}".format(json.dumps(data))
        elif type(data) is str:
            type_exemptions = ["2probe", "5", "2"]
            if not data.startswith("42") and data not in type_exemptions:
                data = f"42{data}"
        else:
            print("invalid data type for wsend")
        await self._ws.send(data)
        print(f"SEND {data}")

    async def run(self):
        enabled_modules = self.settings.Modules["enabled"]
        self.cm.load_all(enabled_modules, bot=self)
        await self.connect()

    async def disconnect(self):
        self.state = BotState.DISCONNECT
        await self._ws.close()

    async def connect(self):
        await self.api.login(self.botconfig.username,
                             self.botconfig.password)

        async with websockets.connect(
                uri=await self.api.get_wss(),
                timeout=600,
                origin="https://jumpin.chat"
        ) as self._ws:
            print("Socket started")
            self.state = BotState.RUNNING
            await self.wsend("2probe")
            async for message in self._ws:
                await self._recv(message=message)

    async def _recv(self, message: str):
        print(f"RECV {message}")
        if message.isdigit():
            return
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
        await self.cm.do_event(data=data)

        if data[0] == "room::updateUserList":
            for user in data[1].get("users", []):
                if user:
                    self.ul.add(User(**user))
            if user:=  data[1].get("user", None):
                if user:
                    print(user)
                    self.ul.add(User(**user))
        if data[0] == "room::updateUser":
            self.ul.update(User(**data[1].get("user", None)))

        #todo  update userlist when a name changes.
        if data[0] == "room::handleChange":
            # ["room::handleChange",{"userId":"5e22c017be8a4900076d3e21","handle":"Tech"}]
            pass
        if data[0] == "room::disconnect":
            self.ul.remove(User(**data[1].get("user", None)))

        if data[0] == "self::join":
            nickmsg = [
                "room::handleChange", {
                    "userId": self.api.login_data.user.get("user_id"),
                    "handle": self.botconfig.nickname
                }
            ]
            await self.wsend(nickmsg)
            # deprecated
            # user_list_data = await self.api.getroominfo(room=str(self.room))
            # self.ul = UserList(**user_list_data)
        if data[0] == "client::error":
            if error := data[1].get("error", False):
                # todo logger
                # todo create an enum for different error codes.

                if error == 'ERR_ACCOUNT_REQUIRED':
                    # if we do not disconnect, spy mode becomes possible.
                    await self.disconnect()
                    raise Exception("Account must be signed in to join this room.")
                if error == 'ENOSESSION':
                    # if we do not disconnect, spy mode becomes possible.
                    await self.disconnect()
                    raise Exception("Session was invalidated.")

        if data[0] == "room::message":
            prefix = self.botconfig.prefix
            if data[1].get("message").startswith(prefix):
                print(type(self.ul))
                # data[1].update({"sender": self.ul.get_by_handle(handle=data[1].get("handle"))})
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

    async def pacemaker(self):
        if self.state == BotState.RUNNING:
            await asyncio.sleep(25)
            await self.wsend("2")
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
