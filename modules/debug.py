import json

from lib.cog import Cog, event
from lib.command import makeCommand, Command
from lib.objects import User, Status, HandleChange, Message, UpdateUserList
from lib.styling import Colors, Styles, encodetxt


class Debug(Cog):

    async def get_template(self):

        f = open('./data/help_template.md', 'r')
        text = f.read()
        command_data = ""

        for cog in self.bot.cm.cogs.values():
            command_data += f"-----{cog.name}------\n"
            for command in cog.commands:
                command_data += f"{getattr(command, '__command_name__')}: {getattr(command, '__description__')}\n"
            command_data += "\n"
        text = text.format(commands=command_data)
        f.close()
        return text

    @makeCommand(name="t", description="test")
    async def generate_readme(self, c: Command):
        generated = await self.get_template()
        f = open('./README.md', 'w')
        f.write(generated)
        f.flush()
        f.close()


    @makeCommand(name="userlist", description="test")
    async def vagina(self, c: Command):
        await self.send_message(json.dumps(await self.bot.userlist))
        #await self.send_message("Test")

    @makeCommand(name="me", description="t")
    async def thirdperson(self, c: Command):
        await self.send_action(c.message)

    @makeCommand(name="font", description="")
    async def demofonts(self, c: Command):
        parts = c.message.split(" ")
        type_ = parts[0]
        message = " ".join(parts[1:])
        if type_ in Styles.__dict__.keys():
            formated = encodetxt(message, Styles.__dict__[type_])
        else:
            formated = encodetxt(c.message, Styles.script)
        await self.send_message(formated)

    @makeCommand(name="whoami", description="")
    async def whoami(self, c: Command):
        users = await self.bot.userlist
        print(a)

    @makeCommand(name="test", description="")
    async def testit(self, c: Command):
        await self.send_message(self.settings["test"])
    #####
    # Events
    #####

    @event(event="room::message")
    async def message(self, message: Message):
        print(message.message)
        pass

    @event(event="room::updateUserList")
    async def updateUserList(self, userlist: UpdateUserList):
        print("that" + userlist.user.handle)
        pass
