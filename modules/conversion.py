from lib.cog import Cog
from lib.command import Command, makeCommand


class Conversion(Cog):
    @makeCommand(aliases=["t", "temp"], description="Convert a temp")
    async def convert_temp(self, c: Command):
        units = ["f", "c"]
        from_unit = c.message[-1].lower()
        if from_unit in units and from_unit == "f":
            toconvert = from_unit.rstrip("f")
            # strip '-' for negative numbers before checking if its a digit
            if toconvert.lstrip("-").isdigit():
                converted = (int(toconvert) - 32) * 5 / 9
                fmt = ":thermometer: {}°F is {}°C".format(
                    toconvert, round(converted))
                await self.send_message(fmt)
            pass
        elif from_unit in units and from_unit == "c":
            toconvert = from_unit.rstrip("c")
            if toconvert.lstrip("-").isdigit():
                converted = int(toconvert) * 1.8 + 32
                fmt = ":thermometer: {}°C is {}°F".format(
                    toconvert, round(converted))
                await self.send_message(fmt)
        else:
            await self.send_action("doesn't think that is a valid unit")
