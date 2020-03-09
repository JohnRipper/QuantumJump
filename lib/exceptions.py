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


# subclass for general Exceptions
class Error(Exception):
    def __init__(self, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {message}")
        else:
            print(self.__class__.__name__)


class InvalidLogin(Error):
    pass


class HttpStatus(Exception):
    def __init__(self, code: int, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {code}:{message}")
        else:
            print(f"{self.__class__.__name__}: {code}")


class CogException(Exception):
    def __init__(self, code: int, message: str = None):
        if message:
            print(f"{self.__class__.__name__}: {code}:{message}")
        else:
            print(f"{self.__class__.__name__}: {code}")