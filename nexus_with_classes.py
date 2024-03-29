import datetime
import os
from typing import Optional, Set

import discord
from discord import Client, Message, Guild, Member


class MyClient(Client):
    guild: Guild = None
    role_names: Set[str] = set()
    cant_member: Optional[Member] = None
    ALL_THE_PINGS: Set[str] = set()

    async def on_ready(self):
        self.guild = self.get_guild(599611697464082434)

        self.role_names = {"red", "yellow", "black", "maroon", "darkred", "brown", "firebrick", "crimson", "tomato",
                           "coral", "indianred", "lightcoral", "darksalmon", "salmon", "lightsalmon", "orangered",
                           "darkorange", "orange", "gold", "darkgoldenrod", "goldenrod", "palegoldenrod", "pink",
                           "lightpink", "hotpink", "deeppink", "darkkhaki", "palevioletred", "khaki", "mediumvioletred",
                           "orchid", "olive", "magenta", "violet", "plum", "thistle", "purple", "yellowgreen",
                           "darkolivegreen", "olivedrab", "mediumorchid", "lawngreen", "darkorchid", "darkviolet",
                           "darkmagenta", "mediumpurple", "mediumslateblue", "greenyellow", "slateblue"}

        self.cant_member = self.guild.get_member(393839495859929089)

        self.ALL_THE_PINGS = {
            self.guild.get_member(232553089658388481).mention,
            self.guild.get_member(444029889063026688).mention,
            self.guild.get_member(535844642776940555).mention,
            self.guild.get_member(164118147073310721).mention,
            self.guild.get_member(237938976999079948).mention
        }

        await self.change_presence(activity=discord.Game(name='with your feelings.'))
        print('Ready!')

    async def on_message(self, message: Message):
        #print("Received message from channel " + str(message.channel))
        if message.content == "!ping":
            await ping(message)
        elif message.content == "!servericon":
            await servericon(message)
        #elif message.author != self.cant_member and (
        #        self.cant_member in message.mentions or message.content == "!test_ping"):
        #    await message.author.send(f"Hello, this message is brought to you by {', '.join(self.ALL_THE_PINGS)}!\n"
        #                              f"You have pinged {self.cant_member.mention}!\n"
        #                              f"Have a good day!")
        #    await message.channel.send(
        #        f"{message.author.mention}, that's not cool, you know.\n"
        #        f"If you just pinged her for **literally nothing**, you'll beg for forgiveness.")
        elif message.content.startswith("!echo"):
            await message.channel.send(message.author.mention + ": " + message.content[6:])
        elif message.channel.id == 599640898233565198:
            print("Message is in the right channel!")
            print("Trying to matching message to a role... Message:" + message.content)
            if message.content in self.role_names:
                new_role = discord.utils.get(self.guild.roles, name=message.content)
                if hasattr(new_role, "id"):
                    await message.delete()
                    print("We have a match! Role:" + new_role.name)
                    print("Checking colored roles to remove...")
                    toremove = []
                    for role in message.author.roles:
                        if role.name in self.role_names:
                            toremove.append(role)
                    print("Removing colored roles...")
                    for role in toremove:
                        print("removing" + role.name)
                        await message.author.remove_roles(role)
                    print("Adding " + new_role.name + " role...")
                    await message.author.add_roles(new_role)
                    print("Great success!")
                    embed = discord.Embed(title=f"You successfully changed your color to **{str(new_role)}**.",
                                          description="Enjoy your new color! | Nexus", color=new_role.colour)
                    await message.author.send(embed=embed)
            else:
                await message.author.send(
                    ":x: | You entered an invalid color.\n"
                    "Please note that the colors are case sensitive, so spell them as you see them.\n"
                    "```\n"
                    "```")
                await message.delete()
            if message.content == "none":
                toremove = []
                for role in message.author.roles:
                    print("a")
                    if role.name in self.role_names:
                        print("b")
                        toremove.append(role)
                for role in toremove:
                    print("removing " + role.name)
                    await message.author.remove_roles(role)


async def ping(message: Message):
    #print("Testing ping!")
    delta = datetime.datetime.now() - message.created_at
    delta_ping = round(delta.microseconds / 1000)
    if delta_ping < 100:
        embed = discord.Embed(title=f"Ping: {delta_ping}ms.",
                              color=0x00ff00)
        await message.channel.send(embed=embed)
        return
    elif delta_ping < 200:
        embed = discord.Embed(title=f"Ping: {delta_ping}ms.",
                              color=0xfe9a2e)
        await message.channel.send(embed=embed)
        return
    else:
        embed = discord.Embed(title=f"Ping: {delta_ping}ms.",
                              color=0xff0000)
        await message.channel.send(embed=embed)


async def servericon(message: Message):
    await message.channel.send(f"{message.author.guild.icon_url}")


client = MyClient()
client.run(os.environ.get("token"))
