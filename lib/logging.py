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
import os
import sys
from logging import LogRecord, addLevelName, getLoggerClass, setLoggerClass, Filter, Formatter, FileHandler, \
    StreamHandler

from lib.terminal_color import teal, pink, orange, white, green, lime, blue

dir_path = os.path.dirname(os.path.realpath(__file__))


class ChatFilter(Filter):
    def filter(self, record: LogRecord):
        msg = record.msg
        if isinstance(msg, str):
            if record.levelno == QuantumLogger.CHAT:
                return True
            if record.levelno == QuantumLogger.INFO:
                return True
        return False


class DebugFilter(Filter):
    def filter(self, record: LogRecord):
        msg = record.msg
        if isinstance(msg, str):
            if record.levelno == QuantumLogger.CHAT:
                return False
        return True


class QuantumFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        s = self.formatMessage(record)
        # THERES PROBABLY A BETTER WAY, but would also have to rework LogRecords and I am feeling lazy
        s = s.replace(" INFO ", blue(" INFO "))
        s = s.replace(" _CHAT ", teal(" CHAT "))
        s = s.replace(" _RECV ", green(" RECV "))
        s = s.replace(" _SENT ", lime(" SENT "))

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


terminal_formatter = QuantumFormatter(
    f"{pink('%(asctime)s')} - {orange('%(name)s')} - %(levelname)s - {white('%(message)s')}")
file_formatter = Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class QuantumLogger(getLoggerClass()):
    # custom levels
    CHAT = 19
    RECV = 14
    SENT = 15

    # logger levels
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    _choices = ((CHAT, "chat"),
                (DEBUG, "debug"),

                (INFO, "info"),
                (WARNING, "warning"),
                (ERROR, "error"))

    shortcodes = {
        "i": INFO,
        "c": CHAT,
        "d": DEBUG,
        "w": WARNING,
        "e": ERROR
    }

    def __init__(self, name, room_name="None", level=10, cleaner_log=True):
        super().__init__(name, level)
        self.room_name = room_name
        addLevelName(self.CHAT, "_CHAT")
        addLevelName(self.RECV, "_RECV")
        addLevelName(self.SENT, "_SENT")

        self.chat_handler_enabled = cleaner_log

        # default is info
        self.set_level(level)

    def ping(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PING):
            self._log(self.PING, msg, args, **kwargs)

    def pong(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PONG):
            self._log(self.PONG, msg, args, **kwargs)

    def chat(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.CHAT):
            self._log(self.CHAT, msg, args, **kwargs)



    def ws_event(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.RECV):
            self._log(self.RECV, msg, args, **kwargs)

    def ws_send(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.SENT):
            self._log(self.SENT, msg, args, **kwargs)

    def remove_handlers(self):
        for handler in self.handlers:
            self.removeHandler(handler)

    def date_suffix(self):
        # TODO for use in log file names for better organization.
        # TODO seperated by Daily logs?
        return

    def add_chat_handler(self):
        # TODO better log file names. ^^ see above ^^ Also apply filter
        file_name = f"logs/chat.log"
        # create if doesnt exist
        open(os.path.join(dir_path, "..", f'{file_name}'), 'a').close()
        handler = FileHandler(filename=file_name)
        # apply filter
        handler.addFilter(ChatFilter())
        self.addHandler(handler)

    def set_level(self, level: int):
        self.setLevel(level)
        for chosen_level in self._choices:
            if level == chosen_level[0]:
                # reset handlers
                self.remove_handlers()
                stream_handler = StreamHandler(sys.stdout)
                stream_handler.setLevel(level)

                file_name = f"logs/{self.room_name}/{chosen_level[1]}.log"
                if not os.path.exists(f"logs/{self.room_name}/"):
                    os.mkdir(f"logs/{self.room_name}/")

                file_handler = FileHandler(filename=f"logs/{self.room_name}/{chosen_level[1]}.log")
                file_handler.setLevel(level)
                file_handler.setFormatter(file_formatter)

                # secondary log file that contains only messages.
                if self.level == self.CHAT:
                    self.add_chat_handler()
                    stream_handler.addFilter(ChatFilter())
                    stream_handler.setFormatter(terminal_formatter)

                else:
                    stream_handler.addFilter(DebugFilter())
                    stream_handler.setFormatter(terminal_formatter)

                    if self.chat_handler_enabled:
                        self.add_chat_handler()

                self.addHandler(file_handler)

                # log to the terminal.

                self.addHandler(stream_handler)
                return True
        # level was not set
        return False


setLoggerClass(QuantumLogger)