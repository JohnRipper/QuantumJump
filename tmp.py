import asyncio
import sys

import json
import time
from concurrent import futures
from dataclasses import dataclass

import websockets
from lib.api import Api
from lib.config import Configuration
import random
import re
import aiohttp


# TEMP
@dataclass
class WSMsg:
    event: str
    data: dict = None

COLOR = ["red", "green", "yellow", "blue", "purple", "aqua", "orange",
         "redalt", "greenalt", "yellowalt", "bluealt", "purplealt",
         "aquaalt", "orangealt"]

class QuantumJumpBot:

    def __init__(self):
        self._ws = None
        self.is_running = False
        self.start_time = time.time()
        # playlist info but im shit
        self.current = {}
        # "_id": {"handle": str, "username": str | None, "handle": str}
        self.userlist = {}

        self.settings = None
        self.api = Api()
        self.tmpid = None

    async def run(self):
        await self.connect()

    async def connect(self):
        await self.api.login(self.settings.Bot.username,
                             self.settings.Bot.password)
        async with websockets.connect(
                uri=await self.api.get_wss(),
                timeout=600,
                origin="https://jumpin.chat"
        ) as self._ws:
            print("Socket started")
            self.is_running = True
            await self.send("2probe")
            # calls to api/rooms/<room> with no args
            await self.adduserlist()
            async for message in self._ws:
                if message == "3probe":
                    await self.send("5")
                    await self.send("room::join", {"room": self.settings.Bot.roomname})
                    print(self.userlist)
                elif message.startswith("42"):
                    message = await self.recv(message)
                    # have to wait for self::join before nick change
                    if message.event == "self::join":
                        self.tmpid = message.data["user"]["_id"]
                        await self.send("room::handleChange",
                                        {"userId": self.tmpid,
                                         "handle": self.settings.Bot.nickname})
                    elif message.event == "room::message":
                        if message.data["message"].startswith("!"):
                            m = message.data["message"].split(" ")
                            command = m[0].lstrip("!")
                            rest = " ".join(m[1:])
                            if command == "yt":
                                await self.tmpyt(rest)

                            elif command == "room":
                                await self.getusers(rest)
                            # blocking
                            # elif command == "tokes":
                            #     await self.dotoke(rest.strip())
                    # recieved for updates like broadcasting (bool), chat color, etc
                    elif message.event == "room::updateUser":
                        user = message.data["user"]
                        if user["_id"] != self.tmpid:
                            current_color = self.userlist[user["_id"]]["color"]
                            new_color = user["color"]
                            nick = user["handle"]
                            if new_color not in COLOR:
                                # incase any hidden colors show up somehow
                                print("\n\nColor is missing\n\n")
                            if current_color != new_color:
                                self.userlist[user["_id"]]["color"] = new_color
                                await self.sendmsg(f"{nick} changed their color from {current_color} to {new_color}, awkward...", new_color)
                    # when a user joins the room with a guest nick, handleChange usually follows
                    elif message.event == "room::updateUserList":
                        user = message.data["user"]
                        # can add from this event or make another call to the API
                        await self.adduserlist(message.data)
                        if user["username"] == "johnripper":
                            # HUE
                            await self.sendmsg(":flag-mx::flag-mx::flag-mx: EL WETBACK REGRESO :flag-mx::taco::burrito::burrito:")
                        elif user["username"] == "xwista":
                            # HUE
                            await self.sendmsg(":flag-no: Luke has returned :flag-no:")

                    elif message.event == "room::disconnect":
                        del self.userlist[message.data["user"]["_id"]]

                    elif message.event == "client::error":
                        # print this in red
                        print(f"\033[91m---{message}\033[0m")
                        # shit workaround for notifying users that youtube is kill
                        await self.sendmsg("JumpinClient: " + message.data["message"], "red")
                    print(f"RECV_{message.event} {message.data}")
                else:
                    print(f"RECV_{message}")

    async def recv(self, msg: str) -> WSMsg:
        msg = msg.lstrip("42")
        msg = json.loads(msg)
        return WSMsg(*msg)

    async def send(self, event: str, data: dict = None):
        if data is not None:
            fmt = '42["{}",{}]'.format(event, json.dumps(data))
        else:
            fmt = event
        print(f"SEND: {fmt}")
        await self._ws.send(fmt)

    async def changecolor(self, color: str =None):
        if color is None:
            color = random.choice(COLOR)
        await self.send("room::changeColor",
                        {"color": color})

    async def sendmsg(self, msg: str, color: str = None):
        await self.send("room::message", {"message": msg})

    async def sendself(self, msg: str, color: str = None):
        # /me
        await self.send("room::command", {
            "message": {
                "command": "me",
                "value": msg,
            }
        })

    async def tmpskip(self):
        if len(self.current.keys()) > 0:
            await self.send("youtube::remove", {"id": self.current["_id"]})

    # async def dotoke(self, msg: str):
    #     # blocking
    #     options = ["torches", "lights up", "blazes", "bakes", "hotboxes your nan's bathroom",
    #                "puffs", "sparks their blunt", "lights their blunt", "sparks their joint",
    #                "lights their joint", "tokes", "sits this one out", "gets a shotgun from your mom"]
    #     if msg.isdigit():
    #         total_seconds = int(msg)
    #         minutes = int(total_seconds / 60)
    #         seconds = int(total_seconds % 60)
    #         # starting message
    #         if minutes != 0:
    #             await self.sendself(
    #                 f"preps for tokes in {minutes}minutes {seconds}s!")
    #         else:
    #             await self.sendself(f"quickly preps for tokes in {seconds} seconds!")
    #         # start counting down.
    #         for i in range(0, minutes):
    #             await asyncio.sleep(60)
    #             if minutes - i <= 5 & minutes - i != 0:
    #                 await self.sendmsg(f"{minutes} minute(s) left before tokes")
    #         await asyncio.sleep(seconds)
    #         await self.sendmsg("Time for tokes!")
    #         await asyncio.sleep(0.4)
    #         await self.sendself(random.choice(options))
    #     else:
    #         await self.sendmsg("Time for tokes!")
    #         await asyncio.sleep(0.4)
    #         await self.sendself(random.choice(options))

    async def tmpyt(self, msg: str):
        # use own API key for now, delete after repo is public
        aidasapikey = "AIzaSyCSQcdyy4T-QVLlelJBIW_572kBtHi2ams"
        searchurl = "https://www.googleapis.com/youtube/v3/search?part=snippet&"\
            "type=video&q={}&maxResults=1&"\
            "videoSyndicated=true&key={}"
        if "youtu" in msg:
            id_ = re.search("(?:v=|\.be\/)(.{11})", msg)[1]
            kek = random.randint(1, 1000)
            # why waste an API call just for the title? :^)
            title = f"10 Hour Twerk Compilation #{kek} [EMOTIONAL] You won't believe what Trump is hiding!"
        else:
            res = await self.api.get(searchurl.format(msg, aidasapikey))
            res = await res.text()
            videoid = json.loads(res)["items"][0]["id"]["videoId"]
            title = json.loads(res)["items"][0]["snippet"]["title"]
            id_ = videoid
        await self.send(
            "youtube::play",
            {"videoId": id_,
                "title": title}
        )

    async def adduserlist(self, data: dict = None):
        if data is None:
            res = await self.api.getroominfo(self.settings.Bot.roomname)
            js = json.loads(res)
            for each in js["users"]:
                self.userlist[each["_id"]] = {
                    "handle": each["handle"],
                    "username": each["username"],
                    "color": each["color"]}
        else:
            user = data["user"]
            self.userlist[user["_id"]] = {
                "handle": user["handle"],
                "username": user["username"],
                "color": user["color"]}
        print(self.userlist)

    async def getusers(self, room: str, iscmd: bool = False):
        res = await self.api.getroominfo(room)
        print(res)
        users = []
        j = json.loads(res)
        if len(j["users"]) > 0:
            for each in j["users"]:
                users.append(each["handle"])
            u = ", ".join(users)
            await self.sendmsg(f"Users in {room}: {u}")
        else:
            await self.sendmsg(f"{room} looks empty")

    def pacemaker(self):
        while True:
            if self.is_running:
                time.sleep(25)
                asyncio.run(self._ws.send("2"))

    def process_input(self):
        while True:
            if self.is_running:
                f = input()
                if f == "exit":
                    sys.exit()
                else:
                    asyncio.run(self.sendmsg(f))

    def process_message_queue(self):
        while True:
            if self.is_running:
                asyncio.run(asyncio.sleep(1))


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.pacemaker)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_input)
    try:
        await bot.run()
    except websockets.WebSocketException as e:
        bot.is_running = False

conf = "dev.toml"
executor = futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumJumpBot()

try:
    bot.settings = Configuration(conf)
except FileNotFoundError:
    from lib.config import generate_config, write_config
    generated = generate_config()
    towrite = write_config(generated, conf)
    if towrite:
        bot.settings = Configuration(conf)
    else:
        sys.exit("Configuration not loaded")

asyncio.get_event_loop().run_until_complete(start(executor, bot))
