from dataclasses import make_dataclass
from pathlib import Path

from tomlkit import dumps as tomldump
from tomlkit import loads as tomlload

from util import prompt

default = {
    "bot": {
        "username": str,
        "password": str,
        "roomname": str,
        "nickname": str,
        "prefix": str,
        "rainbow": bool
    },
    "Modules": {
        "enabled": []
    }
}


class Configuration:
    def __init__(self, path: str):
        self.path = Path(path)
        if self.path.exists():
            self.full = self.load()
            print(self.full)
            self.Bot = make_dataclass("Bot_Configuration",
                                      [(k, type(v), v)
                                       for k, v in self.full["Bot"].items()])
            print(self.Bot)
            self.Modules = self.full["Modules"]
        else:
            raise FileNotFoundError(path)

    def load(self) -> dict:
        config = tomlload(self.path.read_text())
        return config


def getmodules() -> list:
    modules = []
    module_files = Path("modules/").glob("*.py")
    for each in module_files:
        module = each.name.rstrip(".py").capitalize()
        modules.append(module)
    return modules


def generate_config():
    config = default.copy()
    botsettings = config["bot"]
    for each in botsettings.keys():
        if botsettings[each] == bool:
            botsettings[each] = prompt(f"Would you like to enable {each}? y/N ")
        else:
            botsettings[each] = input(f"Please enter your {each}: ")
    modules = getmodules()
    print(
        "Enter the number for each module you'd like to enable, separated by commas"
    )
    print("Example: 1,5,8")
    message = ", ".join([f"{i}) {v}" for i, v in enumerate(modules)])
    to_enable = input(f"{message}\n")
    for module_index in to_enable.split(","):
        if module_index.isdigit() and int(module_index) <= len(modules):
            config["modules"]["enabled"].append(modules[int(module_index)])
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
