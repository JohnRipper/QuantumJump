import json

from lib.cog import Cog, event
from lib.command import makeCommand, Command
from lib.objects import User, Status, HandleChange, Message, UpdateUserList
from lib.styling import Colors, Styles, encodetxt


class Debug(Cog):

    #####
    # Events
    #####
    @makeCommand(name="userlist", description="test")
    async def vagina(self, c: Command):
        await self.send_message(json.dumps(await self.bot.userlist))
        #await self.send_message("Test")

    @makeCommand(name="me", description="t")
    async def thirdperson(self, c: Command):
        await self.send_action(c.message)

    @makeCommand(name="font", description="")
    async def demofonts(self, c: Command):
        parts = c.message.split(" ")
        type_ = parts[0]
        message = " ".join(parts[1:])
        if type_ in Styles.__dict__.keys():
            formated = encodetxt(message, Styles.__dict__[type_])
        else:
            formated = encodetxt(c.message, Styles.script)
        await self.send_message(formated)

    @event(event="room::message")
    async def message(self, message: Message):
        print(message.message)
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UpdateUserList):
        print("that" + userlist.user.handle)
        pass
