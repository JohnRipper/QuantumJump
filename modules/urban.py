import re

import aiohttp

from lib.cog import Cog
from lib.command import Command, makeCommand


class Urban(Cog):
    base_url = "https://api.urbandictionary.com/v0/define?term={}"

    async def urban_lookup(self, query: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url.format(query)) as response:
                if response.status != 200:
                    definition = f"Got {response.status} from Urban Dictionary's API"
                else:
                    try:
                        urbjson = await response.json()
                        _definition = urbjson["list"][0]["definition"].strip(
                        ).replace("  ", " ")
                        definition = re.sub(r"\[*\]*", "", _definition).replace("\n", " ").replace("\r", " ")
                    except (IndexError, KeyError):
                        definition = f"Couldn't find anything for {query}"
                return definition

    @makeCommand(name="urb", description="Search Urban Dictionary")
    async def do_urban(self, c: Command):
        if len(c.message) == 0:
            response = "Need a term to lookup"
        else:
            response = await self.urban_lookup(c.message)
        await self.send_message(f"*{c.message}:* {response}")
