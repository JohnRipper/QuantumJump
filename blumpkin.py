import asyncio
import sys
from pathlib import Path

import json
import time
from concurrent import futures

import tomlkit
import websockets
from lib.api import Api
from lib.cog import CogManager


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

    async def run(self):
        self.cm.load_all(self.settings["modules"].get("enabled"), bot=self)
        await self.connect()

    async def connect(self):
        await self.api.login(self.settings["bot"].get("username", None),
                                   self.settings["bot"].get("password", None))

        async with websockets.connect(
                uri=await self.api.get_wss(),
                timeout=600,
                origin="https://jumpin.chat"
        ) as self._ws:
            print("Socket started")
            self.is_running = True
            await self._ws.send("2probe")

            async for message in self._ws:
                print(message)
                if message == "3probe":
                    await self._ws.send("5")
                    await self._ws.send("42[\"room::join\",{\"room\":\"tech\"}]")
                    continue
                if message.isdigit():
                    if message == "40":
                        await self._ws.send(f"42[\"room::handleChange\",{{\"userId\":\"{self.api.session.user.get('user_id')}\",\"handle\":\"PROFESSOR_X\"}}]")
                    continue

                data = json.loads(message[2:])

                self.cm.do_event(data=data)
                # todo run bot commands
                # todo run sever events

    def pacemaker(self):
        while True:
            if self.is_running:
                time.sleep(25)
                asyncio.run(self._ws.send("2"))

    def process_input(self):
        while True:
            if self.is_running:
                f = input()
                if f == "exit":
                    sys.exit()

    def process_message_queue(self):
        while True:
            if self.is_running:
                asyncio.run(asyncio.sleep(1))

    async def GetClasses(self):
        return [x for x in globals() if hasattr(globals()[str(x)], '__cog__')]


