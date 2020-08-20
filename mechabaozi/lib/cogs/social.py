import discord

from discord.ext import commands

from lib.base_cog import BaseCog

def setup(bot):
    bot.add_cog(SocialCog(bot))


class SocialCog(BaseCog, name="Social"):

    @commands.command(name='hi', aliases=['yo', 'hey', 'oy'])
    async def hi(self, ctx):
        """
        🏓 Ping pong 🏓
        """
        await ctx.send('hey')
