import aiohttp

from lib.cog import Cog
from lib.command import makeCommand, Command


class Chuck(Cog):
    @makeCommand(aliases=["cn", "chuck"], description="Random Chuck Norris joke.")
    async def chucknorris(self, c: Command):
        url = "https://api.chucknorris.io/jokes/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await self.send_message(f"Got {response.status} from chucknorris.io.")
                else:
                    try:
                        cnjson = await response.json()
                        await self.send_action(cnjson["value"])
                    except (IndexError, KeyError) as e:
                        await self.send_message("Error while parsing the json.")
