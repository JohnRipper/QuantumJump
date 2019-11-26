from dataclasses import dataclass, field
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
            "videoQuality": VideoQuality
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
    assignedBy : None
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
    handle: str
    color: str
    userId: str
    message: str
    timestamp: str
    id: str

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

    def __repr__(self):
        return self.user