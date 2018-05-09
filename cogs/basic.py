import discord
from discord.ext import commands

class Basic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def help(self):
        await self.bot.say('hey')
