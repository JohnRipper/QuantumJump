# -*- coding: utf-8 -*-
#
# Copyright 2019, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 2/8/20
# This file is part of QuantumJump.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import asyncio
import importlib
import re
from dataclasses import dataclass, field
from imp import reload
from types import ModuleType

from lib.command import Command
from lib.logging import QuantumLogger
from lib.objects import HandleChange, Message, Status, User, JumpinError, Banlist, UserList, PlaylistUpdate
from lib.styling import Colors, encodetxt


def event(event: str, **attrs):
    def wrap(f: classmethod):
        f.__jumpin_event__ = True
        f.__event__ = event
        return f
    return wrap


class Cog:
    def __init__(self, bot):
        self.bot = bot
        self.name = self.__class__.__name__
        self.__cog__ = True
        self.log = QuantumLogger(self.name, self.bot.room)
        self.log.info(f"initializing cog")
        self.bot_settings = bot.botconfig
        self.settings = bot.settings.Modules.get(self.__class__.__name__, None)

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
    async def ws_send(self, data):
        await self.bot.wsend(data=data)

    async def send_message(self, message: str, room: str = None, color=None, style=None):
        if not room:
            room = self.bot_settings.roomname

        if color is None and self.bot_settings.rainbow:
            color = Colors.random()
            await self.change_color(color)
        elif color is not None:
            await self.change_color(color)

        if len(message) > 254:
            # re.DOTALL makes . match everything, including newline
            messages = re.findall("(.{1,254}[.,;:]|.{1,254})", message, re.DOTALL)
            chunk_limit = self.bot_settings.chunk_limit
            if chunk_limit == 0 or chunk_limit == None:
                chunk_limit = len(messages)
            for i in range(0, chunk_limit):
                message = messages[i][:254]
                if style is not None:
                    message = encodetxt(message, style)
                await self.send_message(message, room=room, color=color, style=style)
            return
        else:
            if style is not None:
                # TODO check if valid style
                message = encodetxt(message, style)
            data = [
                "room::message",
                {
                    "message": message,
                    "room": room
                }
            ]
            await self.ws_send(data=data)

    async def send_action(self, message: str, room: str = None, color=None, style=None):
        """/me messages, styling doesn't work"""
        if color is None and self.bot_settings.rainbow:
            color = Colors.random()
            await self.change_color(color)
        elif color is not None:
            await self.change_color(color)
        if style is not None:
            # TODO check if valid style
            message = encodetxt(message, style)
        if not room:
            room = self.bot_settings.roomname
        data = [
            "room::command",
            {
                "message": {
                    "command": "me",
                    "value": message
                },
                "room": room
            }
        ]
        await self.ws_send(data=data)

    #####
    # Jumpin Commands
    #####
    async def remove_yt(self, id):
        data = ["youtube::remove", {"id": id}]
        await self.ws_send(data=data)

    async def checkisplaying(self, notify: bool = True):
        data = [
            "youtube::checkisplaying",
            {
                "notify": notify
            }
        ]
        await self.ws_send(data=data)

    async def play(self, video_id: str, title: str):
        data = [
            "youtube::play",
            {
                "videoId": video_id,
                "title": title
            }
        ]
        await self.ws_send(data=data)

    async def remove(self, id: str):
        data = [
            "youtube::remove",
            {
                "id": id
            }
        ]
        await self.ws_send(data=data)

    async def get_ignore_list(self, room: str):
        data = [
            "room::getIgnoreList",
            {
                "roomName": room
            }
        ]
        await self.ws_send(data=data)

    async def kick(self, user_id: str):
        data = [
            "room::operation::kick",
            {
                "user_list_id": user_id
            }
        ]
        await self.ws_send(data=data)

    async def banlist(self):
        data = [
            "room::operation::banlist",
            {
                "user_list_id": self.bot.api.session.user.user_id
            }
        ]
        await self.ws_send(data=data)

    async def ban(self, user_id: str, duration: int = 24):
        # perm is 4464
        data = [
            "room::operation::ban",
            {
                "user_list_id": user_id,
                "duration": duration
            }
        ]
        await self.ws_send(data=data)

    async def unban(self, ban_id: str, handle: str):
        data = [
            "room::operation::unban",
            {
                "banlistId": ban_id,
                "handle": handle
            }
        ]
        await self.ws_send(data=data)

    async def handle_change(self, nick: str):
        data = [
            "room::handleChange",
            {
                "handle": nick
            }
        ]
        await self.ws_send(data=data)

    async def change_color(self, color: str):
        data = [
            "room::changeColor",
            {
                "color": color
            }
        ]
        await self.ws_send(data=data)

    async def is_still_joined(self, room: str = None):
        if not room:
            room = self.bot_settings.roomname
        data = [
            "room::isStillJoined",
            {
                "room": room
            }
        ]

        await self.ws_send(data=data)

    async def join(self, room: str = None):
        if not room:
            room = self.bot_settings.roomname
        data = ["room::join", {"room": room}]
        await self.ws_send(data=data)

    async def close_broadcast(self, user_id: str):
        data = [
            "room::operation::closeBroadcast",
            {
                "user_list_id": user_id
            }
        ]
        await self.ws_send(data=data)

    async def do_pm(self):
        pass

    def __repr__(self) -> str:
        return self.name

    # these dont actually need to be here anymore.
    # left for reference
    @event(event="room::updateUser")
    async def updateUser(self, user: User):
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UserList):
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
        pass

    @event(event="room::alert")
    async def alert(self, message):
        pass


    @event(event="youtube::playlistUpdate")
    # 42["youtube::playlistUpdate",[{"startTime":null,"endTime":null,"description":null,"channelId":"UCqukXrA3L_B0EVHiM14EU7g","pausedAt":null,"_id":"5dea8a123533d70008b01aa9","mediaId":"jesc3yvZSws","title":"DANZIG - Mother Lyrics","link":"https://youtu.be/jesc3yvZSws","duration":226,"thumb":"https://i.ytimg.com/vi/jesc3yvZSws/default.jpg","mediaType":"TYPE_YOUTUBE","startedBy":"5c4b7b6746bb1a000712c13c","createdAt":"2019-12-06T17:04:18.334Z"}]]
    async def playlistUpdate(self, playlistUpdate: list):
        pass


@dataclass
class CogManager:
    modules: dict = field(default_factory=dict)
    cogs: dict = field(default_factory=dict)

    @property
    def all_commands(self) -> dict:
        cl = {}
        for cog in self.cogs.values():
            for command in cog.commands:
                for name in command.__command_name__:
                    cl.update({name: command.__description__})
        return cl

    def igetattr(self, obj, attr):
        # just don't have modules with same spelling and different capitalization.
        for a in dir(obj):
            if a.lower() == attr.lower():
                return getattr(obj, a)

    def import_module(self, module: str, bot) -> ModuleType:
        # attempt to reload if already loaded
        if mod := self.modules.get(module.lower(), False):
            self.unload(module)
            if m := reload(mod):
                self.modules.update({module.lower(): m})
                self.add_cog(mod=m, name=module, bot=bot)
        # not loaded? try loading.
        try:
            m = importlib.import_module(f"modules.{module}".lower())
            self.modules.update({module.lower(): m})
            return m
        except ModuleNotFoundError as e:
            print(e)

    def load_all(self, module_list: [str], bot):
        for module in module_list:
            m = self.import_module(module, bot)
            self.add_cog(m, module, bot)

    def add_cog(self, mod: ModuleType, name: str, bot):
        cog = self.igetattr(mod, name)(bot)
        self.cogs.update({name.lower(): cog})

    def unload(self, module: str) -> bool:
        if module in self.cogs.keys():
            self.cogs.pop(module.lower())
            return True
        return False

    def get_cog(self, module: str) -> Cog:
        if module in self.cogs.keys:
            return self.cogs.get(module.lower())

    def get_module(self, module: str) -> Cog:
        if module in self.cogs.keys:
            return self.modules.get(module.lower())


    async def do_event(self, data: list):
        for cog in self.cogs.values():
            for meth in cog.events:
                if meth.__event__ == data[0]:
                    routes = {
                        "room::updateUserList": UserList,
                        "room::message": Message,
                        "client::error": JumpinError,
                        "youtube::playlistUpdate": PlaylistUpdate,
                        "room::operation::ban": Banlist
                    }
                    if choice := routes.get(data[0], False):
                        if type(data[1]) is dict:
                            asyncio.create_task(meth(choice(**data[1])))
                        elif type(data[1]) is list:
                            asyncio.create_task(meth(choice(data[1])))

    async def do_command(self, command: Command) -> bool:
        found = False
        for cog in self.cogs.values():
            for meth in cog.commands:
                if command.name in meth.__command_name__:
                    if meth.__restricted__:
                        if command.sender.role >= meth.__role__:
                            asyncio.create_task(meth(command))
                    else:
                        asyncio.create_task(meth(command))
                    # command found.
                    return True
        if not found:
            return False
