from dataclasses import make_dataclass
from pathlib import Path
from util import prompt
from tomlkit import loads as tomlload
from tomlkit import dumps as tomldump

default = {
    "bot": {
        "username": str,
        "password": str,
        "roomname": str,
        "nickname": str,
    },
}


class Configuration:
    def __init__(self, path: str):
        self.path = Path(path)
        if self.path.exists():
            self.full = self.load()
            self.Bot = make_dataclass(
                "Bot_Configuration",
                [(k, type(v), v)
                    for k, v in self.full["bot"].items()]
            )
            self.Modules = None
        else:
            raise FileNotFoundError(path)

    def load(self) -> dict:
        config = tomlload(self.path.read_text())
        return config

def generate_config():
    config = default.copy()
    botsettings = config["bot"]
    for each in botsettings.keys():
        botsettings[each] = input(f"Please enter your {each}: ")
    return tomldump(config)

def write_config(config: str, path: str) -> bool:
    check = prompt(f"\n{config}\nDoes this look correct? y/N")
    if check is False:
        return False
    else:
        path = Path.cwd() / path
        with open(path, "w") as toml:
            toml.write(config)
        return True
