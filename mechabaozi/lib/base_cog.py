import datetime
import discord
import logging

from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger(f"mechabaozi.{self.qualified_name}")

    @staticmethod
    async def report_error(ctx, *, title='', message='', footer=None):
        error_embed = discord.Embed(
            title=title,
            timestamp=datetime.datetime.utcnow(),
            description=message,
            color=discord.Color.dark_red(),
        )
        # error_embed.set_author(
        #     name=str(ctx.message.author),
        #     icon_url=str(ctx.message.author.avatar_url),
        # )
        if footer:
            error_embed.set_footer(text=footer)
        await ctx.message.add_reaction('👎')
        return await ctx.send(embed=error_embed)
