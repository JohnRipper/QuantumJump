# QuantumJump

A work in progress bot for [JumpInChat](https://jumpin.chat)

## Prerequisites

⚠ Requires [Python 3.8.0+](https://www.python.org/downloads/release/python-382/) ⁠— you may need to [compile it yourself](https://tecadmin.net/install-python-3-8-ubuntu/)

Optionally, you can use [pipenv](https://pipenv.readthedocs.io/en/latest/) to manage the
[virtualenv](https://virtualenv.pypa.io/en/stable/)

A few Python modules are required:

- [websockets](https://github.com/aaugustin/websockets)
- [tomlkit](https://github.com/sdispater/tomlkit)
- [aiohttp](https://github.com/aio-libs/aiohttp/)
- [beautifulsoup4](https://code.launchpad.net/beautifulsoup)
- [wikipedia](https://github.com/goldsmith/Wikipedia)
- [aiohttp_socks](https://github.com/romis2012/aiohttp-socks) (Tor support)
- [pytz](https://pythonhosted.org/pytz/) (Wundertime support)

QuantumJump is confirmed working on GNU/Linux, the status of operation on other operating systems is currently unknown.
Feel free to give it a go and report back.

## Installation

With `pipenv`

```bash
pipenv install
```

With `pip`

```bash
pip3.8 install -U --user aiohttp aiohttp_socks beautifulsoup4 pytz tomlkit websockets wikipedia wolframalpha
```

## Running

With `pipenv`

```bash
pipenv run python run.py
```

With `python`

```bash
python3.8 run.py
```

Upon first run the bot will search for `config.toml`, if it doesn't exist it will walk you through configuration.

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

### Builitins

| Command | Argument | Description                        |
|---------|----------|------------------------------------|
| uptime  | N/A      | current uptime                     |
| version | N/A      | current version and latest version |
| timer   | seconds  | count down                         |

### Fun

| Command | Argument   | Description            |
|---------|------------|------------------------|
| roll    | sides dice | roll dice, default is 1 die, 6 sides |
| rate    | thing      | rate a thing out of 10 |
| 8ball   | question?  | standard magic 8ball   |

### Movie

| Command | Argument | Description |
|---------|----------|-------------|
| imdb    | query    | search [The Movie Db](https://www.themoviedb.org/documentation/api) for TV and movies |

### Tokes

| Command | Argument | Description                     |
|---------|----------|---------------------------------|
| 420hour | N/A      | toggle hourly 420 notifications |
| tokes   | seconds  | call tokes in a bit             |
| cheers  | N/A      | Cheers!                         |

### Youtube

| Command | Argument | Description |
|---------|----------|-------------|
| yt      | title or url |      play a video |

### Urban Dictionary

| Command | Argument | Description |
|---------|----------|-------------|
| urb     | query    | search Urban Dictionary |

## Contributors

### Thanks to those who have helped make quantum a thing

[`@rkben`](https://github.com/rkben)

[`@Tech`](https://github.com/Technetium1)
