import os
import random
import urllib
import asyncio
import time
import sys

import discord

from discord.ext import commands, tasks
from discord.utils import get


if __name__ == '__main__':
    token = os.environ.get('BOT_TOKEN')

    if not token:
        print('Token required')
        sys.exit(0)

    pfx = '~'

    bot = commands.Bot(command_prefix=pfx)
    bot.load_extension("cogs.Ranks")
    bot.load_extension("cogs.Misc_Commands")
    bot.run(token)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        if not "```" in message.content and (message.content.count("|") >= 20 or "||‍" in message.content):
            await message.delete()
            await message.channel.send("lmao u tryin to troll or smth mate smh")

        poss = [722260161456111657, 560245352129888257, 574072152760778753, 520454991618506772,
                743291316720500836, 589171911305461965, 589171618534653955]
        if "pysh" in message.content.lower() or "push" in message.content.lower():
            if random.random() < 0.5:
                emoji = bot.get_emoji(random.choice(poss))
                await message.add_reaction(emoji)
        await bot.process_commands(message)

# @bot.command(name='ready')
# async def startStack(ctx):
#     if ctx.author in cur_players:
#         await ctx.send(f'You are already ready! Use {pfx}unready to leave.')
#         return
#     if len(cur_players) == 0:
#         await ctx.send(f'<@&{stacker_roleid}>, creating new game! Join using {pfx}ready.')
#     else:
#         await ctx.send(f'Added {ctx.author} to the stack.')
#         if len(cur_players) == 5:
#             await ctx.send(f'<@&{stacker_roleid}>, there are enough players for a 5 stack! Game time?')

#     cur_players.append(ctx.author)


# @bot.command(name='unready')
# async def leaveStack(ctx):
#     if ctx.author in cur_players:
#         cur_players.remove(ctx.author)
#         await ctx.send(f'Removed {ctx.author} from the stack.')
#     else:
#         await ctx.send(f"You aren't in the stack. Use {prefix}ready to join.")

# @bot.command(name='players')
# async def inStack(ctx):
#     msg = "Players curently ready: \n"
#     for player in cur_players:
#         msg += f'{player}\n'
#     await ctx.send(msg)

# @bot.command(name='clear')
# async def clearStack(ctx):
#     cur_players.clear()
#     await ctx.send("cleared the player stack.")
