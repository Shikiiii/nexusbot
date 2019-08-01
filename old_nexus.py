import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord import Forbidden
from discord import HTTPException
from itertools import cycle
import aiohttp
import random
import os
import json
import time
import datetime

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

server = 0

role_names = set()


@bot.event
async def on_ready():
    global server
    server = bot.get_server("599611697464082434")

    global role_names
    role_names = {"red", "yellow", "black", "maroon", "darkred", "brown", "firebrick", "crimson", "tomato", "coral",
                  "indianred", "lightcoral", "darksalmon", "salmon", "lightsalmon", "orangered", "darkorange", "orange",
                  "gold", "darkgoldenrod", "goldenrod", "palegoldenrod", "pink", "lightpink", "hotpink", "deeppink",
                  "darkkhaki", "palevioletred", "khaki", "mediumvioletred", "orchid", "olive", "magenta", "violet",
                  "plum", "thistle", "yellow", "purple", "yellowgreen", "darkolivegreen", "olivedrab", "mediumorchid",
                  "lawngreen", "darkorchid", "darkviolet", "darkmagenta", "mediumpurple", "mediumslateblue",
                  "greenyellow", "slateblue"}

    await bot.change_presence(game=discord.Game(name='with your feelings.'))
    print('Ready!')


# await run_tests()

@bot.event
async def on_message(message):
    print("Got a message!")
    if (message.channel.id == "599640898233565198"):
        print("Message is in the right channel!")
        print("Trying to matching message to a role... Message:" + message.content)
        if message.content in role_names:
            new_role = discord.utils.get(server.roles, name=message.content)
            if hasattr(new_role, "id"):
                await bot.delete_message(message)
                print("We have a match! Role:" + new_role.name)
                print("Checking colored roles to remove...")
                toremove = []
                for role in message.author.roles:
                    print("a")
                    if role.name in role_names:
                        print("b")
                        toremove.append(role)
                print("Removing colored roles...")
                for role in toremove:
                    print("removing" + role.name)
                    await bot.remove_roles(message.author, role)
                print("Adding " + new_role.name + " role...")
                await bot.add_roles(message.author, new_role)
                print("Great success!")
                embed = discord.Embed(title="You successfully changed your color to **{}**.".format(str(new_role)),
                                      description="Enjoy your new color! | Nexus", color=new_role.colour)
                await bot.send_message(message.author, embed=embed)
        else:
            await bot.send_message(message.author,
                                   ":x: | You entered an invalid color. Please note that the colors are case sensitive, so spell them as you see them.")
            await bot.delete_message(message)
        if (message.content == "none"):
            toremove = []
            for role in message.author.roles:
                print("a")
                if role.name in role_names:
                    print("b")
                    toremove.append(role)
            for role in toremove:
                print("removing " + role.name)
                await bot.remove_roles(message.author, role)


async def run_tests():
    print("Running tests!")
    cant = discord.utils.get(server.members, id="393839495859929089")
    print(cant)

    test_role = discord.utils.get(server.roles, name="pink")
    print("Removing " + str(test_role) + " role...")
    await bot.remove_roles(cant, test_role)

    test_role = discord.utils.get(server.roles, name="red")
    print("Adding " + str(test_role) + " role...")
    await bot.add_roles(cant, test_role)

    print("Tests done! Logging out...")
    await bot.logout()
    print("Logged out, see you later! ^^")


bot.run(os.environ.get("token"))
