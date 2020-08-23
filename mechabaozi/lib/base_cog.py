import datetime
import discord
import logging

from discord.ext import commands

from lib.globals import COMMAND_REACTION_APPROVE, COMMAND_REACTION_DENY, COMMAND_REACTION_FAIL


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger(f"mechabaozi.{self.qualified_name}")

    @staticmethod
    async def report_error(ctx, *, title='Error', message='Encountered error', footer=None):
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
        await ctx.message.add_reaction(COMMAND_REACTION_FAIL)
        return await ctx.send(embed=error_embed)

    @staticmethod
    async def request_confirmation(ctx, *, title='Confirm request', message='You must confirm this action', footer=None, timeout=15.0):
        embed = discord.Embed(
            title=title,
            timestamp=datetime.datetime.utcnow(),
            description=message,
            color=discord.Color.dark_gray(),
        )
        embed.set_author(
            name=str(ctx.message.author),
            icon_url=str(ctx.message.author.avatar_url),
        )
        if footer:
            embed.set_footer(text=footer)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(COMMAND_REACTION_APPROVE)
        await msg.add_reaction(COMMAND_REACTION_DENY)
        ret = True
        try:
            reaction, user = await ctx.bot.wait_for(
                'reaction_add',
                timeout=timeout,
                check=lambda reaction, usr: usr == ctx.message.author and str(reaction.emoji) in [COMMAND_REACTION_APPROVE, COMMAND_REACTION_DENY],
            )
        except asyncio.TimeoutError:
            await ctx.message.add_reaction(COMMAND_REACTION_DENY)
            ret = False
        else:
            if str(reaction.emoji) == COMMAND_REACTION_APPROVE:
                await ctx.message.add_reaction(COMMAND_REACTION_APPROVE)
            else:
                await ctx.message.add_reaction(COMMAND_REACTION_DENY)
                ret = False
        await msg.delete()
        return ret
