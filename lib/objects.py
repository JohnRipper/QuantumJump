from dataclasses import dataclass


@dataclass
class JumpinObject:

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
    user_id: str
    username: str
    isGold: None
    userIcon: None
    settings: Settings = None
    videoQuality: VideoQuality = None
    isAdmin: bool = False
    isSiteMod: bool = False
    isSupporter: bool = False




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
    pass

@dataclass
class Message:
    pass