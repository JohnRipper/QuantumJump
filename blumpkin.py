import asyncio
import sys
from pathlib import Path
import json
import time
import tomlkit
import websockets
from lib.api import Api
from lib.cog import CogManager
from lib.command import Command
from lib.objects import Message, UpdateUserList, UserList, User


class QuantumJumpBot:

    def __init__(self, settings_file: str):
        self._ws = None
        self.is_running = False
        self.start_time = time.time()
        self._settings = None
        self.settings_file = settings_file
        self.api = Api()
        self.cm = CogManager()

    @property
    def settings(self):
        if not self._settings:
            config = Path(f"{self.settings_file}.toml")
            if config.exists():
                self._settings = tomlkit.loads(config.read_text())
            else:
                sys.exit("Configuration not found, exiting.")
        return self._settings

    @property
    async def userlist(self) -> [User]:
        data = await self.api.getroominfo(room=str(self.settings["bot"]["room"]))
        ul = UserList(**data)
        return ul.users

    async def wsend(self, data):
        await self._ws.send(f"42{data}")

    async def run(self):
        self.cm.load_all(self.settings["modules"].get("enabled"), bot=self)
        await self.connect()

    async def disconnect(self):
        self.is_running = False
        await self._ws.close()

    async def connect(self):
        await self.api.login(self.settings["bot"].get("username", None),
                                   self.settings["bot"].get("password", None))

        async with websockets.connect(uri=await self.api.get_wss(),
                                      timeout=600,
                                      origin="https://jumpin.chat") as self._ws:
            print("Socket started")
            self.is_running = True
            await self._ws.send("2probe")
            async for message in self._ws:
                await self._recv(message=message)

    async def _recv(self, message: str):
                print(message)
                if message.isdigit():
                    return
                if message == "3probe":
                    await self._ws.send("5")
                    await self._ws.send("42[\"room::join\",{\"room\":\"johnripper\"}]")
                    asyncio.create_task(self.pacemaker())
                    return

                data = json.loads(message[2:])
                await self.cm.do_event(data=data)
                if data[0] == "self::join":
                    await self._ws.send(
                        f"42[\"room::handleChange\",{{\"userId\":\"{self.api.session.user.get('user_id')}\",\"handle\":\"PROFESSOR_X\"}}]")

                if data[0] == "room::message":
                    prefix = '.'
                    if data[1].get("message").startswith(prefix):
                        c = Command(prefix=prefix, data=Message(**data[1]))
                        if c.name == "reload" or c.name == "load":
                            m = self.cm.import_module(c.message)
                            self.cm.add_cog(m, c.message, self)
                            print("reloaded")
                        if c.name == "unload":
                            m = self.cm.unload(c.message)
                        # do cog commands.
                        await self.cm.do_command(c)


    async def pacemaker(self):
        await asyncio.sleep(25)
        if self.is_running:
            await self._ws.send("2")
            asyncio.create_task(self.pacemaker())

    def process_input(self, loop):
        prefix = '.'
        while True:
            if self.is_running:
                f = input()
                if f.startswith(prefix):
                    m = Message(message=f)
                    data = f"42[\"room::message\", {json.dumps(m.__dict__)}]"
                    asyncio.run_coroutine_threadsafe(self._recv(message=data), loop)
                else:
                    asyncio.run_coroutine_threadsafe(self.send_message(f), loop)

    async def send_message(self, message: str, room=None):
        if not room:
            room = self.settings["bot"]["room"]
        data = [
            "room::message",
            {
                "message": message,
                "room": room
            }
        ]
        await self.wsend(data=json.dumps(data))

    async def process_message_queue(self):
        if self.is_running:
            asyncio.run(asyncio.sleep(1))
            # await self.send_message()
            asyncio.create_task(self.process_message_queue())

    async def GetClasses(self):
        return [x for x in globals() if hasattr(globals()[str(x)], '__cog__')]


