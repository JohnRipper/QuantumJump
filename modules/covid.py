# -*- coding: utf-8 -*-
#
# Copyright 2020, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 3/28/20
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
import json
import random
from datetime import date
from difflib import get_close_matches

from attr import dataclass

from lib.cog import Cog
from lib.command import Command, makeCommand


@dataclass
class World:
    updated: int
    cases: int
    todayCases: int
    deaths: int
    todayDeaths: int
    recovered: int
    todayRecovered: int
    active: int
    critical: int
    casesPerOneMillion: int
    deathsPerOneMillion: int
    tests: int
    testsPerOneMillion: int
    population: int
    oneCasePerPeople: int
    oneDeathPerPeople: int
    oneTestPerPeople: int
    activePerOneMillion: int
    recoveredPerOneMillion: int
    criticalPerOneMillion: int
    affectedCountries: int


@dataclass
class CountryInfo:
    _id: int
    iso2: str
    iso3: str
    lat: int
    long: int
    flag: str


@dataclass
class Country:
    updated: int
    country: str
    countryInfo: CountryInfo
    cases: int
    todayCases: int
    deaths: int
    todayDeaths: int
    recovered: int
    todayRecovered: int
    active: int
    critical: int
    casesPerOneMillion: int
    deathsPerOneMillion: int
    tests: int
    testsPerOneMillion: int
    population: int
    continent: str
    oneCasePerPeople: int
    oneDeathPerPeople: int
    oneTestPerPeople: int
    activePerOneMillion: int
    recoveredPerOneMillion: int
    criticalPerOneMillion: int


@dataclass
class State:
    state: str
    updated: int
    cases: int
    todayCases: int
    deaths: int
    todayDeaths: int
    active: int
    casesPerOneMillion: int
    deathsPerOneMillion: int
    tests: int
    testsPerOneMillion: int


class Covid(Cog):
    WORLD = "https://corona.lmao.ninja/v2/all"
    COUNTRY = "https://corona.lmao.ninja/v2/countries"
    STATES = "https://corona.lmao.ninja/v2/states"

    def __init__(self, bot):
        super().__init__(bot)

    @makeCommand(aliases=["world"], description="covid's world kdr")
    async def world(self, c: Command):
        data = await self.bot.api.get(self.WORLD)
        data = World(**json.loads(await data.text()))
        updated = date.fromtimestamp(int(data.updated) / 1000).strftime('%Y-%m-%d %H:%M')
        message = f"Updated:{updated} Cases:{data.cases} CasesToday:{data.todayCases} 💀:{data.deaths} 💀Today:{data.todayDeaths} Recovered:{data.recovered} RecoveredToday:{data.todayRecovered} Active:{data.active} Critical:{data.critical} Cases/1M:{data.casesPerOneMillion} 💀/1M:{data.deathsPerOneMillion} Tests:{data.tests} Tests/1M:{data.testsPerOneMillion} Pop:{data.population} 1Case/People:{data.oneCasePerPeople} 1💀/People:{data.oneDeathPerPeople} 1Test/People:{data.oneTestPerPeople} ActivePer1M:{data.activePerOneMillion} RecoveredPer1M:{data.recoveredPerOneMillion} CriticalPer1M:{data.criticalPerOneMillion} Countries:{data.affectedCountries}"
        await self.send_message(message)

    @makeCommand(aliases=["country", "where"], description="<country name> covid's country kdr")
    async def cwhere(self, c: Command):
        data = await self.bot.api.get(self.COUNTRY)
        data = json.loads(await data.text())
        # data = CountryInfo(**data)
        if c.message == "":
            await self.send_message("This command needs a country name")

        myDict = {}

        for country_data in data:
            country = country_data['country']
            # cool enough to use abbreviations fix.
            if country == 'usa':
                myDict['united states'] = country_data

            myDict[country] = country_data
        matches = get_close_matches(c.message, myDict.keys(), 1, .4)

        if myDict[matches[0]]:
            country = Country(**myDict[matches[0]])
            await self.send_message(country.__repr__())
            return
        await self.send_message("Not Found!")

    @makeCommand(aliases=["randomc", "randc", "crand"], description="<country name> covid's random country kdr")
    async def crandom(self, c: Command):
        data = await self.bot.api.get(self.COUNTRY)
        data = json.loads(await data.text())
        randomly_picked = random.choice(data)
        country = Country(**randomly_picked)
        await self.send_message(country.__repr__())

    @makeCommand(aliases=["state"], description="<state name> covid's random state kdr")
    async def cstate(self, c: Command):
        data = await self.bot.api.get(self.STATES)
        data = json.loads(await data.text())
        if c.message == "":
            await self.send_message("This command needs a state name")
        for state_data in data:
            if state_data.get("state").title() == c.message.title():
                state = State(**state_data)
                await self.send_message(state.__repr__())
                return
        # todo, support for inexact names? South Dakota
        await self.send_message("Not Found!")

    @makeCommand(aliases=["randoms", "rands", "srand", "srandom"], description="<state name> covid's random states kdr")
    async def srandom(self, c: Command):
        data = await self.bot.api.get(self.STATES)
        data = json.loads(await data.text())
        randomly_picked = random.choice(data)
        country = State(**randomly_picked)
        await self.send_message(country.__repr__())
