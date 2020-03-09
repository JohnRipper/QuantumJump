# -*- coding: utf-8 -*-
#
# Copyright 2020, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 3/8/20
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

# printf "\x1b[38;2;255;100;0mTRUECOLOR\x1b[0m\n"

YELLOW = "fdd365"
PINK = "fd2eb3"
ORANGE = "fb8d62"
TEAL = "61d4b3"
RED = "d63447"
WHITE = "f6eedf"
GREEN = "216353"
LIME = "75daad"
BLUE = "CCE5FF"


def color(text: str, r: int = None, g: int = None, b: int = None, hexcode: str = None) -> str:
    # can handle both rgb, and hex codes, prefers hexcode.
    if hexcode:
        r, g, b = hex_to_rgb(hexcode)
    assert r < 255 or r > 0, "r color value is out of range"
    assert g < 255 or g > 0, "g color value is out of range"
    assert b < 255 or b > 0, "b color value is out of range"
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"


def hex_to_rgb(hex: str) -> list:
    assert len(hex) == 6
    return [int(hex[i:i + 2], 16) for i in range(0, len(hex), 2)]


# info
def blue(text: str) -> str:
    value = hex_to_rgb(BLUE)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# warning
def yellow(text: str) -> str:
    value = hex_to_rgb(YELLOW)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# errors
def red(text: str) -> str:
    value = hex_to_rgb(RED)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# recv
def green(text: str) -> str:
    value = hex_to_rgb(GREEN)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# sent
def lime(text: str) -> str:
    value = hex_to_rgb(LIME)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# chat
def teal(text: str) -> str:
    value = hex_to_rgb(TEAL)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# time
def pink(text: str) -> str:
    value = hex_to_rgb(PINK)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr


# logger name
def orange(text: str) -> str:
    value = hex_to_rgb(ORANGE)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return color(text=text, hexcode=ORANGE)


# message
def white(text: str) -> str:
    value = hex_to_rgb(WHITE)
    fstr = color(text=text, r=value[0], g=value[1], b=value[2])
    return fstr
