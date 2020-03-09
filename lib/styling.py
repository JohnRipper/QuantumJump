# -*- coding: utf-8 -*-
#
# Copyright 2019, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 2/8/20
# This file is part of QuantumJump.
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
    bolditalic: dict = fonts.BOLD_ITALIC
    bubble: dict = fonts.BUBBLE
    bubbleinvert: dict = fonts.BUBBLE_NEG
    square: dict = fonts.SQUARE
    squareinvert: dict = fonts.SQUARE_NEG
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
