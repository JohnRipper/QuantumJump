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

from lib.cog import Cog, event
from lib.command import makeCommand, Command
from lib.objects import Message, JumpinError
from lib.styling import Styles, encodetxt


class Debug(Cog):
    async def get_template(self):
        f = open('./docs/help_template.md', 'r')
        text = f.read()
        command_data = ""

        for cog in self.bot.cm.cogs.values():
            command_data += f"-----{cog.name}------\n"
            for command in cog.commands:
                command_data += f"{getattr(command, '__command_name__')}: {getattr(command, '__description__')}\n"
            command_data += "\n"
        text = text.format(commands=command_data)
        f.close()
        return text

    # @makeCommand(aliases=["t", description="test")
    # async def generate_readme(self, c: Command):
    #     generated = await self.get_template()
    #     f = open('./README.md', 'w')
    #     f.write(generated)
    #     f.flush()
    #     f.close()

    @makeCommand(aliases=["do"], description="makes the bot do something.")
    async def thirdperson(self, c: Command):
        await self.send_action(c.message)

    @makeCommand(aliases=["mock"], description="mocks a socket message.")
    async def mocking_bird(self, c: Command):
        await self.bot._recv(c.message)



    @makeCommand(aliases=["font"], description="")
    async def demofonts(self, c: Command):
        fontstyles = {
            "bold": encodetxt("bold", Styles.bold),
            "italic": encodetxt("italic", Styles.italic),
            "bolditalic": encodetxt("bolditalic", Styles.bolditalic),
            "bubble": encodetxt("bubble", Styles.bubble),
            "bubbleinvert": encodetxt("bubbleinvert", Styles.bubbleinvert),
            "square": encodetxt("square", Styles.square),
            "squareinvert": encodetxt("squareinvert", Styles.squareinvert),
            "script": encodetxt("script", Styles.script)
        }
        if len(c.message) < 2:
            a_ = []
            for each in fontstyles.keys():
                a_.append(fontstyles[each])
            await self.send_message(", ".join(a_))
        else:
            parts = c.message.split(" ")
            type_ = parts[0]
            message = " ".join(parts[1:])
            if type_ in Styles.__dict__.keys():
                formated = encodetxt(message, Styles.__dict__[type_])
            else:
                formated = encodetxt(c.message, Styles.script)
            await self.send_message(formated)

    @makeCommand(aliases=["exception"], description="raises an exception")
    async def testit(self, c: Command):
        raise Exception("I am a T-Rex")

    @makeCommand(aliases=["bw"], description="<sides> <dice>, default is single 6 sided")
    async def hw(self, c: Command):
        await self.send_message("standby - pref's washing his hands in the shower. thanks for your patience in advance")

    #####
    # Events
    #####
    @event(event="client::error")
    async def error(self, error: JumpinError):

        # does not work if bot is guest in  a room with authenticated required.

        if error.message:
            #await self.send_message(f"{error.context}:{error.error}:{error.message}")
            pass
        else:
            #await self.send_message(f"{error.context}:{error.error}")
            pass


    @event(event="room::message")
    async def message(self, message: Message):
        pass


