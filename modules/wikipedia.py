import asyncio
import re

import wikipedia
from lib.cog import Cog
from lib.command import Command, makeCommand


class Wikipedia(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.searches = []

    @makeCommand(aliases=["wikilang"], description="Set Wikipedia's language")
    async def wiki_lang(self, c: Command):
        if len(c.message) == 2:
            await self.send_action(f"sets Wikipedia's language to {c.message}")
            self.settings["language"] = c.message
        else:
            await self.send_message("Need the 2 letter code, get it from http://dpaste.com/2WC4YXT.txt")

    @makeCommand(aliases=["wiki"], description="query|none return a wikipedia summary")
    async def wiki_lookup(self, c: Command):
        wikipedia.set_lang(self.settings["language"])
        # sentences = self.settings["sentences"]
        query = c.message
        # expected response for choosing a topic from `self.searches`
        if len(query) == 1 and query.isdigit():
            query = self.searches[int(query)]
        elif len(query) == 0:
            query = wikipedia.random(pages=1)
        try:
            page = wikipedia.page(query)
            summary = wikipedia.summary(query,
                                        sentences=self.settings["sentences"])
        except wikipedia.exceptions.PageError:
            await self.send_message("PageError, FIXME")
        except wikipedia.exceptions.DisambiguationError as err:
            self.searches = err.options[:4]
            # iterate over self.searches to create a formated string,
            # ie "0) List Index 0, 1) List Index 1, " etc
            # TODO, this doesn't work great
            fmtd = ", ".join(
                [str(i) + ") " + m for i, m in enumerate(self.searches)])
            message = "Select one with '{}wiki #' {}".format(
                self.bot_settings.prefix, fmtd)
            await self.send_message(message)
        else:
            # wikipedia lib reformats headings? yuck.
            summary = re.sub("==.+==", " ", summary)
            summary = re.sub("\n", "", summary)
            # TODO maybe pull this limit from the settings
            await self.send_message(summary)
            if self.settings["include_url"]:
                await asyncio.sleep(0.5)
                await self.send_message(page.url)
