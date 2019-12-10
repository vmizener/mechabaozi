import discord

from discord.ext import commands


class SocialInteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        """
        🏓 Ping pong 🏓
        """
        await ctx.send('hey')
