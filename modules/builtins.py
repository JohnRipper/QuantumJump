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
from datetime import datetime

from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.styling import Styles
from lib.util import get_current_sha1, get_latest_sha1


class Builtins(Cog):
    @makeCommand(aliases=["version"], description="get the current version")
    async def version(self, c: Command):
        message = ":crystal_ball: currently using: *{}* | Latest is: *{}*".format(
            get_current_sha1(),
            await get_latest_sha1()
        )
        await self.send_message(message)

    @makeCommand(aliases=["uptime"], description="get the bot's uptime")
    async def uptime(self, c: Command):
        current = datetime.now()
        start = datetime.fromtimestamp(self.bot.start_time)
        difference = str(current - start)
        # strip after the decimal
        message = "has been alive for {} ⏱".format(
            str(difference)[:7].replace(":", ";"))
        await self.send_action(message, style=Styles.bold)

    @makeCommand(aliases=["timer"], description="a seconds timer ")
    async def timer(self, c: Command):
        if c.message.isdigit():
            await self.send_message(f"Set a timer set for {c.message}")
            await asyncio.sleep(int(c.message))
            await self.send_message(f"Timer has expired!")
