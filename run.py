import asyncio
from concurrent import futures
import websockets
from blumpkin import QuantumJumpBot


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.pacemaker)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_input)
    try:
        await bot.run()
    except websockets.WebSocketException as e:
        bot.is_running = False

executor = futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumJumpBot("default")

asyncio.get_event_loop().run_until_complete(start(executor, bot))
