from collections import Set

import discord
from discord import Guild, Client, Message, TextChannel, Role

import os


class MyClient(Client):
    server: Guild = None
    color_channel: TextChannel = None
    role_names: Set[str] = set()

    async def on_ready(self):
        self.server = self.get_guild("599611697464082434")
        self.color_channel = self.server.get_channel("599640898233565198")
        self.role_names = {"red", "yellow", "black", "maroon", "darkred", "brown", "firebrick", "crimson", "tomato",
                           "coral", "indianred", "lightcoral", "darksalmon", "salmon", "lightsalmon", "orangered",
                           "darkorange", "orange", "gold", "darkgoldenrod", "goldenrod", "palegoldenrod", "pink",
                           "lightpink", "hotpink", "deeppink", "darkkhaki", "palevioletred", "khaki",
                           "mediumvioletred", "orchid", "olive", "magenta", "violet", "plum", "thistle",
                           "purple", "yellowgreen", "darkolivegreen", "olivedrab", "mediumorchid", "lawngreen",
                           "darkorchid", "darkviolet", "darkmagenta", "mediumpurple", "mediumslateblue", "greenyellow",
                           "slateblue"}
        await self.change_presence(activity=discord.Game(name='with your feelings.'))
        print(f'Ready, we have logged in as {self.user.name}!')

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.channel.id == self.color_channel.id:
            content = message.content.lower()
            if content in self.role_names:
                new_role = discord.utils.get(self.server.roles, name=content)
                if isinstance(new_role, Role):
                    await message.delete()
                    toremove = []
                    for role in message.author.roles:
                        if role.name in self.role_names:
                            toremove.append(role)
                    for role in toremove:
                        await message.author.remove_roles(role)
                    await message.author.add_roles(new_role)
                    await message.author.send_message(
                        embed=discord.Embed(
                            title=f"You successfully changed your color to **{new_role}**.",
                            description="Enjoy your new color! | Nexus",
                            color=new_role.colour))
            elif content == "none":
                toremove = []
                for role in message.author.roles:
                    if role.name in self.role_names:
                        toremove.append(role)
                for role in toremove:
                    await message.author.remove_roles(role)
                await message.author.send_message(
                    embed=discord.Embed(
                        title=f"You successfully changed your color to **No color!**.",
                        description="Enjoy your new ~~(not actually a)~~ color! | Nexus"))
            else:
                await message.author.send_message(
                    ":x: | You entered an invalid color.\n"
                    "Please note that the colors are case sensitive, so spell them as you see them.")
                await message.delete()


client = MyClient()
client.run(os.environ.get("token"))
