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

import asyncio
import random

from lib.cog import Cog
from lib.command import makeCommand, Command


class DeathBattle(Cog):
    BATTLECRIES = [
        '{} beats up {} with a baseball bat for {} damage.',
        '{} blows up {} with a nuke for {} damage.',
        '{} beats up {} with his fists for {} damage.',
        '{} beats up {} with a resinated bong for {} damage.',
        '{} runs over {} with a shitty car for {} damage.',
        '{} runs over {} with a bicycle for {} damage.',
        '{} runs over {} with a bicycle, but misses and just slaps him with it instead for {} damage.',
        '{} runs over {} with a motorcycle for {} damage.',
        '{} runs over {} with a motorcycle, but misses and just slaps him with it instead for {} damage.',
        '{} runs over {} with a tricycle for {} damage.',
        '{} runs over {} with a tricycle, but misses and just slaps him with it instead for {} damage.',
        '{} runs over {} with a dirtbike for {} damage.',
        '{} runs over {} with a skateboard for {} damage.',
        '{} runs over {} with a stampede of elephants for {} damage.',
        '{} runs over {} with a army of mice for {} damage.',
        '{} runs over {} with a army of hoes for {} damage.',
        '{} runs over {} with a herd of hippopotomus for {} damage.',
        '{} runs over {} with a herd of cows for {} damage.',
        '{} hits {} with a tuna fish for {} damage.',
        '{} hits the bong then hits {} with the bong and does {} damage.',
        '{} hits {} with brass knuckles for {} damage.',
        '{} hits {} with a dirty bong for {} damage.',
        '{} hits {} with a dirty hoe for {} damage.',
        '{} hits {} with pizza for {} damage.',
        '{} burns {} with a joint for {} damage.',
        '{} burns {} with a joke for {} damage.',
        '{} burns {} with a torch for {} damage.',
        '{} burns {} with a lighter for {} damage.',
        '{} burns {} with a cig for {} damage.',
        '{} insults {} with a lame comeback for {} damage.',
        '{} smacks {} with his bong for {} damage.',
        '{} smacks this mothafucka {}, with anotha mothafucka {} damage.',
        '{} smacks this fucktart {}, with anotha fucktart {} damage.',
        '{} smacks this hoe {}, with anotha hoe {} damage.',
        '{} smashes {} face in with a beer glass for {} damage.',
        '{} smashes {} face in with dogshit for {} damage.',
        '{} smashes {} face in with a bong for {} damage.',
        '{} stabs {} with a steak knife and does {} damage.',
        '{} stabs {} with a sword and does {} damage.',
        '{} slashes {} with a sword and does {} damage.',
        '{} slashes {} with an old sword and does {} damage.',
        '{} slashes {} with a rusty katana and does {} damage.',
        '{} slashes {} with a katana and does {} damage.',
        '{} stabs {} with a a broken bong and does {} damage.',
        '{} stabs {} with a a broken beer bottle and does {} damage.',
        '{} punches {} in the nuts for {} damage.',
        '{} punches {} in the face for {} damage.',
        '{} bites {} and does {} damage.',
        '{} sets {} on fire and does {} damage.',
        '{} sets {} on fire with a flamethrower and does {} damage.',
        '{} poisons {} dabs and does {} damage.',
        '{} poisons {} food and does {} damage, as well as giving him a case of the shits.',
        '{} punches {} in the gut for {} damage.',
        '{} gives {} a wedgie and does {} damage.',
        '{} gives {} a super wedgie and does {} damage.',
        '{} gives {} a SUUUUPPPERR wedgie or brown stain death and does {} damage.',
        '{} dropkicks {} in the chest for {} damage.',
        '{} falcon punches {} for {} damage.',
        '{} throws feces at {} for {} damage.',
        '{} throws dabs at {} for {} damage.',
        '{} throws a cat at {} for {} damage.',
        '{} uses his nunchucks to disable {} for {} damage.',
        '{} uses pokemon move Submission on {} for {} damage. It is super effective.',
        '{} throws a keg at {} for {} damage.',
        '{} throws burning acid at {} for {} damage.',
        '{} throws a bong at {} for {} damage.',                                            
        '{} throws a beehive at {} for {} damage.',
        '{} pours molten lava over {} for {} damage.',
        '{} fires an arrow at {} for {} damage.',
        '{} fires an rpg at {} for {} damage.',
        '{} launches a gofundme to help with {}\'s stupidity problem for {} damage.',
        '{} launches a cyber-attack against {} for {} damage.',
        '{} launches a kamehameha against {} for {} damage.',
        '{} launches a super kamehameha against {} for {} damage.',
        '{} does witch craft and summons a ghost to haunt {} for {} damage.',
        '{} strangles {} with string cheese for {} damage.',
        '{} strangles {} with beef jerky for {} damage.',
        '{} throws a pickup truck at {} for {} damage.',
        '{} throws a spider at {} for {} damage. He screamed like a girl.',
        '{} throws pussy at {} for {} damage.',
        '{} throws gnarly pussy at {} for {} damage.',
        '{} farts on {} for {} damage.',
        '{} slaps {} for {} damage.',
        '{} summons a demon to attack {} for {} damage.',
        '{} summons cthulu to smite {} for {} damage.',
        '{} summons a digimon to attack {} for {} damage.',
        '{} summons a pokemon to attack {} for {} damage.',
        '{} summons el chapo to attack {} for {} damage.',
        '{} summons trump to deport {} for {} damage.',
        '{} pocket-sands {} for {} damage.',
        '{} performs voodoo on {} for {} damage.',
        '{} drops a piano on {} for {} damage.',
        '{} drops a boulder on {} that does {} damage.',
        '{} ties {} to a rocket and launches him, causing {} damage.',
        '{} slaps {} with a chainsaw and does {} damage.',
        '{} makes {} slap himself and does {} damage.',
        '{} makes {} bitchslap himself and does {} damage.',
        '{} slaps {} with a retro game system for {} damage.',
        '{} bitchslaps {} for {} damage.',
        '{} smacks {} with his bong for {} damage.',
        '{} nukes {} for {} damage.',
        '{} shoots at {} with an ak-47 for {} damage.',
        '{} launches a neo-nazi anti-feminist campaign against {} for {} damage.',
        '{} shoots at {} with a paintballgun for {} damage.',
        '{} fires an catapult at {} for {} damage.',
        '{} fires an rpg at {} for {} damage.',
        '{} stings {} with the fish that killed steve irwin for {} damage.',
        '{} hacks {} and exposes the awful truth for {} damage.',
        '{} eats all of {}\'s bacon and causes {} points worth of emotional trauma damage.',
        '{} drinks all of {}\'s beer and causes {} points worth of emotional trauma damage.',
        '{} smokes all of {}\'s dabs and causes {} points worth of emotional trauma damage.',
        '{} smokes all of {}\'s marijuana and causes {} points worth of emotional trauma damage.',
        '{} shaves {}\'s head and causes {} points worth of emotional trauma damage.',
        '{} uses his words and hurts {}\'s feelings causing {} points worth of emotional trauma damage.',
        '{} makes fun of {} and causes {} points worth of emotional trauma damage.',
        '{} exposes {} deepest darkest secret and causes {} points worth of emotional trauma damage.',
    ]
    @makeCommand(aliases=["md", "dmc"], description="<opponent name> measure dicks")
    async def md(self, c: Command):
        if c.message:

            length_one = "".ljust(random.randint(0, 100), "=")
            length_two = "".ljust(random.randint(0, 100), "=")
            await self.send_message(f"8{length_one}D  ~ ~ {c.data.handle} ~ ~")
            await self.send_message(f"8{length_two}D  ~ ~ {c.message} ~ ~")
            if length_one > length_two:
                await self.send_message(f"{c.data.handle} has a bigger dick")
            elif length_one < length_two:
                await self.send_message(f"{c.message} has a bigger dick")
            elif length_one == length_two:
                await self.send_message(f"DICK TWINS!!!!!!!!!!")
        else:
            await self.send_message(f"you need a bro to help you measure... for reasons. ")

    @makeCommand(aliases=["battle", "deathbattle"], description="attack in death battle")
    async def boop(self, c: Command):
        if c.message:
            player_one_damage = random.randint(0, 100)
            data = random.choice(self.BATTLECRIES).format(c.data.handle, c.message, player_one_damage)
            await self.send_message(data)
            await asyncio.sleep(.01)

            player_two_damage = random.randint(0, 100)
            data = random.choice(self.BATTLECRIES).format(c.message, c.data.handle, player_two_damage)
            await self.send_message(data)
            gold_stolen = random.randint(0, 42)
            await asyncio.sleep(.01)

            if player_one_damage > player_two_damage:
                await self.send_action(f"{c.data.handle} wins {gold_stolen} gold!")
            else:
                await self.send_action(f"{c.message} wins {gold_stolen} gold!")

    @makeCommand(aliases=["attack"], description="<opponent name> attack in death battle")
    async def attack(self, c: Command):
        if c.message:
            player_one_damage = random.randint(0, 100)
            data = random.choice(self.BATTLECRIES).format("_prefbot_", c.message, player_one_damage)
            await self.send_message(data)
            await asyncio.sleep(.01)

            player_two_damage = random.randint(0, 100)
            data = random.choice(self.BATTLECRIES).format(c.message, c.data.handle, player_two_damage)
            await self.send_message(data)
            gold_stolen = random.randint(0, 42)
            await asyncio.sleep(.01)

            if player_one_damage > player_two_damage:
                await self.send_action(f"_prefbot_ wins {gold_stolen} gold!")
            else:
                await self.send_action(f"{c.message} wins {gold_stolen} gold!")
