import re

from lib.cog import Cog, event
from lib.command import makeCommand, Command
from lib.styling import Colors, Styles
from lib.objects import JumpinError, PlaylistUpdate, PlayVideo


class Youtube(Cog):
    async def ytsearch(self, query: str) -> dict:
        searchurl = "https://www.googleapis.com/youtube/v3/search?"\
            "part=snippet&type=video&q={query}&maxResults=1&"\
            "videoSyndicated=true&key={key}"
        response = await self.bot.api.get(
            searchurl.format(query=query, key=self.settings["api_key"]))
        ytjson = await response.json()
        videoid = ytjson["items"][0]["id"]["videoId"]
        title = ytjson["items"][0]["snippet"]["title"]
        return {"title": title, "video_id": videoid}

    @makeCommand(name="yt", description="<query | url> play youtube")
    async def playyt(self, c: Command):
        print(c.message)
        if re.match("youtube(.be\/|.com\/watch\?)", c.message):
            ytid = re.search("(?:v=|\.be\/)(.{11})", c.message)[1]
            lazylook = await self.ytsearch(ytid)
            await self.play(video_id=ytid, title=lazylook["title"])
        else:
            ytinfo = await self.ytsearch(c.message)
            print(ytinfo)
            await self.play(video_id=ytinfo["video_id"],
                            title=ytinfo["title"])

    @makeCommand(name="rm", description="")
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

    @makeCommand(name="pl", description="append a youtube to play to jumpin's")
    async def addplaylist(self, c: Command):
        pass

    @event(event="client::error")
    async def error(self, err: JumpinError):
        if err.message == "Error starting Youtube video":
            await self.send_message(
                "Jumpin's quota has been reached :sob:",
                color=Colors.red, style=Styles.bold
            )
