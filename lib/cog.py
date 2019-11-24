from lib.objects import Status, User, Session, HandleChange, Message


class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.bot = bot
        self.settings = bot.settings

    #####
    # client control
    ######
    def send_message(self, message: str, room=None):
        if not room:
            room = self.settings.bot.room
        data = [
            "room::message",
            {
                "message": message,
                "room": room
            }
        ]
        self.ws_send(data=data)

    def ws_send(self, data: list):
        data = f"42{data}"
        pass

    #####
    # Jumpin Commands
    #####
    def get_ignore_list(self, room: str):
        data = [
            "room::getIgnoreList",
            {
                "roomName": room
            }
        ]
        self.ws_send(data=data)

    def kick(self, user_id: str):
        data = [
            "room::operation::kick",
            {
                "user_list_id": user_id
            }
        ]
        self.ws_send(data=data)

    def banlist(self):
        data = [
            "room::operation::banlist",
            {
                "user_list_id": self.bot.api.session.user.user_id
            }
        ]
        self.ws_send(data=data)

    def ban(self, user_id: str, duration: int = 24):
        # perm is 4464
        data = [
            "room::operation::ban",
            {
                "user_list_id": user_id,
                "duration": duration
            }
        ]
        self.ws_send(data=data)

    def unban(self, ban_id: str, handle: str):
        data = [
            "room::operation::unban",
            {
                "banlistId": ban_id,
                "handle": handle
            }
        ]
        self.ws_send(data=data)

    def do_youtube(self):
        pass

    def handle_change(self, nick: str):

        data = [
            "room::handleChange",
            {
                "handle": nick
            }
        ]
        self.ws_send(data=data)

    def is_still_joined(self, room: str = None):
        if not room:
            room = self.settings.bot.room
        data = [
            "room::isStillJoined",
            {
                "room": room
            }
        ]

        self.ws_send(data=data)

    def join(self, room: str = None):
        if not room:
            room = self.settings.bot.room
        data = ["room::join", {"room": room}]
        self.ws_send(data=data)

    def close_broadcast(self, user_id: str):
        data = [
            "room::operation::closeBroadcast",
            {
                "user_list_id": user_id
            }
        ]
        self.ws_send(data=data)

    def do_pm(self):
        pass

    #####
    # Events
    #####

    def updateUser(self, user: User):
        pass

    def updateIgnore(self, ignore_list: list):
        pass

    def status(self, status: Status):
        pass

    def handleChange(self, handleChange: HandleChange):
        pass

    def message(self, message: Message):
        pass