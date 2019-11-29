import asyncio
import datetime
import random

from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.objects import BotState
from lib.styling import Colors, Styles


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        print(self.settings)
        self.cheers_replies = self.settings["cheers"]
        self.prepares = self.settings["pre"]
        self.post_timer = self.settings["post"]
        self.is_running_hourly = self.settings["hourly_420"]
        if self.is_running_hourly:
            asyncio.create_task(self.it_is_420())

    async def it_is_420(self):
        while self.bot.state is BotState.RUNNING and self.is_running_hourly:
            minute = datetime.datetime.now().minute
            if minute == 20:
                await self.send_message("It's 420 somewhere",
                                        color=Colors.greenalt,
                                        style=Styles.bold)
            await asyncio.sleep(60)
            pass

    @makeCommand(name="420hour",
                 description="enables/disables call for tokes hourly.")
    async def hour420(self, c: Command):
        self.is_running_hourly = not self.is_running_hourly
        await self.send_message("Hourly 420 notification set to: {}".format(
            self.is_running_hourly),
                                color=Colors.greenalt,
                                style=Styles.bold)

    @makeCommand(name="cheers", description="Cheers!")
    async def cheers(self, c: Command):
        await self.send_message(random.choice(self.cheers_replies),
                                style=Styles.script)
        await asyncio.sleep(0.6)
        await self.send_action(random.choice(self.post_timer),
                               color=Colors.greenalt)

    @makeCommand(name="tokes", description="<int> calls for tokes")
    async def tokes(self, c: Command):
        if c.message.isdigit():
            total_seconds = int(c.message)
            minutes = int(total_seconds / 60)
            seconds = int(total_seconds % 60)
            # starting message
            if minutes != 0:
                await self.send_message(
                    f"Calling for tokes in {minutes} minutes {seconds} seconds!",
                    color=Colors.greenalt)
                await self.send_action(random.choice(self.prepares),
                                       color=Colors.greenalt)
            else:
                await self.send_message(f"Calling for tokes in {seconds}!",
                                        color=Colors.greenalt)
                await self.send_action(random.choice(self.prepares),
                                       color=Colors.greenalt)
            # start counting down.
            for i in range(0, minutes):
                await asyncio.sleep(60)
                if minutes - i <= 5 & minutes - i != 0:
                    await self.send_message(f"{minutes} left before tokes.")
            await asyncio.sleep(seconds)
            await self.send_message("Time for tokes!",
                                    color=Colors.greenalt,
                                    style=Styles.bold)
            await asyncio.sleep(0.6)
            await self.send_action(random.choice(self.post_timer),
                                   color=Colors.greenalt)
        else:
            await self.send_message("Time for tokes!",
                                    color=Colors.greenalt,
                                    style=Styles.bold)
            await asyncio.sleep(0.6)
            await self.send_action(random.choice(self.post_timer),
                                   color=Colors.greenalt)
