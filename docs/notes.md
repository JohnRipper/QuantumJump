- [WS Events](#sec-1)
  - [Room Events](#sec-1-1)
    - [Send](#sec-1-1-1)
    - [Receive](#sec-1-1-2)
  - [Youtube Events](#sec-1-2)
    - [Send](#sec-1-2-1)
    - [Receive](#sec-1-2-2)
  - [Client Events](#sec-1-3)
    - [Receive](#sec-1-3-1)
  - [Self Events](#sec-1-4)
    - [Receive](#sec-1-4-1)
- [API](#sec-2)
  - [Youtube](#sec-2-1)
    - [Playlist](#sec-2-1-1)
    - [Search DEPRECATED](#sec-2-1-2)
  - [Room](#sec-2-2)
    - [Users](#sec-2-2-1)
    - [Unread](#sec-2-2-2)
    - [Profile](#sec-2-2-3)
    - [Emoji](#sec-2-2-4)
    - [Room Settings](#sec-2-2-5)
    - [Broadcast Options](#sec-2-2-6)
    - [Room Roles](#sec-2-2-7)
    - [Session](#sec-2-2-8)

### Some notes on IDs
In most if not all cases `_id` is the "user_list_id", that's the key used for sending ban messages so we might aswell call it that's

The `user_id` is the ID for account

`operator_id` This exists only if the user is a moderator, so we can do

```py
if User.operator_id:
    do_a_thing()
```
Side note: `assignedBy` is treated the same, but for oper. If it's empty, the user is not oper. (half star thing)

There is also a unique id for unbanning, retrieved from `42["room::operation::banlist",{"user_list_id":""}]`

AND youtube videos get an id which are unique per item in playlist, no matter if duplicated.

### More notes on things


If/when jumpin sorts out cloudflare, port [cfscrape](https://github.com/Anorov/cloudflare-scrape/blob/master/cfscrape/__init__.py) to aiohttp, maybe use pyjs to exec the javascript challenge instead of node.

Text formatting: \***bold**\* \__italic_\_
# WS Events<a id="sec-1"></a>

Initial connection is sending `2probe` and receiving `3probe` then sending `5`. Ping interval is sending `2` every 25 seconds; expecting `3` as response.

## Room Events<a id="sec-1-1"></a>

### Send<a id="sec-1-1-1"></a>

1.  `room::getIgnoreList`

    Response: `room::updateIgnore`
    
    ```json
    42[
      "room::getIgnoreList",
      {
        "roomName": "<ROOM>"
      }
    ]
    ```
1. `room::ignoreUser`
    
    Response: `room::status`, `room::updateIgnore`
    
    ```json
    42[
      "room::ignoreUser",
      {
        "userListId": "",
        "roomName": "<ROOM>"
      }
    ]
    ```
1. `room::unignoreUser`
    
    Response: `room::status`, `room:updateIgnore`
    
    ```json
    42[
      "room::unignoreUser",
      {
        "id":""
      }
    ]
    ```

2.  `room::handleChange`

    Response: `client::handleChange`, `room::handleChange`, `room::status`
    
    ```json
    42[
      "room::handleChange",
      {
        "handle": "<NICK>"
      }
    ]
    ```

3.  `room::isStillJoined`

    Response: `client::stillConnected` Sent every 5 minutes
    
    ```json
    42[
      "room::isStillJoined",
      {
        "room": "<ROOM>"
      }
    ]
    ```

4.  `room::join`

    Generated from POST to session API
    
    Response: `room::updateUserList`, `self::join` (maybe?)
    
    ```json
    42[
      "room::join",
      {
        "room": "<ROOM>",
        "user": {
          "user_id": "<USER ID>", 
          "username": "<USERNAME>",
          "isAdmin": false,
          "isSiteMod": false,
          "isSupporter": false,
          "isGold": null,
          "userIcon": null,
          "settings": {
            "playYtVideos": false,
            "allowPrivateMessages": true,
            "pushNotificationsEnabled": false,
            "receiveUpdates": false,
            "receiveMessageNotifications": true,
            "darkTheme": true,
            "videoQuality": "VIDEO_240",
            "userIcon": null,
            "ignoreList": [],
            "wideLayout": false
          },
          "videoQuality": {
            "id": "VIDEO_240",
            "label": "240p",
            "dimensions": {
              "width": 320,
              "height": 240
            },
            "frameRate": 15,
            "bitRate": 128000
          }
        }
      }
    ]
    ```

5.  `room::message`

    Response: `room::message`
    
    ```json
    42[
      "room::message",
      {
        "message": "<MESSAGE>",
        "room": "<ROOM>"
      }
    ]
    ```

6.  `room::operation::closeBroadcast`

    Response: `room::status`, `room::updateUser`
    
    ```json
    42[
      "room::operation::closeBroadcast",
      {
        "user_list_id": "<USER'S ID>"
      }
    ]
    ```

7.  `room::operation::ban`

    Response: `room::status`, `room:userbanned`, `room::disconnect`
     
    Duration is in hours? "permanent" ban is `duration: "4464"`

    
    ```json
    42[
      "room::operation::ban",
      {
        "user_list_id": "<USER ID>",
        "duration": "1"
      }
    ]
    ```

8.  `room::operation::banlist`

    Response `client::banlist`
    
    ```json
    42[
      "room::operation::banlist",
      {
        "user_list_id": "<SELF ID>"
      }
    ]
    ```

9.  `room::operation::kick`

    Response: `room::status` , `room::disconnect`
    
    ```json
    42[
      "room::operation::kick",
      {
        "user_list_id": "<USER ID>"
      }
    ]
    ```

10. `room::operation::unban`

    Response: `room::status`, `client::banlist`
    
    ```json
    42[
      "room::operation::unban",
      {
        "banlistId": "<BAN ID FROM client::banlist>",
        "handle": "<HANDLE FROM client::banlist>"
      }
    ]
    ```

11. `room::setUserIsBroadcasting`

    Response: `room::updateUser`
    
    ```json
    42[
      "room::setUserIsBroadcasting",
      {
        "isBroadcasting": true
      }
    ]
    ```

12. `room::command`
    Some of the commands: `me`, `topic`, `shrug`, `clear`
    Responses depend on command sent. 
    ```json
    42[
      "room::command",
      {
        "message": {
        "command": "<COMMAND>",
        "value": "<MESSAGE>"
        },
      "room": "<ROOM>"
      }
    ] 
    ```

### Receive<a id="sec-1-1-2"></a>

1.  `room::updateUser`

    ```json
    42[
      "room::updateUser",
      {
        "user": {
          "_id": "",
          "handle": "",
          "operator_id": DEPRECATED,
          "user_id": "",
          "username": "",
          "isBroadcasting": true,
          "assignedBy": null,
          "isAdmin": false,
          "isSiteMod": false,
          "isSupporter": false,
          "userIcon": null,
          "color": "green",
          "roles": [""]
        }
      }
    ]
    ```

2.  `room::updateIgnore`

    ```json
    42[
      "room::updateIgnore",
      {
        "ignoreList": []
      }
    ]
    ```

3.  `room::updateUserList`

    ```json
    42[
      "room::updateUserList",
      {
        "user": {
          "_id": "<ID?>",
          "handle": "addicted_profit",
          "operator_id": DEPRECATED,
          "user_id": "<USER ID>",
          "username": "aida",
          "isBroadcasting": false,
          "assignedBy": null,
          "isAdmin": false,
          "isSiteMod": false,
          "isSupporter": false,
          "userIcon": null,
          "color": "bluealt",
          "roles": [""]
        }
      }
    ]
    ```

4.  `room::status`

    ```json
    42[
      "room::status",
      {
        "message": "<MSG>",
        "timestamp": "<ISO 8601 UTC>",
        "id": "<UUID4>"
      }
    ]
    ```
    
    Or?
    
    ```json
    42[
      "room::status",
      {
        "notification_type": "room",
        "message": "<MSG>",
        "timestamp": "<ISO 8601 UTC>",
        "id": "<UUID4>"
      }
    ]
    ```
    
    TODO: log `notification_type`'s

5.  `room::handleChange`

    ```json
    42[
      "room::handleChange",
      {
        "userId": "<USER ID>",
        "handle": "<NICK>"
      }
    ]
    ```

6.  `room::disconnect`

    ```json
    42[
      "room::disconnect",
      {
        "user": {
          "_id": "<USER ID>",
          "handle": "<NICK>",
          "operator_id": DEPREICATED,
          "user_id": "",
          "username": "",
          "isBroadcasting": false,
          "assignedBy": null,
          "isAdmin": false,
          "isSiteMod": false,
          "isSupporter": false,
          "userIcon": null,
          "color": "red",
          "roles": [""]
        }
      }
    ]
    ```

7.  `room::message`

    ```json
    42[
      "room::message",
      {
        "handle": "<NICK>",
        "color": "redalt",
        "userId": "<USER ID>",
        "message": "<MESSAGE>",
        "timestamp": "<ISO 8601 UTC>",
        "id": "<UUID4>"
      }
    ]
    ```

## Youtube Events<a id="sec-1-2"></a>

### Send<a id="sec-1-2-1"></a>

1.  `youtube::checkisplaying`

    ```json
    42[
      "youtube::checkisplaying",
      {
        "notify": true
      }
    ]
    ```

2.  `youtube::play`

    ```json
    42[
      "youtube::play",
      {
        "videoId": "<YT ID>",
        "title": "<TITLE STR>"
      }
    ]
    ```

3.  `youtube::remove`

    id comes from API `/api/youtube/ROOM/playlist`
    
    ```json
    42[
      "youtube::remove",
      {
        "id": "<JUMPIN'S ASSIGNED ID>"
      }
    ]
    ```

### Receive<a id="sec-1-2-2"></a>

1.  `youtube::playlistUpdate`

    ```json
    42[
      "youtube::playlistUpdate",
      [
        {
          "startTime": null,
          "endTime": null,
          "description": null,
          "channelId": "<YT CHANNEL ID STR>",
          "pausedAt": null,
          "_id": "<JUMPIN'S VIDEO ID STR>",
          "mediaId": "<YT ID STR>",
          "title": "<YT TITLE STR>",
          "link": "<YT SHORT URL STR>",
          "duration": 240,
          "thumb": "<THUMBNAIL URL STR>",
          "mediaType": "TYPE_YOUTUBE",
          "startedBy": "<USER ID>",
          "createdAt": "<ISO 8601 UTC>"
        }
      ]
    ]
    ```

2.  `youtube::playvideo`

    ```json
    42[
      "youtube::playvideo",
      {
        "startTime": "<ISO 8601 UTC>",
        "endTime": "<ISO 8601 UTC + YT DURACTION>",
        "description": null,
        "channelId": "<YT CHANNEL ID STR>",
        "pausedAt": null,
        "createdAt": "<ISO 8601 UTC>",
        "_id": "<JUMPIN'S VIDEO ID STR>",
        "mediaId": "<YT ID STR>",
        "title": "<YT TITLE STR>",
        "link": "<YT SHORT URL STR>",
        "duration": 240,
        "thumb": "<THUMBNAIL URL STR",
        "mediaType": "TYPE_YOUTUBE",
        "startedBy": {
          "profile": {
            "pic": "user-avatar/avatar-blank.png"
          },
          "_id": "<USER ID>",
          "username": "<USER>"
        }
      }
    ]
    ```

## Client Events<a id="sec-1-3"></a>

### Receive<a id="sec-1-3-1"></a>

1.  `client::banlist`

    Includes global bans, no clear way to filter out
    
    ```json
    42[
      "client::banlist",
      {
        "list": [
          {
            "_id": "<BANLIST ID>",
            "handle": "<BANLIST HANDLE>",
            "timestamp": "<ISO 8601 UTC>"
          },
        ]
      }
    ]
    ```

2.  `client::stillConnected`

    ```json
    42[
      "client::stillConnected"
    ]
    ```

3.  `client::handleChange`

    ```json
    42[
      "client::handleChange",
      {
        "handle": "<OWN NICK>"
      }
    ]
    ```

## Self Events<a id="sec-1-4"></a>

### Receive<a id="sec-1-4-1"></a>

1.  `self::join`
    Received after `room::join`
    ```json
    42[
      "self::join",
      {
        "user": {
          "user_id": "<USER ID>",
          "operator_id": DEPRECATED,
          "assignedBy": null,
          "username": "<USERNAME>",
          "isBroadcasting": false,
          "isAdmin": false,
          "isSiteMod": false,
          "isSupporter": false,
          "userIcon": null,
          "_id": "<PUBLIC ID??>",
          "handle": "<TMP NICK>",
          "color": "bluealt",
          "createdAt": "<ISO 8601 UTC>",
          "joinTime": "<ISO 8601 UTC>",
          "roles": [""],
        }
      }
    ]
    ```

# API<a id="sec-2"></a>

Base URL: `https://jumpin.chat/api/`

## Youtube<a id="sec-2-1"></a>

### Playlist<a id="sec-2-1-1"></a>

Path: `youtube/<ROOM>/playlist`

Method: `GET`

Response:

```json
[
  {
    "startTime": "<ISO 8601 UTC>",
    "endTime": "<ISO 8601 UTC + DURATION>",
    "description": null,
    "channelId": "<YT CHANNEL ID STR>",
    "pausedAt": null,
    "createdAt": "<ISO 8601 UTC>",
    "_id": "<JUMPIN'S VIDEO ID>",
    "mediaId": "<YT ID STR>",
    "title": "<YT TITLE STR>",
    "link": "<YT SHORT LINK STR>",
    "duration": 240,
    "thumb": "<THUMBNAIL URL STR>",
    "mediaType": "TYPE_YOUTUBE",
    "startedBy": {
      "userId": "<USER ID>",
      "username": "<USER>",
      "pic": "user-avatar/avatar-blank.png"
    }
  }
]
```

### Search DEPRECATED<a id="sec-2-1-2"></a>

Path: `youtube/search/<QUERY>`

Method: `GET`

Response: (for query as "abc")

```json
[
  {
    "title": "ABC SONG | ABC Songs for Children - 13 Alphabet Songs &amp; 26 Videos",
    "videoId": "_UR-l3QI2nE",
    "thumb": {
      "url": "https://i.ytimg.com/vi/_UR-l3QI2nE/mqdefault.jpg",
      "width": 320,
      "height": 180
    },
    "channelId": "UCbCmjCuTUZos6Inko4u57UQ",
    "urls": {
      "video": "https://youtu.be/_UR-l3QI2nE",
      "channel": "https://youtube.com/channel/UCbCmjCuTUZos6Inko4u57UQ"
    }
  },
  {
    "title": "ABC Song + More Nursery Rhymes &amp; Kids Songs - CoCoMelon",
    "videoId": "71h8MZshGSs",
    "thumb": {
      "url": "https://i.ytimg.com/vi/71h8MZshGSs/mqdefault.jpg",
      "width": 320,
      "height": 180
    },
    "channelId": "UCbCmjCuTUZos6Inko4u57UQ",
    "urls": {
      "video": "https://youtu.be/71h8MZshGSs",
      "channel": "https://youtube.com/channel/UCbCmjCuTUZos6Inko4u57UQ"
    }
  },
  {
    "title": "ABC Song with Balloons | CoCoMelon Nursery Rhymes &amp; Kids Songs",
    "videoId": "RIQDmnIJZv8",
    "thumb": {
      "url": "https://i.ytimg.com/vi/RIQDmnIJZv8/mqdefault.jpg",
      "width": 320,
      "height": 180
    },
    "channelId": "UCbCmjCuTUZos6Inko4u57UQ",
    "urls": {
      "video": "https://youtu.be/RIQDmnIJZv8",
      "channel": "https://youtube.com/channel/UCbCmjCuTUZos6Inko4u57UQ"
    }
  },
  {
    "title": "ABC Song | Wendy Pretend Play Learning Alphabet w/ Toys &amp; Nursery Rhyme Songs",
    "videoId": "BNTCpF_n6J4",
    "thumb": {
      "url": "https://i.ytimg.com/vi/BNTCpF_n6J4/mqdefault.jpg",
      "width": 320,
      "height": 180
    },
    "channelId": "UCgFXm4TI8htWmCyJ6cVPG_A",
    "urls": {
      "video": "https://youtu.be/BNTCpF_n6J4",
      "channel": "https://youtube.com/channel/UCgFXm4TI8htWmCyJ6cVPG_A"
    }
  },
  {
    "title": "Alphabet Song | ABC Song | Phonics Song",
    "videoId": "36IBDpTRVNE",
    "thumb": {
      "url": "https://i.ytimg.com/vi/36IBDpTRVNE/mqdefault.jpg",
      "width": 320,
      "height": 180
    },
    "channelId": "UC1jhiDqp-jIYR07Ini8Jamw",
    "urls": {
      "video": "https://youtu.be/36IBDpTRVNE",
      "channel": "https://youtube.com/channel/UC1jhiDqp-jIYR07Ini8Jamw"
    }
  }
]
```

## Room<a id="sec-2-2"></a>

### Users<a id="sec-2-2-1"></a>

Path: `rooms/<ROOM>`

Method: `GET`

Response:

```json
{
  "_id": "<ROOM ID>",
  "name": "tech",
  "users": [
    {
      "_id": "<CURRENT ID>",
      "handle": "matriarch",
      "operator_id": "<OP ID>",
      "user_id": "<USER ID>",
      "username": "<ACCOUNT>",
      "isBroadcasting": true,
      "assignedBy": null,
      "isAdmin": false,
      "isSiteMod": false,
      "isSupporter": false,
      "userIcon": null,
      "color": "aquaalt"
    },
  ],
  "attrs": {
    "owner": "<USER ID>",
    "janus_id": 1782420776,
    "fresh": false,
    "ageRestricted": false
  },
  "settings": {
    "public": true,
    "modOnlyPlayMedia": true,
    "forcePtt": true,
    "forceUser": false,
    "description": "Technology, Games, and THC 18+ ☮ Discord.gg/UpDZMB3 ☮",
    "topic": {
      "text": "Join our Discord server!",
      "updatedAt": "<ISO 8601 UTC>",
      "updatedBy": {
        "_id": "<USER ID>",
        "username": "<ROOM>"
      }
    },
    "display": "room-display/display-tech.jpg",
    "requiresPassword": false
  }
}
```

### Unread<a id="sec-2-2-2"></a>

Path: `message/<USER ID>/unread`

Method: `GET`

Response:

```json
{
  "unread": 0
}
```

TODO: Sort this out

### Profile<a id="sec-2-2-3"></a>

Path: `/user/<USER ID>/profile`

Method: `GET`

Response:

```json
{
    "username": "notfat",
    "joinDate": "<ISO 8601 UTC>",
    "lastActive": "<ISO 8601 UTC>",
    "location": "",
    "pic": "user-avatar/avatar-<USERNAME>.png",
    "trophies": [{
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-email-verified.jpg",
        "description": "You have confirmed your email is real and is owned by you. Useful in case you need to reset your password",
        "_id": "5b16450d8de04a00075d1f47",
        "name": "TROPHY_EMAIL_VERIFIED",
        "type": "TYPE_MANUAL",
        "__v": 0,
        "title": "Email verified"
    }, {
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-site-supporter.jpg",
        "description": "A user who has supported the site",
        "_id": "5b16450d8de04a00075d1f49",
        "name": "TROPHY_SITE_SUPPORTER",
        "type": "TYPE_MANUAL",
        "__v": 0,
        "title": "Site supporter!"
    }, {
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-site-supporter-gold.jpg",
        "description": "A supporter who has set up recurring donation payments, or who has donated a significant amount",
        "_id": "5b16450d8de04a00075d1f4a",
        "name": "TROPHY_SITE_SUPPORTER_GOLD",
        "type": "TYPE_MANUAL",
        "__v": 0,
        "title": "Gold site supporter!"
    }, {
        "conditions": {
            "date": {
                "day": 1,
                "month": 1,
                "year": 2020
            }
        },
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-placeholder.png",
        "description": "",
        "_id": "5b16450d8de04a00075d1f56",
        "name": "TROPHY_NEW_YEARS_2020",
        "type": "TYPE_OCCASION",
        "__v": 0,
        "title": "Happy new year 2020"
    }, {
        "conditions": {
            "date": {
                "day": 25,
                "month": 12,
                "year": 2019
            }
        },
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-placeholder.png",
        "description": "",
        "_id": "5b16450d8de04a00075d1f55",
        "name": "TROPHY_XMAS_2019",
        "type": "TYPE_OCCASION",
        "__v": 0,
        "title": "Xmas 2019"
    }, {
        "conditions": {
            "date": {
                "day": 5,
                "month": 11,
                "year": 2019
            }
        },
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-5th-nov-2019.jpg",
        "description": "",
        "_id": "5b16450d8de04a00075d1f54",
        "name": "TROPHY_FIFTH_NOVEMBER_2019",
        "type": "TYPE_OCCASION",
        "__v": 0,
        "title": "Fifth of November 2019"
    }, {
        "conditions": {
            "date": {
                "day": 31,
                "month": 10,
                "year": 2019
            }
        },
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-halloween-2019.jpg",
        "description": "",
        "_id": "5b16450d8de04a00075d1f53",
        "name": "TROPHY_HALLOWEEN_2019",
        "type": "TYPE_OCCASION",
        "__v": 0,
        "title": "Halloween 2019"
    }, {
        "image": "https://s3.amazonaws.com/jic-assets/trophies/trophy-gifted.jpg",
        "description": "Someone sent this user support status as a gift",
        "_id": "5c8b78f2cb32320008c2adb7",
        "name": "TROPHY_GIFTED",
        "title": "Gifted support",
        "type": "TYPE_MANUAL",
        "__v": 0
    }],
    "trophyCount": 8,
    "userType": "site supporter"
}
```

### Emoji<a id="sec-2-2-4"></a>

Path: `/rooms/tech/emoji`

Method: `GET`

Response:

```json
[]
```

### Room Settings<a id="sec-2-2-5"></a>
Path: `/api/rooms/<ROOM>`
  
Method: `GET`

Response:

```json
{
    "_id": "<ROOM ID>",
    "name": "<ROOM>",
    "users": [],
    "attrs": {
        "owner": "<OWNER ID>",
        "janus_id": "",
        "fresh": false,
        "ageRestricted": false
    },
    "settings": {
        "public": true,
        "modOnlyPlayMedia": true,
        "forcePtt": true,
        "forceUser": true,
        "description": "",
        "topic": {
            "text": "",
            "updatedAt": "<ISO 8601 UTC>",
            "updatedBy": {
                "_id": "<USER ID>",
                "username": "<USERNAME>"
            }
        },
        "display": "room-display/display-<ROOM>.png",
        "requiresPassword": false
    }
}
```

### Broadcast Options<a id="sec-2-2-6"></a>

Path: `/api/user/checkCanBroadcast/<ROOM>`

Method: `GET`

Response:

```json
{
    "videoOptions": [{
        "id": "VIDEO_240",
        "label": "240p",
        "dimensions": {
            "width": 320,
            "height": 240
        },
        "frameRate": 15,
        "bitRate": 128000
    }, {
        "id": "VIDEO_480",
        "label": "480p",
        "dimensions": {
            "width": 640,
            "height": 480
        },
        "frameRate": 30,
        "bitRate": 1024000
    }, {
        "id": "VIDEO_720",
        "label": "720p",
        "dimensions": {
            "width": 960,
            "height": 720
        },
        "frameRate": 30,
        "bitRate": 2048000
    }, {
        "id": "VIDEO_720_60",
        "label": "720p 60fps",
        "dimensions": {
            "width": 960,
            "height": 720
        },
        "frameRate": 60,
        "bitRate": 4096000
    }, {
        "id": "VIDEO_1080",
        "label": "1080p",
        "dimensions": {
            "width": 1920,
            "height": 1080
        },
        "frameRate": 30,
        "bitRate": 4096000
    }, {
        "id": "VIDEO_1080_60",
        "label": "1080p 60fps",
        "dimensions": {
            "width": 1920,
            "height": 1080
        },
        "frameRate": 60,
        "bitRate": 8192000
    }]
}
```

### Roles<a id="sec-2-2-7"></a>

Path: `/api/role/room/<ROOM>/all`

Method: `GET`

Response:

```json
[{
    "icon": {
        "url": null,
        "color": "aqua"
    },
    "permissions": {
        "ban": false,
        "kick": false,
        "closeCam": false,
        "muteUserAudio": false,
        "muteUserChat": false,
        "muteRoomChat": false,
        "muteRoomAudio": false,
        "applyPassword": false,
        "assignRoles": false,
        "manageRoles": false,
        "playMedia": false,
        "controlMedia": false,
        "playYoutube": true,
        "uploadEmoji": false,
        "roomDetails": false,
        "broadcast": true,
        "bypassPassword": false
    },
    "permanent": true,
    "isDefault": true,
    "_id": "<ROLE ID>",
    "name": "Everyone",
    "tag": "everyone",
    "roomId": "<ROOM ID>",
    "createdBy": "<PROBABLY OWNER ID>",
    "createdAt": "<ISO 8601 UTC>",
    "__v": 0,
    "order": 0
}]
```

### Session<a id="sec-2-2-8"></a>

Path: `/api/user/session`

Method: `POST`

```json
{
    "fp": ""
}
```

Response:

```json
{
    "user": {
        "user_id": "<USER ID>",
        "username": "<USERNAME>",
        "isAdmin": false,
        "isSiteMod": false,
        "isSupporter": false,
        "isGold": null,
        "userIcon": null,
        "settings": {
            "playYtVideos": false,
            "allowPrivateMessages": true,
            "pushNotificationsEnabled": false,
            "receiveUpdates": false,
            "receiveMessageNotifications": true,
            "darkTheme": true,
            "videoQuality": "VIDEO_240",
            "wideLayout": false,
            "userIcon": null,
            "ignoreList": []
        },
        "videoQuality": {
            "id": "VIDEO_240",
            "label": "240p",
            "dimensions": {
                "width": 320,
                "height": 240
            },
            "frameRate": 15,
            "bitRate": 128000
        }
    },
    "token": ""
}
```

### Request Template

Path: ``

Method: `GET`

Response:

```json
```
