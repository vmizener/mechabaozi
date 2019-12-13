import discord

from discord.ext import commands


def setup(bot):
    bot.add_cog(SocialCog(bot))


class SocialCog(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hi', aliases=['yo', 'hey', 'oy'])
    async def hi(self, ctx):
        """
        🏓 Ping pong 🏓
        """
        await ctx.send('hey')
