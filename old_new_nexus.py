import discord
from discord.ext.commands import Bot
import os

bot = Bot(command_prefix='!')
bot.remove_command('help')

server = None

role_names = set()


@bot.event
async def on_ready():
    global server
    server = bot.get_guild("599611697464082434")

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
async def on_message(message):
    print("Got a message!")
    if message.channel.id == "599640898233565198":
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
                    print("a")
                    if role.name in role_names:
                        print("b")
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
                await message.author.send_message(embed=embed)
        else:
            await message.author.send_message(
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
