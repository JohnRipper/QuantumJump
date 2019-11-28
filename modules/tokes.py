import asyncio
import datetime
import random

from lib.objects import BotState
from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.styling import Colors, Styles, encodetxt

CHEERS = ["▂▅▇ 🔥 CHEERS 🔥 ▇▅▂"]
ACTIONS = []
RESPONSES = [
    "torches", "lights up", "blazes", "bakes", "hotboxes your nan's bathroom",
    "puffs", "sparks their blunt", "lights their blunt", "sparks their joint",
    "lights their joint", "tokes", "sits this one out",
    "gets a shotgun from your mom"
]


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        # self.settings = self.bot.settings["module"]["tokes"]
        # self.is_running_hourly = self.bot.settings["module"]["tokes"]["hourly_420"]
        self.is_running_hourly = True
        asyncio.create_task(self.it_is_420())

    async def it_is_420(self):
        while self.bot.state is BotState.RUNNING and self.is_running_hourly:
            minute = datetime.datetime.now().minute
            if minute == 20:
                await self.send_message("it is 420 somewhere")
            await asyncio.sleep(60)
            pass

    @makeCommand(name="420hour",
                 description="enables/disables call for tokes hourly.")
    async def hour420(self, c: Command):
        self.is_running_hourly = not self.is_running_hourly
        await self.send_message("Hourly 420 notification set to: {}".format(
            self.is_running_hourly))

    @makeCommand(name="timer", description="a seconds timer ")
    async def timer(self, c: Command):
        if c.message.isdigit():
            await self.send_message(f"Set a timer set for {c.message}")
            await asyncio.sleep(int(c.message))
            await self.send_message(f"Timer has expired!")

    @makeCommand(name="cheers", description="Cheers!")
    async def cheers(self, c: Command):
        await self.send_message(random.choice(CHEERS), style=Styles.script)

    @makeCommand(name="tokes", description="<int> calls for tokes")
    async def tokes(self, c: Command):
        if c.message.isdigit():
            total_seconds = int(c.message)
            minutes = int(total_seconds / 60)
            seconds = int(total_seconds % 60)
            # starting message
            if minutes != 0:
                await self.send_message(
                    f"Calling for tokes in {minutes} minutes {seconds} seconds!"
                )
            else:
                await self.send_message(f"Calling for tokes in {seconds}!")
            # start counting down.
            for i in range(0, minutes):
                await asyncio.sleep(60)
                if minutes - i <= 5 & minutes - i != 0:
                    await self.send_message(f"{minutes} left before tokes.")
            await asyncio.sleep(seconds)
            await self.send_message("Time for tokes!", color=Colors.green, style=Styles.bold)
        else:
            await self.send_message("Time for tokes!", color=Colors.green, style=Styles.bold)
