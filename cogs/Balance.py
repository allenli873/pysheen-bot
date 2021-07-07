import discord
import gspread
import os
import json
import random
from oauth2client.service_account import ServiceAccountCredentials

from discord.ext import commands, tasks

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.teams = []

    @commands.command(name='balance')
    async def balance(self, ctx, *args):
        google_secret = json.loads(os.environ.get('GOOGLE_CLIENT_SECRETS'))
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(google_secret, scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        sheet = client.open("Cow Server CSGO ELO").sheet1

        vals = []
        # Extract and print all of the values
        for name in args:
            try:
                cell = sheet.find(name.lower())
            except gspread.exceptions.CellNotFound:
                await ctx.message.channel.send("Could not find player {}".format(name))
                return
            vals.append((name, float(sheet.cell(cell.row, cell.col + 1).value)))

        mid = len(args) // 2
        best_abs_dif = 1000000
        best_dif = 0
        best_arr = vals

        for _ in range(2000):
            random.shuffle(vals)
            t1, t2 = sum(n for _, n in vals[:mid]), sum(n for _, n in vals[mid:])
            if abs(t1 - t2) < best_abs_dif:
                best_abs_dif = abs(t1 - t2)
                best_dif = t1 - t2
                best_arr = vals.copy()

        self.teams = best_arr

        await ctx.message.channel.send("Best Teams:\n{}\n{}\nDifferential: {}".format(
            best_arr[:mid],
            best_arr[mid:],
            best_dif
        ))

    @commands.command(name='updatelo')
    async def updatelo(self, ctx, *args):
        if len(args) != 1:
            await ctx.message.channel.send("Not enough arguments")
            return

        try:
            winning_team = int(args[0])
        except ValueError:
            await ctx.message.channel.send("Enter a number (1 or 2) indicating the winning team")
            return

        if winning_team < 1 or winning_team > 2:
            await ctx.message.channel.send("Enter a number (1 or 2) indicating the winning team")
            return

        if len(self.teams) == 0:
            await ctx.message.channel.send("No game to update elo for")
            return

        mid = len(self.teams) // 2
        winners = [name.lower() for name, _ in self.teams[:mid]]
        losers = [name.lower() for name, _ in self.teams[mid:]]

        if winning_team == 2:
            winners, losers = losers, winners

        google_secret = json.loads(os.environ.get('GOOGLE_CLIENT_SECRETS'))
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(google_secret, scope)
        client = gspread.authorize(creds)

        sheet = client.open("Cow Server CSGO ELO").worksheet("Logger")

        sheet_content = sheet.get_all_values()

        # new row we're updating
        res = []
        for name in sheet_content[0]:
            if name in winners:
                res.append(4)
            elif name in losers:
                res.append(-4)
            else:
                res.append(0)

        res = [res]

        sheet.update('A{}:{}{}'.format(len(sheet_content) + 1, chr(ord('A') + len(sheet_content[0]) - 1), len(sheet_content) +  1), res)

        self.teams = []

        await ctx.message.channel.send("Good job team {}, tell your opponents they gotta get good, especially {}".format(winning_team, random.choice(losers)))

def setup(bot):
    bot.add_cog(Balance(bot))
