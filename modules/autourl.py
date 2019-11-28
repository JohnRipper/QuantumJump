import re

import aiohttp
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog, event
from lib.objects import Message


class Autourl(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        # self.settings = self.bot.settings["module"]["autourl"]
        # self.pattern = self.settings["pattern"]
        # self.exclusion_char = self.settings["exclusion_char"]
        self.exclusion_char = "!"

    @event("room::message")
    async def message(self, message: Message):
        msg = message.message
        match = re.findall(r"http.*\S", msg)
        # workaround for youtube playing
        if re.match(r"\A.?yt", msg):
            pass
        elif msg.startswith(self.exclusion_char) or len(match) == 0:
            pass
        else:
            if self.ignore_msg(match[0]) is False:
                title = await self.get_title(match[0])
                if title:
                    await self.send_message(title)

    def ignore_msg(self, msg):
        ignores = ["jumpin.chat", "jumpinchat.com"]
        for each in ignores:
            if re.search(each, msg):
                return True
            else:
                return False

    async def get_title(self, url):
        url = url.strip()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = bs4(text, "html.parser")
                    if soup is not None:
                        try:
                            title = soup.title.string
                        except AttributeError as error:
                            pass
                        else:
                            return title.strip()
