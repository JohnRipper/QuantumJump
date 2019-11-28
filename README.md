# QuantumJump
A work in progress bot for [JumpInChat](https://jumpin.chat)

## Prerequisites
QuantumJump requires at least [Python 3.8](https://www.python.org/downloads/release/python-380/)

Optionally, you can use [pipenv](https://pipenv.readthedocs.io/en/latest/) to manage the 
[virtualenv](https://virtualenv.pypa.io/en/stable/)

A few Python modules are required:
- [websockets](https://github.com/aaugustin/websockets)
- [tomlkit](https://github.com/sdispater/tomlkit)
- [aiohttp](https://github.com/aio-libs/aiohttp/)
- [beautifulsoup4](https://code.launchpad.net/beautifulsoup)

QuantumJump is confirmed working on GNU/Linux, the status of operation on other operating systems is currently unknown.
Feel free to give it a go and report back.

## Installation
With `pipenv`
```
pipenv install
```
With `pip`
```
pip3.8 install --user websockets tomlkit aiohttp beautifulsoup4
```

## Running
With `pipenv`
```
pipenv run python run.py
```
With `python`
```
python3.8 run.py
```
Upon first run the bot will search for `config.toml`, if it doesn't exist it will walk you through configuration.


### Example Configuration
```toml
[bot]
nickname = "quantum"
password = "topsecret"
prefix = "!"
rainbow = true
roomname = "topsecret"
username = "notabot"

[modules]
enabled = ["Debug", "Urban", "Builtins", "Autourl", "Movie", "Fun", "Tokes"]
```

## Porting To QuantumJump
`makeCommand`
```py
@makeCommand(name="ping", description="Reply to ping")
async def replytoping(self, c: Command):
    await self.send_message("Pong!") # quantum: Pong!
    # or if you want third person
    await self.send_action("pongs") # *quantum pongs
```

`event`
```py
from lib.styling import Colors, Styles
@event(event="room::message")
async def message(self, message: Message):
    msg = message.message
    if "ping" in msg:
        # colorize or stylize your message
        await self.send_message("Pong!", color=Colors.red, style=Styles.script)
        # quantum: 𝓟𝓸𝓷𝓰! 
```

## Commands
```
-----Fun------
8ball: <query> standard magic 8ball
rate: <user> rate someones appearance
roll: <sides> <dice>, default is single 6 sided

-----Autourl------

-----Movie------
movie: <query> search The Movie Db for Movies
imdb: <query> search The Movie Db for TV and movies
tv: <query> search The Movie Db for TV shows

-----Tokes------
cheers: Cheers!
420hour: enables/disables call for tokes hourly.
timer: a seconds timer 
tokes: <int> calls for tokes

-----Builtins------
uptime: get the bot's uptime
version: get the current version

-----Urban------
urb: Search Urban Dictionary

-----Debug------
font: 
t: test
me: t
userlist: test


```
