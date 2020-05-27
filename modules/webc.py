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
import inspect
import json
import random
import string
from dataclasses import dataclass
from enum import Enum

import aioice
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, RTCIceParameters
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
    out_location: str = "/dev/video1"


pcs = set()


def transaction_id():
    return "".join(random.choice(string.ascii_letters) for x in range(12))


class JanusPlugin:
    def __init__(self):
        self._queue = asyncio.Queue()


class Webc(Cog):

    def __init__(self, bot):
        super().__init__(bot)

        self.create_id = transaction_id()
        self._attach_id = transaction_id()
        self._attach_plugin_id = transaction_id()
        self.publish_transaction_id = transaction_id()
        self.message_id = transaction_id()
        self.candidates_complete = transaction_id()

        self.transactions = {self.create_id: 'create',
                             self._attach_id: 'attach',
                             self._attach_plugin_id: 'attach_plugin',
                             self.publish_transaction_id: 'publish',
                             self.message_id: 'message',
                             self.candidates_complete: 'candidates_complete', }

        self._plugins = {}

        self.token = ""
        self.room = ""
        self.janus_id = ""
        self.handle_id = ""
        self.username = ""
        self.password = ""
        self._session_url = None
        self._session = None

        self.player = None

        self.turnservers = None
        p = RTCIceParameters(usernameFragment="", password="", iceLite=False)
        self.connection = aioice.Connection(ice_controlling=True, )
        self.pc = RTCPeerConnection()

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

    async def publish(self, plugin, player):
        """
        Send video to the room.
        """
        self.connection.turn_server = self.turnservers
        self.connection.turn_transport = "udp"
        self.connection.turn_username = self.username
        self.connection.turn_password = self.password
        self.connection.remote_username = self.username
        self.connection.remote_password = self.password

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

        # for c in self.connection.local_candidates:
        #     c.sdpMid = '0'
        #     self.pc.addIceCandidate(c)

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
                     "transaction": self.candidates_complete,
                     "token": self.token, "session_id": self.session_id,
                     "handle_id": self.handle_id}
        await self.send(json.dumps(completed))
        configure = {"janus": "message",
                     "body": request,
                     "transaction": self.message_id,
                     "token": self.token,
                     "session_id": self.session_id,
                     "handle_id": self.handle_id}
        await self.send(json.dumps(configure))

    async def send(self, message):
        self.log.ws_send(message)
        await self._session.send_str(message)

    async def create(self):
        """starts a janus connection"""
        create = {"janus": "create", "transaction": self.create_id,
                  "token": self.token}
        await self.send(json.dumps(
            create))

    async def success(self, data):
        trans = self.transactions.get(data['transaction'])
        if trans:
            self.log.info(f"transaction {trans}:{data['transaction']} succeeded")

        if data.get("transaction") == self.create_id:
            self.session_id = data["data"]["id"]
            await self.send(json.dumps({"janus": "attach", "plugin": "janus.plugin.videoroom",
                                        "transaction": self._attach_plugin_id,
                                        "token": self.token,
                                        "session_id": self.session_id}))
        if data.get("transaction") == self.publish_transaction_id or data.get("transaction") == "ppppp":
            if 'jsep' in data:
                if data['jsep'].get('type', "") == "answer":
                    sdp = data['jsep'].get('sdp', "")

                    description = RTCSessionDescription(type="answer", sdp=sdp)

                    await self.pc.setRemoteDescription(description)
                    # await self.connection.connect()
                    asyncio.ensure_future(self.connection.connect(), loop=asyncio.get_event_loop())
                    await self.bot.wsend('42["room::setUserIsBroadcasting",{"isBroadcasting":true}]')

        if data.get("transaction") == self._attach_id:
            await self.attach(data)
        if data.get("transaction") == self._attach_plugin_id:
            await self.attach_plugin(data)

    async def retrieve_name(self, var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    async def attach(self, data: json):
        pass

    async def attach_plugin(self, data):
        self.handle_id = data["data"]["id"]
        plugin = JanusPlugin()
        self._plugins[self.session_id] = plugin
        message = {"janus": "message",
                   "transaction": self._attach_id,
                   "token": self.token,
                   "session_id": self.session_id,
                   "handle_id": self.handle_id
                   }
        payload = {
            "body": {
                "display": "5e90938358e6a300086c279d",
                "ptype": "publisher",
                "request": "join",
                "room": int(self.janus_id),
            }
        }

        message.update(payload)
        await self.send(json.dumps(message))
        d = {"janus": "keepalive", "session_id": self.session_id, "transaction": transaction_id(),
             "token": self.token}
        await self.send(json.dumps(d))

        await asyncio.sleep(3)
        await self.publish(plugin=list(self._plugins.values())[0], player=self.player)
        # exchange media for 10 minutes
        print("Exchanging media")

    async def trickle_complete(self, data):
        d = {"janus": "message", "body": {"request": "configure"}, "transaction": self.candidates_complete,
             "token": self.token,
             "session_id": self.session_id, "handle_id": self.handle_id}
        await self.send(json.dumps(d))

    async def trickle(self, data: json):
        if data.get("janus") == "trickle" and data["candidate"].get("completed", False):
            await self.trickle_complete(data)
        else:
            data["candidate"]["sdpMid"] = int(data["candidate"]["sdpMid"])
            candidate = json.dumps(data["candidate"])
            candidate = candidate.replace(",", "")
            c = candidate.split("candidate:")

            candidate = candidate.replace("candidate:", "")
            candidate = candidate[:44] + candidate[44:].replace('"', '')
            candidate = aioice.Candidate.from_sdp(candidate)
            candidate.sdpMid = data["candidate"]["sdpMid"]
            self.pc.addIceCandidate(candidate)

    async def message_joinroom(self):
        pass

    async def message_configure(self):
        pass

    async def ack(self, data):
        pass

    async def event(self, data):
        plugin = self._plugins.get(data["sender"], None)
        if plugin:
            await plugin._queue.put(data)

    async def keepalive(self):
        pass

    async def process_messages(self, message):
        data = json.loads(message.data)
        routes = {
            'event': self.event,
            'trickle': self.trickle,
            'success': self.success,
            'ack': self.ack,
        }
        route = routes.get(data.get("janus"))
        if route:
            self.log.info(f"Attempting{data.get('janus')}")
            await route(data=data)

    async def start(self):
        async with self.bot.api.session.ws_connect("wss://jumpin.chat/janus/ws") as self._session:
            await self.create()
            async for msg in self._session:
                self.log.debug(f"{msg.data}")
                await self.process_messages(msg)

    @makeCommand(aliases=["cc"], description="cams up in a room")
    async def cc(self, c: Command):
        data = await self.bot.api.get('https://jumpin.chat/api/turn/')
        data = json.loads(await data.text())
        self.username = data.get("username", "")
        self.password = data.get("password", "")
        uris = data.get("uris", "")

        turnservers = uris[0].split(":")
        self.turnservers = (turnservers[1], turnservers[2])

        options = {"volume": "33", "video_size": f"720x480",
                   "pix_fmt": "vp8"}
        self.player = MediaPlayer(
            "http://www.wiki-bazar.net/~josh/V%20for%20Vendetta/%5bfmovies.to%5d%20V%20For%20Vendetta%20-%20HD%201080p.mp4",
            format="mp4", options=options)
        data = await self.bot.api.get("https://jumpin.chat/api/rooms/johnripper")
        data = await data.json()
        self.janus_id = int(data['attrs'].get("janus_id"))

        data = await self.bot.api.get('https://jumpin.chat/api/janus/token')
        t = await data.json()
        self.token = t.get("token", False)
        if self.token:
            # join video room
            await self.start()
