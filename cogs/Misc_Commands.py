import os
import random
import urllib
import asyncio
import time
import discord

from discord.ext import commands, tasks

class Misc_Commands(commands.Cog):
    def __init(self, bot):
        self.bot = bot
        self.stacker_roleid = 736769041640849450
        self.camelwatchers_roleid = 781636133762629632

    @commands.command(name='stalk')
    async def stalk(self, ctx):
        # http://usaco.org/current/data/feb20_platinum_results.html
        # !stalk Siyong Huang
        divs = ['plat', 'gold', 'silver', 'bronze']

        namearr = ctx.message.content.split()

        if len(namearr) != 3:
            await ctx.send("ur bad")
            return

        name = f'{namearr[1]} {namearr[2]}'

        found = False

        for i, div in enumerate(divs):
            if div == 'plat':
                continue
            with open(f"{div}.txt", "r") as f:
                for line in f.readlines():
                    if name.lower() in line.lower():
                        await ctx.send(f'{divs[i - 1]}')
                        found = True
                        break
                else:
                    continue
                break

        if not found:
            await ctx.send('bronze')

        
    @commands.command(name='tmw')
    async def tmw(self, ctx):
        await ctx.send("tmw orz")

    @commands.command(name='amongus')
    async def among_us(self, ctx):
        if ctx.author.voice == None:
            await ctx.send("Error: please connect to a VC channel")
            return
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='umvc')
    async def discussion(self, ctx):
        pysheen_disciple = ctx.guild.get_role(756009671478739015)

        if pysheen_disciple not in ctx.author.roles:
            await ctx.send("no.")
            return

        voiceChannel = ctx.author.voice.channel
        for member in voiceChannel.members:
            await member.edit(mute=False)

    @commands.command(name='mvc')
    async def undisc(self, ctx):
        pysheen_disciple = ctx.guild.get_role(756009671478739015)

        if pysheen_disciple not in ctx.author.roles:
            await ctx.send("no.")
            return
        
        voiceChannel = ctx.author.voice.channel
        for member in voiceChannel.members:
            await member.edit(mute=True)


    @commands.command(name='end')
    async def end_game(self, ctx):
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(Misc_Commands(bot))
