import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class JumpinObject:
    def __init__(self):
        self.__jumpin_object__ = True

    def __post_init__(self):
        _routes = {
            "dimensions": Dimensions,
            "user": User,
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


@dataclass
class User(JumpinObject):
    userIcon: None
    assignedBy: None
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


@dataclass
class Session:
    token: str
    user: User


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
class Message:
    message: str
    handle: str = ""
    color: str = "green"
    userId: str = "8675309"
    timestamp: str = time.time().__str__()
    id: str = "00000"

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
    timestamp: str
    context: str
    message: str

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


@dataclass()
class UpdateUserList(JumpinObject):
    user: User


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
class UserList(JumpinObject):
    _id: str
    name: str
    attrs: Attrs = None
    settings: Settings = None
    users: List[User] = field(default_factory=User)


class BotState(Enum):
    INITIALIZED = 0
    RUNNING = 1
    DISCONNECT = 2
    EXCEPTION = 3
