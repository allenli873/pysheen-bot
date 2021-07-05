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
                cell = sheet.find(name)
            except gspread.exceptions.CellNotFound:
                await ctx.message.channel.send("Could not find player {}".format(name))
                return
            vals.append((name, int(sheet.cell(cell.row, cell.col + 1).value)))

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

        await ctx.message.channel.send("Best Teams:\n{}\n{}\nDifferential: {}".format(
            best_arr[:mid],
            best_arr[mid:],
            best_dif
        ))


def setup(bot):
    bot.add_cog(Balance(bot))
