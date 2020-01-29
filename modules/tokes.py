import asyncio
import datetime
import random
from dataclasses import field
from enum import Enum

from attr import dataclass

from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.objects import BotState
from lib.styling import Colors, Styles

@dataclass
class Action:
    action: str
    joined: [str] = field(default_factory=str)
    active: bool = False


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.cheers_replies = self.settings["cheers"]
        self.actions = {}
        self.running = ""

        self.prepares = self.settings["pre"]
        self.post_timer = self.settings["post"]
        self.is_running_hourly = self.settings["hourly_420"]

        if self.is_running_hourly:
            asyncio.create_task(self.it_is_420())

    async def it_is_420(self):
        last_hr = 0
        while self.bot.state is BotState.RUNNING and self.is_running_hourly:
            minute = datetime.datetime.now().minute
            hour = datetime.datetime.now().hour
            # prevent message repeats.
            if minute == 20 and (last_hr < hour or hour == 0):
                await self.send_message("It's 420 somewhere",
                                        color=Colors.greenalt,
                                        style=Styles.bold)
                last_hr = hour
                # let the internal timer sleep for 50 minutes before checking the clock again.
                await asyncio.sleep(int(60 * 50))
            # todo a count down?
            await asyncio.sleep(60)

    @makeCommand(aliases=["420hour"],
                 description="enables/disables call for tokes hourly.")
    async def hour420(self, c: Command):
        self.is_running_hourly = not self.is_running_hourly
        await self.send_message("Hourly 420 notification set to: {}".format(
            self.is_running_hourly),
                                color=Colors.greenalt,
                                style=Styles.bold)

    @makeCommand(aliases=["cheers"], description="Cheers!")
    async def cheers(self, c: Command):
        await self.send_message(random.choice(self.cheers_replies),
                                style=Styles.script)
        await asyncio.sleep(0.6)
        await self.send_action(random.choice(self.post_timer),
                               color=Colors.greenalt)

    @makeCommand(aliases=["join"], description="joins tokes")
    async def join(self, c: Command):
        if action := self.actions.get('tokes', False):
            if action.active:
                homies = str(action.joined)[1:-1]
                if c.data.handle in action.joined:
                    await self.send_message(f"{c.data.handle} already joined {homies} for {self.running}!!!",
                                            color=Colors.greenalt,
                                            style=Styles.bold)
                else:
                    await self.send_message(f"{c.data.handle} has joined {homies} for {self.running}!!!",
                                            color=Colors.greenalt,
                                            style=Styles.bold)
                    action.joined.append(c.data.handle)
                    self.actions.update({c.name: action})

    @makeCommand(aliases=["tokes"], description="<int> calls for tokes")
    async def tokes(self, c: Command):
        await self.do_wrap(c)

    @makeCommand(aliases=["chugs"], description="<int> calls for chugs")
    async def chugs(self, c: Command):
        await self.do_wrap(c)

    async def do_wrap(self, c: Command):
        if action := self.actions.get(c.name, False):
            if action.active:
                await self.join(c)
                return
        total_seconds = 0
        if c.message.isdigit():
            total_seconds = c.message
            self.actions.update({c.name: Action(active=True, action=c.name, joined=[c.data.handle])})
        await self.do(thing=c.name, total_seconds=total_seconds)

    @makeCommand(aliases=["call"], description="<str> <int> calls for chugs")
    async def call_thing(self, c: Command):
        if c.message:
            try:
                thing, seconds = c.message.split(" ", 1)
            except (ValueError):
                thing = c.message
                seconds = 0

            seconds = int(seconds)
            if type(thing) is str and type(seconds) is int:
                await self.do(thing=thing, total_seconds=seconds)
        else:
            await self.send_message("call who? your sister?")

    async def do(self, thing: str, total_seconds: int = 0):
        total_seconds = int(total_seconds)
        if total_seconds == 0:
            await self.send_message(f"Time for {thing}!",
                                    color=Colors.greenalt,
                                    style=Styles.bold)
            await self.send_action(random.choice(self.post_timer),
                                   color=Colors.greenalt)
        else:
            minutes = int(total_seconds / 60)
            seconds = int(total_seconds % 60)
            # starting message
            if minutes != 0:
                await self.send_message(
                    f"Calling for {thing} in {minutes} minutes {seconds} seconds!",
                    color=Colors.greenalt)
                await self.send_action(random.choice(self.prepares),
                                       color=Colors.greenalt)
            else:
                await self.send_message(f"Calling for {thing} in {seconds}!",
                                        color=Colors.greenalt)
                await self.send_action(random.choice(self.prepares),
                                       color=Colors.greenalt)
            self.running = thing
            # start counting down.
            for i in range(0, minutes):
                if minutes - i <= 5 & minutes - i != 0:
                    await self.send_message(f"{minutes} left before {thing}.")
                    await asyncio.sleep(60)

            await asyncio.sleep(seconds)
            await self.send_message(f"Time for {thing}!",
                                    color=Colors.greenalt,
                                    style=Styles.bold)

            if action := self.actions.get(thing, False):
                homies = str(action.joined)[1:-1]
                if len(action.joined) == 1:
                    await self.send_message(f"{homies} called for {thing}, and noone joined! Oh well, fuck it!!!",
                                            color=Colors.greenalt,
                                            style=Styles.bold)
                else:
                    await self.send_message(f"{homies} joined for {thing}!!!",
                                            color=Colors.greenalt,
                                            style=Styles.bold)
                await self.send_message(f"Time for {thing}!",
                                        color=Colors.greenalt,
                                        style=Styles.bold)
                action.active = False
                action.joined = []
                self.actions.update({action.action: action})
                self.running = ""
            await asyncio.sleep(0.6)
            await self.send_action(random.choice(self.post_timer),
                                   color=Colors.greenalt)
