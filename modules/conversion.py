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

from lib.cog import Cog
from lib.command import Command, makeCommand


class Conversion(Cog):
    @makeCommand(aliases=["t", "temp"], description="Convert a temp")
    async def convert_temp(self, c: Command):
        units = ["f", "c"]
        from_unit = c.message[-1].lower()
        if from_unit in units and from_unit == "f":
            toconvert = c.message.rstrip("f")
            # strip '-' for negative numbers before checking if its a digit
            if toconvert.lstrip("-").isdigit():
                converted = (int(toconvert) - 32) * 5 / 9
                fmt = ":thermometer: {}°F is {}°C".format(
                    toconvert, round(converted))
                await self.send_message(fmt)
            pass
        elif from_unit in units and from_unit == "c":
            toconvert = c.message.rstrip("c")
            if toconvert.lstrip("-").isdigit():
                converted = int(toconvert) * 1.8 + 32
                fmt = ":thermometer: {}°C is {}°F".format(
                    toconvert, round(converted))
                await self.send_message(fmt)
        else:
            await self.send_action("doesn't think that is a valid unit")
