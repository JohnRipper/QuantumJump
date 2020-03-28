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
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog
from lib.command import makeCommand, Command


class Man(Cog):
    pass
    # async def getman(self, query: str):
    #     url = ""
    #     async with aiohttp.ClientSession() as session:

    # @makeCommand(aliases=["man"], description="Return a description from die.net")
    # async def manpage(self, c: Command):
    #     if c.message is None:
    #         await self.send_action("needs a query")
    #     else:
    #         searched = await self.getman(c.message)
    #         if searched is None:
    #             await self.send_action(f"couldn't find {c.message}")
    #         elif self.settings["justname"] is True:
    #             name = searched["NAME"]
    #             await self.send_message(name)
    #         else:
    #             description = searched["DESCRIPTION"]
    #             await self.send_message(description)

