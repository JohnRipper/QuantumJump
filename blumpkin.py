import asyncio
import sys
from pathlib import Path

import json
import time
from concurrent import futures

import tomlkit
import websockets
from lib.api import Api


class QuantumJumpBot:
    def __init__(self):
        self._ws = None
        self.is_running = False
        self.start_time = time.time()

        self.settings = None

        self.load_config("default.toml")
        self.api = Api()

    def load_config(self, config):
        config = Path(config)
        if config.exists():
            self.settings = tomlkit.loads(config.read_text())
        else:
            sys.exit("Configuration not found, exiting.")

    async def run(self):
        print(self.settings)
        await self.connect()

    async def connect(self):
        print(self.settings["bot"].get("username", None))
        url = await self.api.login(self.settings["bot"].get("username", None),
                                   self.settings["bot"].get("password", None))
        print("Starting socket")
        print(url)
        async with websockets.connect(
                uri=url, timeout=600,
                origin="https://jumpin.chat") as self._ws:
            print("Socket started")
            self.is_running = True
            await self._ws.send("2probe")

            async for message in self._ws:
                print(message)
                if message == "3probe":
                    await self._ws.send("5")
                    await self._ws.send(
                        "42[\"room::join\",{\"room\":\"tech\"}]")

                    continue
                if message.isdigit():
                    if message == "40":
                        continue
                        #await self._ws.send("42[\"room::join\",{\"room\":\"tech\"}]")
                        #await self._ws.send("42[\"room::join\",{\"room\":\"johnripper\"}]")
                        #await ws.send("42[\"room::handleChange\",{\"userId\":\"5dbe52979070930008f85b5c\",\"handle\":\"PROFESSOR_X\"}]")
                        await self._ws.send(data)
                        await asyncio.sleep(1)
                    continue
                adjusted = message[2:]
                data = json.loads(str(adjusted))

    def pacemaker(self):
        while True:
            if self.is_running:
                time.sleep(25)
                asyncio.run(self._ws.send("2"))

    def process_input(self):
        while True:
            if self.is_running:
                f = input()

    def process_message_queue(self):
        while True:
            if self.is_running:
                asyncio.run(asyncio.sleep(1))


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.pacemaker)
    asyncio.get_event_loop().run_in_executor(executor,
                                             bot.process_message_queue)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_input)
    try:
        await bot.run()
    except websockets.WebSocketException as e:
        bot.is_running = False


executor = futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumJumpBot()
bot.load_config("default.toml")

asyncio.get_event_loop().run_until_complete(start(executor, bot))
