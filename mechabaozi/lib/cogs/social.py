import discord

from lib.base_cog import BaseCog
from lib.command import command


def setup(bot):
    bot.add_cog(SocialCog(bot))


class SocialCog(BaseCog, name="Social"):

    @command(name='hi', aliases=['yo', 'hey', 'oy'])
    async def hi(self, ctx):
        """
        🏓 Ping pong 🏓
        """
        await ctx.send('hey')
