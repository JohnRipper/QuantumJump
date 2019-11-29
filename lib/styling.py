import random
import re
from dataclasses import dataclass
from typing import Callable

# import unidecode
from lib import fonts


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


class Styles:
    bold: dict = fonts.BOLD
    italic: dict = fonts.ITALIC
    bold_italic: dict = fonts.BOLD_ITALIC
    bubble: dict = fonts.BUBBLE
    bubble_invert: dict = fonts.BUBBLE_NEG
    square: dict = fonts.SQUARE
    square_invert: dict = fonts.SQUARE_NEG
    script: dict = fonts.SCRIPT

# TODO
# def decodetxt(text: str) -> str:
#     decoded_text = unidecode(text)
#     return decoded_text


def encodetxt(text: str, style=None) -> str:
    emoji = re.findall(":\w*:", text)
    for each in emoji:
        text = re.sub(each, "{}", text)
    characters = list(text)
    for position, char in enumerate(characters):
        if char in style.keys():
            characters[position] = style[char]
    return ''.join(characters).format(*emoji)
