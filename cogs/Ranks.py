import requests
import bs4
import urllib
import discord
from bs4 import BeautifulSoup

from discord.ext import commands, tasks

CAMEL_RANK_CACHE = get_rank('camellCase#NA1')

def get_rank(name):
    url = "https://tracker.gg/valorant/profile/riot/" + urllib.parse.quote(name) + "/overview?playlist=competitive"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    try:
        return soup.find_all("span", class_="valorant-highlighted-stat__value")[0].text
    except:
        return None

class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.print_camel_rank.start()

    def cog_unload(self):
        self.print_camel_rank.cancel()

    @tasks.loop(minutes=5)
    async def print_camel_rank(self):
        channel = self.bot.get_channel(781629627730231328)
        rank: str = get_rank("camellCase#NA1")
        if rank:
            await channel.send(rank)
            if CAMEL_RANK_CACHE != rank:
                CAMEL_RANK_CACHE = rank
                await channel.send(f'<@&781636133762629632>, camel rank has changed to {rank} !')
        else:
            await channel.send('bad')

    @commands.command(name='rank')
    async def rank_of(self, ctx, *args):
        for id in args:
            rank: str = get_rank(id)
            if rank:
                await ctx.message.channel.send(rank)
            else:
                await ctx.message.channel.send('bad')

def setup(bot):
    bot.add_cog(Ranks(bot))