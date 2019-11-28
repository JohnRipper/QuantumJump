import random
from dataclasses import dataclass, asdict
from typing import Callable


@dataclass
class Colors:
    red: str = "red"
    redalt: str = "redalt"
    green: str = "green"
    greenalt: str = "greenalt"
    yellow: str = "yellow"
    yellowalt: str = "yellowalt"
    blue: str = "blue"
    bluealt: str = "bluealt"
    purple: str = "purple"
    purplealt: str = "purplealt"
    aqua: str = "aqua"
    aquaalt: str = "aquaalt"
    orange: str = "orange"
    orangealt: str = "orangealt"
    _all: set = ("red", "redalt", "green", "greenalt", "yellow", "yellowalt",
                 "blue", "bluealt", "purple", "purplealt", "aqua", "aquaalt",
                 "orange", "orangealt")
    random: Callable = lambda: random.choice(Colors._all)


@dataclass
class Styles:
    # format(str)
    bold: str = "*{}*"
    italic: str = "_{}_"
