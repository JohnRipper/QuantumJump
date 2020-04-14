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

import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class JumpinObject:
    def __post_init__(self):
        _routes = {
            "dimensions": Dimensions,
            "userlist": UserList,
            "user": User,
            "sender": User,
            "settings": Settings,
            "videoQuality": VideoQuality,
            "attrs": Attrs,
            "topic": Topic,
            "updatedBy": UpdatedBy
        }
        for attr in self.__dict__:
            cheddar = getattr(self, attr)
            if type(cheddar) is dict:
                setattr(self, attr, _routes.get(attr)(**cheddar))


@dataclass
class Dimensions(JumpinObject):
    width: int
    height: int


@dataclass
class VideoQuality(JumpinObject):
    dimensions: Dimensions = None
    id: str = None
    label: str = None
    frameRate: int = None
    bitRate: int = None


@dataclass
class Settings(JumpinObject):
    playYtVideos: bool
    allowPrivateMessages: bool
    pushNotificationsEnabled: bool
    receiveUpdates: bool
    receiveMessageNotifications: bool
    darkTheme: bool
    videoQuality: str
    userIcon: None
    ignoreList: dict


class Role(Enum):
    ROOM_OWNER = 100
    MOD = 75
    OP = 50
    LOGGED_IN = 25
    GUEST = 10
    SITE_OWNER = 0


@dataclass
class User(JumpinObject):
    userIcon: str = None
    assignedBy: str = None
    operator_id: str = None
    handle: str = None
    user_id: str = None
    username: str = None
    _id: str = None
    color: str = None
    settings: Settings = None
    videoQuality: VideoQuality = None
    isAdmin: bool = False
    isSiteMod: bool = False
    isSupporter: bool = False
    isBroadcasting: bool = False
    isGold: bool = False
    timestamp: str = None
    roles: str = None

    @property
    def is_mod(self):
        if self.operator_id is not None and self.assignedBy is None:
            return True
        else:
            return False

    @property
    def is_op(self):
        # TODO ROOM OPS
        if self.operator_id is not None and self.assignedBy is not None:
            return True
        else:
            return False

    @property
    def role(self) -> Role:
        role: Role = Role.GUEST

        if self.isAdmin:
            role = Role.SITE_OWNER

        if self.isSiteMod:
            role = Role.SITE_MOD

        if self.is_mod:
            role = Role.MOD

        if self.is_op:
            role = Role.OP

        if self.isSupporter or self.isGold:
            role = Role.SUPPORTER

        return role


@dataclass
class Session:
    token: str
    user: User = None


@dataclass
class Status:
    message: str
    timestamp: str
    id: str
    notification_type: str = None


@dataclass
class Join:
    user: User
    room: str = ""


@dataclass
class HandleChange:
    userId: str
    handle: str


@dataclass
class Message(JumpinObject):
    message: str
    handle: str = ""
    color: str = "green"
    userId: str = "8675309"
    timestamp: str = time.time().__str__()
    id: str = "00000"
    sender: User = None

    def json(self):
        return json.dumps(self.__dict__)

    def jumpson(self):
        # mimics a server side message to recycle the code in _recv as a terminal based command processor
        return f"42[\"room::message\",{self.json()}]"

    @staticmethod
    def makeMsg(message: str, room: str) -> str:
        # use this for making messages to use for wsend
        data = [
            "room::message",
            {
                "message": message,
                "room": room
            }
        ]
        return f"42{json.dumps(data)}"


@dataclass
class JumpinError:
    context: str
    message: str = None
    timestamp: str = None
    modal: str = None
    id: str = None
    error: str = None

@dataclass
class PlaylistUpdate:
    startTime: str = None
    endTime: str = None
    description: str = None
    channelId: str = None
    pausedAt: str = None
    _id: str = None
    mediaId: str = None
    title: str = None
    link: str = None
    duration: str = None
    thumb: str = None
    mediaType: str = None
    startedBy: str = None
    createdAt: str = None


@dataclass
class PlayVideo(JumpinObject):
    startTime: str = None
    endTime: str = None
    description: str = None
    channelId: str = None
    pausedAt: str = None
    _id: str = None
    mediaId: str = None
    title: str = None
    link: str = None
    duration: str = None
    thumb: str = None
    mediaType: str = None
    startedBy: dict = None
    createdAt: str = None


@dataclass
class BanListItem:
    _id: str
    handle: str
    timestamp: str


@dataclass
class Banlist:
    list: List[BanListItem]


@dataclass
class HandleChange:
    handle: str



@dataclass
class Attrs(JumpinObject):
    owner: str
    janus_id: int
    fresh: bool
    ageRestricted: bool


@dataclass
class UpdatedBy(JumpinObject):
    _id: str
    username: str


@dataclass
class Topic(JumpinObject):
    text: str
    updatedAt: str
    updatedBy: UpdatedBy = None


@dataclass
class Settings(JumpinObject):
    public: bool
    modOnlyPlayMedia: bool
    forcePtt: bool
    forceUser: bool
    description: str
    display: str
    requiresPassword: bool
    topic: Topic = None

@dataclass
class PlaylistUpdateItem(JumpinObject):
    startTime:str = None
    endTime: str = None
    description: str = None
    channelId:str = None
    pausedAt:str = None
    _id:str = None
    mediaId:str = None
    title:str = None
    duration:str = None
    thumb:str = None
    mediaType: str = None
    startedBy: str = None
    createdAt: str = None



@dataclass
class PlaylistUpdate(List[PlaylistUpdateItem]):
    objects: List[PlaylistUpdateItem] = field(default_factory=PlaylistUpdateItem)
    def __init___(self, data: list):
        for object in data:
            self.objects.append(PlaylistUpdateItem(**object))

@dataclass
class UserList(JumpinObject):
    # _id: str = None
    # name: str = None
    # attrs: Attrs = None
    # settings: Settings = None
    user: User = None
    users: List[User] = field(default_factory=User)

    def add(self, user: User):
        #update the list and return, else add to the list
        if not isinstance(self.users, list):
            self.users = []
        for pos, item in enumerate(self.users):
            if user.user_id == item.user_id:
                self.users[pos] = user
                return
        self.users.append(user)

    def update(self, user: User) -> bool:
        if not isinstance(self.users, list):
            self.users = []
        if user:
            for pos, item in enumerate(self.users):
                if user.user_id == item.user_id:
                    self.users[pos] = user
                    return True
            self.users.append(user)
            return False

    def handle_name_change(self, user_id: str, handle: str) -> bool:
        if not isinstance(self.users, list):
            self.users = []
        for pos, item in enumerate(self.users):
            if user_id == item.user_id:
                self.users[pos].handle = handle
                return True
        return False

    def remove(self, user: User):
        for pos, item in enumerate(self.users):
            if user.user_id == item.user_id:
                self.users.pop(pos)

    def get_by_handle(self, handle: str) -> User:
        if self.users:
            for user in self.users:
                if user.handle == handle:
                    return user

    def get_by_id(self, id: str) -> User:
        if self.users:
            for user in self.users:
                if user._id == id:
                    return user

class BotState(Enum):
    INITIALIZED = 0
    RUNNING = 1
    DISCONNECT = 2
    EXCEPTION = 3
