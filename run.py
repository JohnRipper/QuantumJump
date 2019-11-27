import asyncio
from concurrent import futures
import websockets
from blumpkin import QuantumJumpBot


async def start(executor, bot, loop):
    loop.run_in_executor(executor, bot.process_input, loop)
    try:
        await bot.run()
    except websockets.WebSocketException as e:
        bot.is_running = False

executor = futures.ThreadPoolExecutor(max_workers=1, )
bot = QuantumJumpBot("default")
loop = asyncio.get_event_loop()
loop.run_until_complete(start(executor, bot, loop))
