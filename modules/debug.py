from lib.cog import Cog
from lib.objects import User, Status, HandleChange, Message


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
