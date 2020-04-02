# -*- coding: utf-8 -*-
#
# Copyright 2020, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 4/1/20
# This file is part of QuantumJump
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

import wolframalpha

from lib.cog import Cog
from lib.command import Command, makeCommand


class Jarvis(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self.wolframalpha_appid = self.settings["wolframalpha_appid"]
        self.client = wolframalpha.Client(self.wolframalpha_appid)

    async def check_pods(self, pods: dict):
        pod_count = pods.get("@numpods")
        if pod_count:
            if pod_count == '0':
                await self.send_message("Invalid question")
            elif pod_count == '1':
                pod = pods.get("pod")
                await self.process_pod(pod)
            else:
                for pod in pods.get("pod"):
                    await self.process_pod(pod)

    async def process_pod(self, pod: dict):
        subpod_count = pod.get("@numsubpods")
        if subpod_count:
            if subpod_count == '1':
                subpod = pod.get("subpod")
                # send msg
                await self.send_message(subpod.get("plaintext"))
            elif subpod_count == '0':
                await self.send_message("No result")
            else:
                for subpod in pod.get("subpod"):
                    await self.send_message(subpod.get("plaintext"))

    @makeCommand(aliases=["ask"], description=["ask whatever the fuck you want"])
    async def ask(self, c: Command):
        if c.message != "":
            d = self.client.query(c.message)
            await self.check_pods(d)
        else:
            await self.send_message("Forgot to ask something")
