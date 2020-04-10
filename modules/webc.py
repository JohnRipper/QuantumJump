# -*- coding: utf-8 -*-
#
# Copyright 2020, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 3/24/20
# This file is part of QuantumJump
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
import json
import random
import string
from dataclasses import dataclass
from enum import Enum

import aioice
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer

from lib.cog import Cog
from lib.command import makeCommand, Command


class SupportedFormats(Enum):
    NONE = 0
    HTTPS = 1
    MP4 = 2
    DESKTOP = 3


class Types(Enum):
    NONE = 0
    HTTPS = 1
    MP4 = 2
    DESKTOP = 3


@dataclass
class Video:
    type: Types = 0
    frame_rate: int = 30
    threads: int = 0
    is_playing: bool = False

    # http type
    url: str = ""

    # local movie type
    name: str = ""

    # desktop
    # todo expirement with getting available displays
    x_display: str = ":0.0"
    width: int = 1920
    height: int = 1080
    x_offset: int = 1920
    y_offset: int = 0
    out_location: str = "/dev/video2"


pcs = set()


def transaction_id():
    return "".join(random.choice(string.ascii_letters) for x in range(12))


class JanusPlugin:
    def __init__(self):
        self._queue = asyncio.Queue()


class Webc(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self._plugins = {}
        self.token = ""
        self.janus_id = ""
        self.handle_id = ""
        self.username = ""
        self.password = ""
        self._session_url = None
        self._session = None
        self._attach_id = transaction_id()
        self._attach_plugin_id = transaction_id()
        self.player = None
        self.publish_transaction_id = transaction_id()
        self.turnservers = None
        self.pc = None

    async def publish(self, plugin, player):
        """
        Send video to the room.
        """
        self.connection = aioice.Connection(ice_controlling=True, )
        print(self.turnservers)

        self.pc = RTCPeerConnection()
        pcs.add(self.pc)

        @self.pc.on("signalingstatechange")
        async def on_signalingstatechange():
            print("ICE signaling state is %s" % self.pc.signalingState)

            if self.pc.iceConnectionState == "failed":
                await self.connection.close()

            if self.pc.iceConnectionState == 'completed':
                print("completed")

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % self.pc.iceConnectionState)

            if self.pc.iceConnectionState == "failed":
                await self.connection.close()

            if self.pc.iceConnectionState == 'completed':
                print("completed")

        self.connection.turn_server = self.turnservers
        self.connection.turn_transport = "udp"
        self.connection.turn_username = self.username
        self.connection.turn_password = self.password
        self.connection.remote_username = self.username
        self.connection.remote_password = self.password
        print(f"hello {self.username} {self.password}")
        # self.connection.remote_username = self.username
        # self.connection.remote_password = self.password
        # configure media
        media = {"audio": False, "video": True}
        if player and player.audio:
            self.pc.addTrack(player.audio)
            media["audio"] = True

        if player and player.video:
            self.pc.addTrack(player.video)
        else:
            self.pc.addTrack(VideoStreamTrack())

        await self.connection.gather_candidates()

        for c in self.connection.local_candidates:
            c.sdpMid = 0
            self.pc.addIceCandidate(c)

        # send offer
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        request = {"request": "configure"}
        request.update(media)
        message = {"janus": "message",
                   "transaction": self.publish_transaction_id,
                   "session_id": self.session_id,
                   "handle_id": self.handle_id,
                   "token": self.token
                   }
        payload = {
            "body": request,
            "jsep": {
                "sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type,
            },
        }
        message.update(payload)
        await self.send(json.dumps(message))

        print("getting candidates")
        for c in self.connection.local_candidates:
            data = {"janus": "trickle",
                    "candidate": {
                        "candidate": "candidate:" + aioice.Candidate.to_sdp(c),
                        "sdpMid": "0", "sdpMLineIndex": 0}, "transaction": transaction_id(),
                    "token": self.token,
                    "session_id": self.session_id, "handle_id": self.handle_id}
            await self.send(json.dumps(data))
        completed = {"janus": "trickle", "candidate": {"completed": True},
                     "transaction": "peepee",
                     "token": self.token, "session_id": self.session_id,
                     "handle_id": self.handle_id}
        await self.send(json.dumps(completed))
        configure = {"janus": "message",
                     "body": {"request": "configure"},
                     "transaction": "NXZQc2cE5Gik",
                     "token": self.token,
                     "session_id": self.session_id,
                     "handle_id": self.handle_id}
        await self.send(json.dumps(configure))

    async def send(self, message):
        print(f"sending: {message}")
        await self._session.send_str(message)

    async def create(self):
        data = await self.bot.api.get('https://jumpin.chat/api/janus/token')
        t = json.loads(await data.text())
        token = t.get("token", "")
        async with self.bot.api.session.ws_connect("wss://jumpin.chat/janus/ws") as self._session:
            create = {"janus": "create", "transaction": "create_this_shit",
                      "token": token}
            await self.send(json.dumps(create))
            async for msg in self._session:
                print(msg)
                data = json.loads(msg.data)

                if data["janus"] == "event":
                    plugin = self._plugins.get(data["sender"], None)
                    if plugin:
                        await plugin._queue.put(data)
                    else:
                        print(data)

                if data.get("janus") == "trickle" and data["candidate"].get("completed", False):
                    d = {"janus": "message", "body": {"request": "configure"}, "transaction": "eiCUHTyqRe4z",
                         "token": token,
                         "session_id": self.session_id, "handle_id": self.handle_id}
                    await self.send(json.dumps(d))

                elif data.get("janus") == "trickle":
                    pass
                    # await self.pc.addIceCandidate(aioice.Candidate.from_sdp(json.dumps(data["candidate"])))
                if data.get("transaction") == "create_this_shit":
                    self.session_id = data["data"]["id"]
                    await self.send(json.dumps({"janus": "attach", "plugin": "janus.plugin.videoroom",
                                                "transaction": self._attach_plugin_id,
                                                "token": token,
                                                "session_id": self.session_id}))
                if data.get("transaction") == self.publish_transaction_id or data.get("transaction") == "ppppp":
                    #   apply answer
                    if 'jsep' in data:
                        if data['jsep'].get('type', "") == "answer":
                            sdp = data['jsep'].get('sdp', "")

                            description = RTCSessionDescription(type="answer", sdp=sdp)

                            await self.pc.setRemoteDescription(description)
                            asyncio.ensure_future(self.connection.connect(), loop=asyncio.get_event_loop())
                            await self.bot.wsend('42["room::setUserIsBroadcasting",{"isBroadcasting":true}]')

                if data.get("transaction") == self._attach_id:
                    # send video
                    pass

                if data.get("transaction") == self._attach_plugin_id:
                    self.handle_id = data["data"]["id"]
                    plugin = JanusPlugin()
                    self._plugins[self.session_id] = plugin
                    message = {"janus": "message",
                               "transaction": self._attach_id,
                               "token": token,
                               "session_id": self.session_id,
                               "handle_id": self.handle_id
                               }
                    payload = {
                        "body": {
                            "display": "aiortc",
                            "ptype": "publisher",
                            "request": "join",
                            "room": self.janus_id,
                        }
                    }

                    message.update(payload)
                    await self.send(json.dumps(message))
                    await self.publish(plugin=list(self._plugins.values())[0], player=self.player)
                    # exchange media for 10 minutes
                    print("Exchanging media")

    @makeCommand(aliases=["cc"], description="cams up in a room")
    async def cc(self, c: Command):
        data = await self.bot.api.get('https://jumpin.chat/api/turn/')
        print(await data.text())
        data = json.loads(await data.text())
        self.username = data.get("username", "")
        self.password = data.get("password", "")
        uris = data.get("uris", "")

        turnservers = uris[0].split(":")
        self.turnservers = (turnservers[1], turnservers[2])

        options = {"volume": "33", "video_size": f"1920x1080"}
        self.player = MediaPlayer("/dev/video2", format="v4l2", options=options)

        data = await self.bot.api.get("https://jumpin.chat/api/rooms/johnripper")
        data = json.loads(await data.text())
        self.janus_id = data['attrs'].get("janus_id")

        data = await self.bot.api.get('https://jumpin.chat/api/janus/token')
        t = json.loads(await data.text())
        self.token = t.get("token", "")

        # join video room
        await self.create()
