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
import json
import re

import aiohttp

from lib.cog import Cog, event
from lib.command import Command, makeCommand
from lib.objects import JumpinError
from lib.styling import Colors, Styles


class Youtube(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.headers = None
        self.api_key = self.settings["api_key"]

        if len(self.api_key) == 0:
            self.api_key = "AIzaSyClXZOfbl68EYsCN2NQ5XM-b_a_0fulO74"
            self.headers = {"referer": "https://tinychat.com"}

    async def ytsearch(self, query: str) -> dict:
        searchurl = "https://www.googleapis.com/youtube/v3/search?"\
            "part=snippet&type=video&q={query}&maxResults=1&"\
            "videoSyndicated=true&key={key}"
        url = searchurl.format(query=query, key=self.api_key)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                ytjson = await response.json()
                print(ytjson)
                videoid = ytjson["items"][0]["id"]["videoId"]
                title = ytjson["items"][0]["snippet"]["title"]
                return {"title": title, "video_id": videoid}

    async def ytidsearch(self, videoid: str) -> str:
        idurl = "https://jumpin.chat/api/youtube/search/https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{videoid}"
        url = idurl.format(videoid=videoid)
        ytjson = await self.bot.api.get(url)
        print(ytjson)
        data = json.loads(await ytjson.text())
        title = data[0]["title"]
        return title

    @makeCommand(aliases=["yt"], description="<query | url> play youtube")
    async def playyt(self, c: Command):
        if re.search("youtu(be\.com|\.be)", c.message):
            ytid = re.search("(?:v=|\.be\/)(.{11})", c.message)[1]
            title = await self.ytidsearch(ytid)
            await self.play(video_id=ytid, title=title)
        else:
            ytinfo = await self.ytsearch(c.message)
            await self.play(video_id=ytinfo["video_id"], title=ytinfo["title"])

    @makeCommand(aliases=["rm"], description="remove a video from the playlist")
    async def removeyt(self, c: Command):
        # TODO
        message = c.message.strip()
        if message.isdigit():
            pass
        elif len(message) == 0:
            pass
        elif message == "all":
            pass
        else:
            # attempt to match to title?
            pass

    @makeCommand(aliases=["pl"], description="append a playlist to jumpin's playlist")
    async def addplaylist(self, c: Command):
        pass

    @event(event="client::error")
    async def error(self, err: JumpinError):
        if err.message == "Error starting Youtube video":
            await self.send_message("Jumpin's quota has been reached :sob:",
                                    color=Colors.red,
                                    style=Styles.bold)
