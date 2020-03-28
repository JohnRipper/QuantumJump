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

import re

import aiohttp

from lib.cog import Cog
from lib.command import Command, makeCommand


class Urban(Cog):
    base_url = "https://api.urbandictionary.com/v0/define?term={}"

    async def urban_lookup(self, query: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url.format(query)) as response:
                if response.status != 200:
                    definition = f"Got {response.status} from Urban Dictionary's API"
                else:
                    try:
                        urbjson = await response.json()
                        _definition = urbjson["list"][0]["definition"].strip(
                        ).replace("  ", " ")
                        definition = re.sub(r"\[*\]*", "", _definition).replace("\n", " ").replace("\r", " ")
                    except (IndexError, KeyError):
                        definition = f"Couldn't find anything for {query}"
                return definition

    @makeCommand(aliases=["urb"], description="Search Urban Dictionary")
    async def do_urban(self, c: Command):
        if len(c.message) == 0:
            response = "Need a term to lookup"
        else:
            response = await self.urban_lookup(c.message)
        await self.send_message(f"*{c.message}:* {response}")
