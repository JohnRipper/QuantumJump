from lib.cog import Cog, event
from lib.objects import User, Status, HandleChange, Message, UpdateUserList


class Debug(Cog):

    #####
    # Events
    #####
    def updateUser(self, user: User):
        pass

    def updateIgnore(self, ignore_list: list):
        pass

    def status(self, status: Status):
        pass

    def handleChange(self, handle_change: HandleChange):
        pass

    def message(self, message: Message):
        print(message.message)
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UpdateUserList):
        print("that" + userlist.user.username)
        pass
