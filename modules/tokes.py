# -*- coding: utf-8 -*-
#
# Copyright 2019, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 2/8/20
# This file is part of QuantumJump.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import asyncio
import datetime
import random
import time
from dataclasses import field
from enum import Enum

from attr import dataclass

from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.objects import BotState
from lib.styling import Colors, Styles
from sched import scheduler

@dataclass
class Action:
    action: str
    joined: [str] = field(default_factory=str)
    active: bool = False


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.s = scheduler(time.time, asyncio.sleep)
        self.is_running_hourly = self.settings["hourly_420"]
        self.how_many_420 = 0

        if self.is_running_hourly:
            asyncio.create_task(self.start_420_counter())

        # undone
        self.cheers_replies = self.settings["cheers"]
        self.actions = {}
        self.running = ""

        self.prepares = self.settings["pre"]
        self.post_timer = self.settings["post"]

    async def start_420_counter(self):
        # figure out next 420
        current_minute = datetime.datetime.now().minute
        wait_time = 60 - current_minute + 20
        pre_wait_time = 60 - current_minute + 15
        self.s.enter(pre_wait_time, 1, self.pre_happy_420, str(self.how_many_420))

        self.s.enter(wait_time, 1, self.happy_420, f"{wait_time} minutes")

    async def pre_happy_420(self):
        await self.send_message("5 minutes before 420",
                                color=Colors.greenalt,
                                style=Styles.bold)

    async def happy_420(self):
        await self.send_message("It's 420 somewhere",
                                color=Colors.greenalt,
                                style=Styles.bold)

    @makeCommand(aliases=["420hour"],
                 description="enables/disables call for tokes hourly.")
    async def hour420(self, c: Command):
        self.is_running_hourly = not self.is_running_hourly
        await self.send_message(f"Hourly 420 notification set to: { self.is_running_hourly}",
                                color=Colors.greenalt,
                                style=Styles.bold)

    @makeCommand(aliases=["cheers"],
                 description="Cheers!")
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
            total_seconds = float(c.message)
            if total_seconds > 9223372036.854775:
                await self.send_message(f"{c.message.handle} caused an integer overflow error!!!!!!! HOW DARE YOU@!")
                return
            self.actions.update({c.name: Action(active=True, action=c.name, joined=[c.data.handle])})
        await self.do(thing=c.name, total_seconds=total_seconds)

    @makeCommand(aliases=["call"], description="<str> <int> calls for chugs")
    async def call_thing(self, c: Command):
        if c.message:
            try:
                thing, seconds = c.message.split(" ", 1)
            except ValueError:
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


