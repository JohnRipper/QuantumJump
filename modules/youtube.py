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
            self.api_key = "AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg"
            self.headers = {"referer": "https://tinychat.com"}

    async def ytsearch(self, query: str) -> dict:
        searchurl = "https://www.googleapis.com/youtube/v3/search?"\
            "part=snippet&type=video&q={query}&maxResults=1&"\
            "videoSyndicated=true&key={key}"
        url = searchurl.format(query=query, key=self.api_key)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                ytjson = await response.json()
                videoid = ytjson["items"][0]["id"]["videoId"]
                title = ytjson["items"][0]["snippet"]["title"]
                return {"title": title, "video_id": videoid}

    async def ytidsearch(self, videoid: str) -> str:
        idurl = "https://www.googleapis.com/youtube/v3/videos?"\
            "part=contentDetails,snippet&id={videoid}&fields="\
            "items(contentDetails%2Fduration%2Csnippet(channelTitle%2Ctitle))"\
            "&key={key}"
        url = idurl.format(videoid=videoid, key=self.api_key)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                ytjson = await response.json()
                title = ytjson["items"][0]["snippet"]["title"]
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
