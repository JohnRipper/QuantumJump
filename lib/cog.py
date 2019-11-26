import importlib
from asyncio import Protocol
from dataclasses import dataclass, field
from imp import reload
from types import ModuleType
from typing import List

from lib.objects import Status, User, HandleChange, Message, UpdateUserList


def event(event: str, **attrs):
    def wrap(f: classmethod):
        f.__jumpin_event__ = True
        f.__event__ = event
        return f

    return wrap


class Cog():
    def __init__(self, bot):
        self.bot = bot
        self.name = self.__class__.__name__
        self.__cog__ = True
        self.settings = bot.settings
        self.registered_events = []
        self.events = [getattr(self, name)  # what gets stored.
                       for name in dir(self)  # loop
                       if "__" not in name  # ignore builtins
                       and callable(getattr(self, name))  # is callable
                       and hasattr(getattr(self, name), "__event__")
                       ]

        self.commands = [getattr(self, name)  # what gets stored.
                       for name in dir(self)  # loop
                       if "__" not in name  # ignore builtins
                       and callable(getattr(self, name))  # is callable
                       and hasattr(getattr(self, name), "__command__")
                       ]

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

    def checkisplaying(self, notify: bool = True):
        data = [
            "youtube::checkisplaying",
            {
                "notify": notify
            }
        ]
        self.ws_send(data=data)

    def play(self, video_id: str, title: str):
        data = [
            "youtube::play",
            {
                "videoId": video_id,
                "title": title
            }
        ]
        self.ws_send(data=data)

    def remove(self, id: str):
        data = [
            "youtube::remove",
            {
                "id": id
            }
        ]
        self.ws_send(data=data)

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

    def __repr__(self) -> str:
        return self.name

    # these dont actually need to be here anymore.
    @event(event="room::updateUser")
    async def updateUser(self, user: User):
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UpdateUserList):
        print("this" + userlist.user.username)
        pass

    @event(event="room::updateIgnore")
    async def updateIgnore(self, ignore_list: list):
        pass

    @event(event="room::status")
    async def status(self, status: Status):
        pass

    @event(event="room::handleChange")
    async def handleChange(self, handle_change: HandleChange):
        pass

    @event(event="room::message")
    async def message(self, message: Message):

        pass

    @event(event="room::error")
    async def error(self, message):
        print(message)
        pass

    @event(event="room::alert")
    async def alert(self, message):
        print(message)
        pass

@dataclass
class CogManager:
    modules: dict = field(default_factory=dict)
    cogs: dict = field(default_factory=dict)

    def import_module(self, module: str) -> ModuleType:
        # attempt to reload if already loaded
        for mod in self.modules:
            if mod == f"{module}":
                return reload(module)
        # not loaded? try loading.
        m = importlib.import_module(f"modules.{module}".lower())
        self.modules.update({module: m})
        return m

    def load_all(self, module_list: [str], bot):
        for module in module_list:
            m = self.import_module(module)
            self.add_cog(m, module, bot)

    def add_cog(self, mod: ModuleType, name: str, bot):
        cog = getattr(mod, name)
        self.cogs.update({name: cog(bot)})

    def unload(self, module: str):
        if module in self.cogs.keys():
            self.cogs.pop(module)

    def get_cog(self, module: str) -> Cog:
        if module in self.cogs.keys:
            return self.cogs.get(module)

    async def do_event(self, data: dict = None):
        # trigger event for all cogs
        for cog in self.cogs.values():
            for meth in cog.events:
                print(f"{meth.__event__} {data[0]}")
                if meth.__event__ == data[0]:
                    print("in here")
                    # this
                    routes = {
                        "room::updateUserList": UpdateUserList,
                    }

                    if choice := routes.get(data[0]):
                        await meth( choice(**data[1]))
                    # or this.  hardcoded


    def do_command(self, x: Cog, command: str, data: dict = None):
        pass
