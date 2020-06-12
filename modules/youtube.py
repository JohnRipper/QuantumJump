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
from urllib.parse import parse_qs, urlparse

import aiohttp
import requests

from lib.cog import Cog, event
from lib.command import Command, makeCommand
from lib.objects import Playlist, PlaylistUpdate, PlayVideo, UserList


class Youtube(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.headers: dict = None
        self.api_key: str = self.settings["api_key"]
        self.current_duration: int = None

    async def ytsearch(self, query: str) -> dict:
        searchurl = "https://www.googleapis.com/youtube/v3/search?"\
            "part=snippet&type=video&q={query}&maxResults=1&"\
            "videoSyndicated=true&key={key}"
        url = searchurl.format(query=query, key=self.api_key)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                ytjson = await response.json()
                print(ytjson)
                if ytjson.get("error", False):
                    return {}
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

        if re.search("youtu(be\\.com|\\.be)", c.message):
            ytid = re.search("(?:v=|\\.be\\/)(.{11})", c.message)[1]
            title = await self.ytidsearch(ytid)
            await self.play(video_id=ytid, title=title)
        else:
            ytinfo = await self.ytsearch(c.message)
            if len(ytinfo) > 0:
                await self.play(video_id=ytinfo["video_id"], title=ytinfo["title"])
            else:
                # failed try the back up search
                await self.find(c)

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

    async def get_video_id(self, query, embed_search):
        if embed_search:
            q = f"!ducky+site:youtube.com/embed/+{query}"
        else:
            q = f"!ducky+site:youtube.com+{query}"

        url = f"http://api.duckduckgo.com/?q=" + q + "&format=json&no_redirect=1"
        print(url)
        request = requests.get(url)
        video_id = None
        if len(request.text) > 0:
            data = json.loads(request.text)
            if redirect_url := data.get("Redirect", False):
                video_url = urlparse(redirect_url)
                if video_url.hostname == 'youtu.be':
                    video_id = video_url.path[1:]
                if video_url.hostname in ('www.youtube.com', 'youtube.com'):
                    if video_url.path == '/watch':
                        video_id = parse_qs(video_url.query)['v'][0]
                    if video_url.path[:7] == '/embed/':
                        video_id = video_url.path.split('/')[2]
                    if video_url.path[:3] == '/v/':
                        video_id = video_url.path.split('/')[2]
        if embed_search and not video_id:
            return await self.get_video_id(query, False)
        else:
            return video_id

    @makeCommand(aliases=["find"], description="find a youtube video")
    async def find(self, c: Command):
        if c.message:
            video_id = await self.get_video_id(c.message, True)
            # get url id.
            if video_id:
                data = await self.bot.api.get("https://jumpin.chat/api/youtube/search/" + video_id)
                title = await data.json()
                await self.play(video_id=video_id, title=title[0].get("title", "No title found"))
            else:
                await self.send_message("I couldnt find shit. blame PrefB")
        else:
            await self.send_message("SEARCH FOR SOMETHING???")

    @makeCommand(aliases=["skip", "next"], description="skip video")
    async def skip(self, c: Command):
        await self.settime(self.current_duration)

    @makeCommand(aliases=["seek"], description="seek a video")
    async def seek(self, c: Command):
        m = c.message.strip()
        if m.isnumeric() and int(m) <= self.current_duration and self.current_duration is not None:
            await self.settime(m)
        elif int(m) > self.current_duration:
            await self.send_message(f"The video is only {self.current_duration} seconds long")
        else:
            await self.send_message(f"{m} is not a number.")

    @event(event="room::updateUserList")
    async def notgreat(self, _: UserList):
        # HACK to recieve the "playvideo" event from jumpin
        # sending a full join message with
        # user["settings"]["playYtVideos"] might avoid this
        await self.ws_send(["youtube::checkisplaying",{"notify": True}])

    @event(event="youtube::playvideo")
    async def update(self, video: PlayVideo):
        self.current_duration = int(video.duration)
