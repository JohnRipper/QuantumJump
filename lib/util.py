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

from pathlib import Path

import aiohttp


def prompt(query: str) -> bool:
    options = ["y", "n"]
    check = input(f"{query} ").lower()
    if check not in options:
        return ValueError
    elif check == "y":
        return True
    else:
        return False


async def get_latest_sha1():
    url = "https://api.github.com/repos/JohnRipper/QuantumJump/commits"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            gitjson = await response.json()
            sha1 = gitjson[0]["sha"][:7]
            return sha1


def get_current_sha1():
    cwd = Path.cwd()
    headfile = Path(cwd / ".git/refs/heads/master")
    sha1 = "-Not in a git repository-"
    if headfile.exists():
        sha1 = headfile.read_text()[:7]
    return sha1
