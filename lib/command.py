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

import re

from lib.objects import Message, Role


def makeCommand(aliases: [], description: str, role: Role = None, **attrs):
    def wrap(f):
        f.__command__ = True
        f.__command_name__ = aliases
        f.__description__ = description
        if role:
            f.__role__ = role
            f.__restricted__ = True
        else:
            f.__restricted__ = False
        return f
    return wrap


command_pattern = "{}(\w+)(\\b.*)"


class Command:
    def __init__(self, prefix: str, data: Message):
        self.prefix = prefix
        self.data = data
        self.message = data.message
        self.name = ""

        parsed = re.search(
            command_pattern.format(self.prefix),
            self.message)
        if parsed is not None:
            self.name, self.message = parsed.groups()
            self.message = self.message.lstrip()



