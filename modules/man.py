import aiohttp
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog
from lib.command import makeCommand, Command


class Man(Cog):
    pass
    # async def getman(self, query: str):
    #     url = ""
    #     async with aiohttp.ClientSession() as session:

    # @makeCommand(aliases=["man"], description="Return a description from die.net")
    # async def manpage(self, c: Command):
    #     if c.message is None:
    #         await self.send_action("needs a query")
    #     else:
    #         searched = await self.getman(c.message)
    #         if searched is None:
    #             await self.send_action(f"couldn't find {c.message}")
    #         elif self.settings["justname"] is True:
    #             name = searched["NAME"]
    #             await self.send_message(name)
    #         else:
    #             description = searched["DESCRIPTION"]
    #             await self.send_message(description)

