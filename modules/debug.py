from lib.cog import Cog, event
from lib.command import makeCommand, Command
from lib.objects import User, Status, HandleChange, Message, UpdateUserList


class Debug(Cog):

    #####
    # Events
    #####

    @makeCommand(name="test",description= "test")
    async def vagina(self, c: Command):
        print("test")

        await self.send_message("titty")

    @event(event="room::message")
    def message(self, message: Message):
        print(message.message)
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UpdateUserList):
        print("that" + userlist.user.username)
        pass
