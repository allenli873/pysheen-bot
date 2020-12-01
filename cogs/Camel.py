import os
import random
import urllib
import asyncio
import time
import discord
import random

from discord.ext import commands, tasks

class Camel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.camel.start()

    def cog_unload(self):
        self.camel.cancel()

    @tasks.loop(minutes=5)
    async def camel(self):
        channel = self.bot.get_channel(781629627730231328)
        if channel:
            await channel.send("$camel")

def setup(bot):
    bot.add_cog(Camel(bot))
