import discord
from discord.ext import commands

class Interactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self):
        await self.bot.say('hey')
