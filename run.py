#  -*- coding: utf-8 -*-
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
import sys
import traceback
from concurrent import futures
from blumpkin import QuantumJumpBot, BotState
from lib.config import Configuration
from lib.logging import QuantumLogger


async def start(executor, bot, loop, count=0):
    loop.run_in_executor(executor, bot.process_input, loop)
    try:
        await bot.run()
    except Exception as e:
        # print the caught exception so it doesnt get lost in narnia
        print(e)
        traceback.print_exc(file=sys.stdout)
        bot.state = BotState.EXCEPTION
        await asyncio.sleep(5)
        if bot.botconfig.restart_on_error and count <= bot.botconfig.restart_attempts:
            count += 1
            await start(executor, bot, loop, count)


def load_config():
    try:
        return Configuration("example.toml")
    except FileNotFoundError:
        from lib.config import generate_config, write_config
        generated = generate_config()
        towrite = write_config(generated, "config.toml")
        if towrite:
            return Configuration("config.toml")
        else:
            sys.exit("Couldn't load the configuration")


executor = futures.ThreadPoolExecutor(max_workers=2, )
bot = QuantumJumpBot(load_config())
loop = asyncio.get_event_loop()
loop.run_until_complete(start(executor, bot, loop))
