from dataclasses import dataclass
# ["room::join",{"room":"tech",
# "user":{"user_id":"5c4b7b6746bb1a000712c13c",
# "username":"johnripper",
# "isAdmin":false,
# "isSiteMod":false,
# "isSupporter":false,"isGold":null,
# "userIcon":null,
# "settings":{"playYtVideos":false,"allowPrivateMessages":true,"pushNotificationsEnabled":false,"receiveUpdates":false,"receiveMessageNotifications":true,
# "darkTheme":true,"videoQuality":"VIDEO_240","userIcon":null,"ignoreList":[]},"videoQuality":{"id":"VIDEO_240","label":"240p","dimensions":{"width":320,"height":240},"frameRate":15,"bitRate":128000}}}]
@dataclass
class Dimensions:
    width: int
    height: int


@dataclass
class VideoQuality:
    id: str
    label: str
    dimensions: Dimensions
    frameRate: int
    bitRate: int


@dataclass
class Settings:
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
class User:
    user_id: str
    username: str
    isGold: None
    userIcon: None
    settings: Settings
    isAdmin: bool = False
    isSiteMod: bool = False
    isSupporter: bool = False


@dataclass
class SelfBot:
    user: User
    token: str


@dataclass
class Room_Join:
    user: User
    room: str = ""
