import os
import random
import urllib
import asyncio
import time
import discord

from discord.ext import commands, tasks

class Camel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.camel.start()
        self.sampai.start()

    def cog_unload(self):
        self.camel.cancel()
        self.sampai.cancel()


    @tasks.loop(minutes=5)
    async def camel(self):
        channel = self.bot.get_channel(781629627730231328)
        if channel:
            await channel.send("$camel")

    @tasks.loop(seconds=5)
    async def sampai(self):
        channel = self.bot.get_channel(783123388469084181)
        if channel:
            await channel.send("$userrank <@271689732386324482>")

def setup(bot):
    bot.add_cog(Camel(bot))
