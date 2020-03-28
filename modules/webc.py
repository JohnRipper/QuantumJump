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

import aiohttp
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
    def __init__(self, session, url):
        self._queue = asyncio.Queue()
        self._session = session
        self._url = url

    async def send(self, payload):
        message = {"janus": "message", "transaction": transaction_id()}
        message.update(payload)
        async with self._session._http.post(self._url, json=message) as response:
            data = await response.json()
            assert data["janus"] == "ack"

        response = await self._queue.get()
        assert response["transaction"] == message["transaction"]
        return response


class JanusSession:
    def __init__(self, url, bot):
        self._bot = bot
        self._session = None
        self._poll_task = None
        self._plugins = {}
        self._root_url = url

    async def destroy(self):
        if self._poll_task:
            self._poll_task.cancel()
            self._poll_task = None

        if self._session_url:
            message = {"janus": "destroy", "transaction": transaction_id()}
            async with self._http.post(self._session_url, json=message) as response:
                data = await response.json()
                assert data["janus"] == "success"
            self._session_url = None

        if self._http:
            await self._http.close()
            self._http = None


async def publish(plugin, player):
    """
    Send video to the room.
    """
    pc = RTCPeerConnection()
    pcs.add(pc)

    # configure media
    media = {"audio": False, "video": True}
    if player and player.audio:
        pc.addTrack(player.audio)
        media["audio"] = True

    if player and player.video:
        pc.addTrack(player.video)
    else:
        pc.addTrack(VideoStreamTrack())

    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    request = {"request": "configure"}
    request.update(media)
    response = await plugin.send(
        {
            "body": request,
            "jsep": {
                "sdp": pc.localDescription.sdp,
                "trickle": False,
                "type": pc.localDescription.type,
            },
        }
    )

    # apply answer
    await pc.setRemoteDescription(
        RTCSessionDescription(
            sdp=response["jsep"]["sdp"], type=response["jsep"]["type"]
        )
    )


async def subscribe(session, room, feed, recorder):
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("track")
    async def on_track(track):
        print("Track %s received" % track.kind)
        if track.kind == "video":
            recorder.addTrack(track)
        if track.kind == "audio":
            recorder.addTrack(track)

    # subscribe
    plugin = await session.attach("janus.plugin.videoroom")
    response = await plugin.send(
        {"body": {"request": "join", "ptype": "subscriber", "room": room, "feed": feed}}
    )

    # apply offer
    await pc.setRemoteDescription(
        RTCSessionDescription(
            sdp=response["jsep"]["sdp"], type=response["jsep"]["type"]
        )
    )

    # send answer
    await pc.setLocalDescription(await pc.createAnswer())
    response = await plugin.send(
        {
            "body": {"request": "start"},
            "jsep": {
                "sdp": pc.localDescription.sdp,
                "trickle": False,
                "type": pc.localDescription.type,
            },
        }
    )
    await recorder.start()


class Webc(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self._plugins = {}
        self._session_url = None

    async def create(self):
        data = await self.bot.api.get('https://jumpin.chat/api/janus/token')
        t = json.loads(await data.text())
        print(t)
        token = t.get("token", "")
        async with self.bot.api.session.ws_connect("wss://jumpin.chat/janus/ws") as self._session:
            create = {"janus": "create", "transaction": "create_this_shit",
                      "token": token}
            await self._session.send_str(json.dumps(create))
            async for msg in self._session:
                data = json.loads(msg.data)

                if data["janus"] == "event":
                    plugin = self._plugins.get(data["sender"], None)
                    if plugin:
                        await plugin._queue.put(data)
                    else:
                        print(data)

                if data.get("transaction") == "create_this_shit":
                    session_id = data["data"]["id"]
                    await self._session.send_str(json.dumps({"janus": "attach", "plugin": "janus.plugin.videoroom",
                                                             "transaction": "attach_this_plugin",
                                                             "token": token,
                                                             "session_id": session_id}))

    async def attach(self, plugin_name: str) -> JanusPlugin:
        message = {
            "janus": "attach",
            "plugin": plugin_name,
            "transaction": transaction_id()
        }
        async with await self.bot.api.post("wss://jumpin.chat/janus/ws", json=message) as response:
            print(await response.text())
            data = await response.json()
            assert data["janus"] == "success"
            plugin_id = data["data"]["id"]
            plugin = JanusPlugin(self, self._session_url + "/" + str(plugin_id))
            self._plugins[plugin_id] = plugin
            return plugin

    @makeCommand(aliases=["cc"], description="cams up in a room")
    async def cc(self, c: Command):
        data = await self.bot.api.get('https://jumpin.chat/api/turn/')
        print(await data.text())
        data = json.loads(await data.text())
        username = data.get("username", "")
        password = data.get("password", "")
        uris = data.get("uris", "")

        turnservers = uris[0].split(":")
        turn = (turnservers[1], turnservers[2])

        options = {"volume": "33", "video_size": f"1920x1080"}
        player = MediaPlayer("/dev/video2", format="v4l2", options=options)

        data = await self.bot.api.get("https://jumpin.chat/api/rooms/johnripper")
        data = json.loads(await data.text())
        janus_id = data['attrs'].get("janus_id")

        # join video room
        plugin = await self.attach("janus.plugin.videoroom")
        response = await plugin.send(
            {
                "body": {
                    "display": "aiortc",
                    "ptype": "publisher",
                    "request": "join",
                    "room": janus_id,
                }
            })
        publishers = response["plugindata"]["data"]["publishers"]
        for publisher in publishers:
            print("id: %(id)s, display: %(display)s" % publisher)
        await self.create()

        # send video
        await publish(plugin=plugin, player=player)
        # exchange media for 10 minutes
        print("Exchanging media")
        await asyncio.sleep(600)

    @makeCommand(aliases=["cam"], description="Search Urban Dictionary")
    async def cam(self, c: Command):

        pc = RTCPeerConnection()

        connection = None
        video = Video()
        player = None

        data = await self.bot.api.get('https://jumpin.chat/api/turn/')
        print(await data.text())
        data = json.loads(await data.text())
        # {"username":"1585259115:1585259115","password":"wBp0Wqg3ddna1j3QouYS3TBWSH8=","uris":["turn:turn.jumpin.chat:5349"],"ttl":86400}
        username = data.get("username", "")
        password = data.get("password", "")
        uris = data.get("uris", "")
        ttl = data.get("ttl", "")

        data = await self.bot.api.get("https://jumpin.chat/api/rooms/johnripper")
        data = json.loads(await data.text())
        print(f"janusid {data}")
        janus_id = data['attrs'].get("janus_id")
        id = 0
        handle_id = 0

        data = await self.bot.api.get('https://jumpin.chat/api/janus/token')
        print(await data.text())
        t = json.loads(await data.text())
        token = t.get("token", "")

        async with self.bot.api.session.ws_connect("wss://jumpin.chat/janus/ws", ) as self.ws:
            create = {"janus": "create", "transaction": "prefbot",
                      "token": token}
            await self.ws.send_str(json.dumps(create))

            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(msg.data)

                d = json.loads(msg.data)

                if d.get("transaction") == "prefbot":
                    print(f"sessoionid {d}")
                    id = d['data'].get("id")
                    await self.ws.send_str(json.dumps({"janus": "attach", "plugin": "janus.plugin.videoroom",
                                                       "transaction": "prefbotnext",
                                                       "token": token,
                                                       "session_id": id}))

                if d.get("transaction") == "prefbotnext":
                    handle_id = d['data'].get("id")
                    data = {"janus": "message", "body":
                        {"request": "join",
                         "room": janus_id,
                         "ptype": "publisher",
                         "display": "aiortc"},
                            "transaction": "preftired",
                            "token": token,
                            "session_id": id,
                            "handle_id": handle_id}
                    print(data)
                    await self.ws.send_str(json.dumps(data))

                if d.get("transaction") == "preftired":

                    # s_server = data['servers'][0].split(":")
                    connection = aioice.Connection(ice_controlling=True, )

                    video.type = Types.HTTPS
                    video.url = 'http://dominicannetworkvideos.com/files/cinemas/Dunkirk.mp4'

                    if video.type == Types.HTTPS:
                        options = {"volume": "33", "video_size": f"{video.width}x{video.height}"}
                        player = MediaPlayer(video.out_location, format="v4l2", options=options)

                    # if player and player.audio:
                    #    pc.addTrack(player.audio)
                    if player and player.video:
                        pc.addTrack(player.video)

                    @pc.on("iceconnectionstatechange")
                    async def on_iceconnectionstatechange():
                        print("ICE connection state is %s" % pc.iceConnectionState)

                        if pc.iceConnectionState == "failed":
                            await connection.close()

                        if pc.iceConnectionState == 'completed':
                            print("completed")

                    turnservers = uris[0].split(":")
                    turn = (turnservers[1], turnservers[2])
                    connection.turn_server = turn
                    print(f"yooo {username} {password}")

                    connection.turn_username = username
                    connection.turn_password = password

                    await connection.gather_candidates()

                    await pc.setLocalDescription(await pc.createOffer())

                    print(f"offer {pc.localDescription.sdp}")

                    data = {"janus": "message",
                            "body": {"request": "configure",
                                     "audio": True, "video": True},
                            "transaction": "pref_help_pls",
                            "token": token,
                            "jsep": {"type": "offer", "sdp": pc.localDescription.sdp},
                            "session_id": id, "handle_id": handle_id}
                    await self.ws.send_str(json.dumps(data))

                    for c in connection.local_candidates:
                        transaction = ''.join(random.choices(string.ascii_uppercase, k=13))

                        data = {"janus": "trickle",
                                "candidate": {
                                    "candidate": "candidate:" + aioice.Candidate.to_sdp(c),
                                    "sdpMid": "0", "sdpMLineIndex": 0}, "transaction": transaction,
                                "token": token,
                                "session_id": id, "handle_id": handle_id}
                        print(f"sending {data}")
                        await self.ws.send_str(json.dumps(data))

                if d.get("transaction") == "pref_help_pls":
                    print(f"prefhelppls {d}")
                    if 'jsep' in d:
                        if d['jsep'].get('type', "") == "answer":
                            sdp = d['jsep'].get('sdp', "")

                            self.bot.wsend('42["room::setUserIsBroadcasting",{"isBroadcasting":true}]')

                            description = RTCSessionDescription(type="answer", sdp=sdp)
                            await pc.setRemoteDescription(description)

                            asyncio.ensure_future(connection.connect(), loop=asyncio.get_event_loop())

                if d.get("janus") == "trickle" and d["candidate"].get("completed", False):
                    data = {"janus": "message", "body": {"request": "configure"}, "transaction": "eiCUHTyqRe4z",
                            "token": token,
                            "session_id": id, "handle_id": handle_id}
                    print(f"sending {data}")
                    await self.ws.send_str(json.dumps(data))
