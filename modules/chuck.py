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

import aiohttp

from lib.cog import Cog
from lib.command import makeCommand, Command


class Chuck(Cog):
    @makeCommand(aliases=["cn", "chuck"], description="Random Chuck Norris joke.")
    async def chucknorris(self, c: Command):
        url = "https://api.chucknorris.io/jokes/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await self.send_message(f"Got {response.status} from chucknorris.io.")
                else:
                    try:
                        cnjson = await response.json()
                        await self.send_action(cnjson["value"])
                    except (IndexError, KeyError) as e:
                        await self.send_message("Error while parsing the json.")

    # his real name is carlos.
    @makeCommand(aliases=["carlos"], description="Random Carlos Norris joke.")
    async def carlosnorris(self, c: Command):
        url = "https://api.chucknorris.io/jokes/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await self.send_message(f"Got {response.status} from chucknorris.io.")
                else:
                    try:
                        cnjson = await response.json()
                        sentence = cnjson["value"].replace("chuck", "Carlos")
                        sentence = cnjson["value"].replace("Chuck", "Carlos")
                        await self.send_action(sentence)
                    except (IndexError, KeyError) as e:
                        await self.send_message("Error while parsing the json.")
