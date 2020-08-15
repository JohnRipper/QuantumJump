# -*- coding: utf-8 -*-
#
# Copyright 2020, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by tech 8/1/20
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

import asyncio
from lib.cog import Cog, event
from lib.objects import Message

from dhooks import Webhook
from dhooks import Embed


class Relay(Cog):
    # def __init__(self, bot):
    # super().__init__(bot)
    # don't need to do this to get bot config as it's imported from Cog as bot_settings

    @event("room::message")
    async def relay(self, message: Message):
        d_webhookurl = self.settings["d_webhookurl"]
        embed_hook = self.settings["embed_hook"]
        roomname = self.bot_settings.roomname

        msgprofile = message.sender.username
        msgnick = message.handle
        msg = message.message

        jumpinurl = f"https://jumpin.chat/{roomname}"
        giticon = "https://image.flaticon.com/icons/png/512/25/25231.png"
        jprofilepic = f"https://s3.amazonaws.com/jic-uploads/room-display/display-{roomname}.png"

        async with Webhook.Async(
            url=d_webhookurl,
            username="Jumpin Relay",
            avatar_url=jprofilepic,
        ) as hook:
            if embed_hook and msgnick != self.bot_settings.nickname or None:
                em = Embed(
                    title=roomname.title,
                    url=jumpinurl,
                    timestamp="now",
                    color="#00FF00",
                    image_url="https://i.imgur.com/BiUki4F.png",
                    thumbnail_url=jprofilepic,
                )
                em.set_footer(text="via git.io/QuantumJump", icon_url=giticon)
                if msgnick != self.bot_settings.nickname:
                    em.add_field(
                        name=f"**__{msgnick}__** ({msgprofile}):",
                        value=f"`{msg}`",
                        inline=False,
                    )
                # await hook.send(embeds=[em])
            elif embed_hook is False and msgnick != self.bot_settings.nickname or None:
                await asyncio.sleep(1.1)
                await hook.send(f"**__{msgnick}__** ({msgprofile}): `{msg}`")
            else:
                raise Exception("WEBHOOK FAILED TO SEND!")

