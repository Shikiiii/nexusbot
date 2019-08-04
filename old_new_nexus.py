# Trying to make the "ping" command work, just temporary:
import datetime
import os
from typing import Optional, Set

import discord
from discord import Message, Guild
from discord.ext.commands import Bot

bot = Bot(command_prefix='!')
bot.remove_command('help')

server: Optional[Guild] = None

role_names: Set[str] = set()


@bot.event
async def on_ready():
    global server
    server = bot.get_guild(599611697464082434)

    global role_names
    role_names = {"red", "yellow", "black", "maroon", "darkred", "brown", "firebrick", "crimson", "tomato", "coral",
                  "indianred", "lightcoral", "darksalmon", "salmon", "lightsalmon", "orangered", "darkorange", "orange",
                  "gold", "darkgoldenrod", "goldenrod", "palegoldenrod", "pink", "lightpink", "hotpink", "deeppink",
                  "darkkhaki", "palevioletred", "khaki", "mediumvioletred", "orchid", "olive", "magenta", "violet",
                  "plum", "thistle", "purple", "yellowgreen", "darkolivegreen", "olivedrab", "mediumorchid",
                  "lawngreen", "darkorchid", "darkviolet", "darkmagenta", "mediumpurple", "mediumslateblue",
                  "greenyellow", "slateblue"}

    await bot.change_presence(activity=discord.Game(name='with your feelings.'))
    print('Ready!')


# await run_tests()

@bot.event
async def on_message(message: Message):
    print("Received message from channel " + str(message.channel))
    if message.content == "!ping":
        await ping(message)
    elif message.content == "!servericon":
        await servericon(message)
    elif "<@393839495859929089>" in message.content:
        await message.delete()
        await message.channel.send("{}, that's not cool, you know. If you just pinged her for **literally nothing**, you'll beg for forgiveness.".format(message.author))
    elif message.channel.id == 599640898233565198:
        print("Message is in the right channel!")
        print("Trying to matching message to a role... Message:" + message.content)
        if message.content in role_names:
            new_role = discord.utils.get(server.roles, name=message.content)
            if hasattr(new_role, "id"):
                await message.delete()
                print("We have a match! Role:" + new_role.name)
                print("Checking colored roles to remove...")
                toremove = []
                for role in message.author.roles:
                    if role.name in role_names:
                        toremove.append(role)
                print("Removing colored roles...")
                for role in toremove:
                    print("removing" + role.name)
                    await message.author.remove_roles(role)
                print("Adding " + new_role.name + " role...")
                await message.author.add_roles(new_role)
                print("Great success!")
                embed = discord.Embed(title="You successfully changed your color to **{}**.".format(str(new_role)),
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
                if role.name in role_names:
                    print("b")
                    toremove.append(role)
            for role in toremove:
                print("removing " + role.name)
                await message.author.remove_roles(role)


async def ping(message: Message):
    print("Testing ping!")
    delta = datetime.datetime.now() - message.created_at
    delta_ping = round(delta.microseconds / 1000)
    if delta_ping < 100:
        embed = discord.Embed(title="Ping: {}ms.".format(delta_ping),
                              description=":green_book: Ping is normal! There's no need to inform bot support.",
                              color=0x00ff00)
        await message.channel.send(embed=embed)
        return
    elif delta_ping < 200:
        embed = discord.Embed(title="Ping: {}ms.".format(delta_ping),
                              description=":orange_book: Ping is abnormal! There's no need to inform bot support, "
                                          "but try using !ping again after 5 minutes and check the ping again, "
                                          "just in case.",
                              color=0xfe9a2e)
        await message.channel.send(embed=embed)
        return
    else:
        embed = discord.Embed(title="Ping: {}ms.".format(delta_ping),
                              description=":closed_book: Ping is high! Please, type ``inform`` to inform bot support.",
                              color=0xff0000)
        await message.channel.send(embed=embed)

        async def check(checked_message):
            return checked_message.content == 'inform' and checked_message.channel == message.channel

        msg = await bot.wait_for('message', check=check)

        if msg is None:
            await message.channel.send(
                "Alright, {}. The bot support wasn't informed because you didn't typed ``inform``.".format(
                    message.author.name))
        else:
            informed = discord.Embed(title="Thank you! The bot support has been informed.", description="owo",
                                     color=0x3adf00)
            botsupportchannel = discord.utils.get(message.server.channels, name="logs")
            await botsupportchannel.send("{} reported a high ping! {}ms.".format(message.author, delta_ping))
            await botsupportchannel.send("", embed=informed)

async def servericon(message: Message):
    await message.channel.send("{}".format(message.author.guild.icon_url))

async def run_tests():
    print("Running tests!")
    cant = discord.utils.get(server.members, id="393839495859929089")
    print(cant)

    test_role = discord.utils.get(server.roles, name="pink")
    print("Removing " + str(test_role) + " role...")
    await cant.remove_roles(test_role)

    test_role = discord.utils.get(server.roles, name="red")
    print("Adding " + str(test_role) + " role...")
    await cant.add_roles(test_role)

    print("Tests done! Logging out...")
    await bot.logout()
    print("Logged out, see you later! ^^")


bot.run(os.environ.get("token"))
