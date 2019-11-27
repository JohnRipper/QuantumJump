import asyncio
import sys
from concurrent import futures

import websockets

from blumpkin import QuantumJumpBot
from lib.config import Configuration


async def start(executor, bot, loop):
    loop.run_in_executor(executor, bot.process_input, loop)
    try:
        await bot.run()
    except websockets.WebSocketException as e:
        bot.is_running = False


try:
    config = Configuration("config.toml")
except FileNotFoundError:
    from lib.config import generate_config, write_config
    generated = generate_config()
    towrite = write_config(generated, "config.toml")
    if towrite:
        config = Configuration("config.toml")
    else:
        sys.exit("Couldn't load the configuration")


executor = futures.ThreadPoolExecutor(max_workers=2, )
bot = QuantumJumpBot(config)
loop = asyncio.get_event_loop()
loop.run_until_complete(start(executor, bot, loop))
