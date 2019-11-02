import asyncio
import json
import re as regex
import sys
import time
from concurrent import futures

import tomlkit
import websockets


class QuantumJumpBot:

    def __init__(self):
        self._ws = None
        self.is_running = False
        self.start_time = time.time()
        self.modules = []
        self.cogs = []

    async def run(self):
        await self.connect()

    async def connect(self):
        return

    def process_input(self):
        while True:
            if self.is_running:
                f = input()


    def process_message_queue(self):
        while True:
            if self.is_running:
                asyncio.run(asyncio.sleep(1))


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_input)
    while True:
        try:
            await bot.run()
        except websockets.WebSocketException as e:
            bot.is_running = False
            #bot.log.error(f"websocket crashed:{e}\n Restarting in {settings['bot']['restart_time']}")

executor = futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumJumpBot()
asyncio.get_event_loop().run_until_complete(start(executor, bot))
