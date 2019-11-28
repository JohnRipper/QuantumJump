from util import get_current_sha1 #, get_latest_sha1
from lib.cog import Cog
from lib.command import makeCommand, Command
from datetime import datetime


class Builtins(Cog):
    @makeCommand(name="version", description="get the current version")
    async def version(self, c: Command):
        message = ":crystal_ball: currently using: *{}* | Latest is: *{}*".format(
            get_current_sha1(),
            "N/A"
            # cant hit API till repo is public
            # await get_latest_sha1()
        )
        await self.send_message(message)

    @makeCommand(name="uptime", description="get the bot's uptime")
    async def uptime(self, c: Command):
        current = datetime.now()
        start = datetime.fromtimestamp(self.bot.start_time)
        difference = str(current - start)
        print(difference)
        print(difference[:-7])
        # strip after the decimal
        message = ":stopwatch: current uptime is {}".format(
            str(difference)[:7].replace(":", ";"))
        await self.send_message(message)
