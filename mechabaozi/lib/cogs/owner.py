import discord
import importlib
import inspect

from discord.ext import commands

import lib.globals as config


def setup(bot):
    bot.add_cog(OwnerCog(bot))


class OwnerCog(commands.Cog, name="Owner"):
    """
    OwnerCog

    Cog defining owner-only functionality:
        - Loading/unloading cogs
        - Manipulating git repository state
        - Executing arbitrary code

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eval', aliases=['debug'])
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """
        Evaluates input code and outputs the result.
        """
        code = code.strip('` ')
        env = {
            'bot':      self.bot,
            'ctx':      ctx,
            'message':  ctx.message,
            'server':   ctx.guild,
            'channel':  ctx.message.channel,
            'author':   ctx.message.author,
        }.update(globals())

        result = None
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as err:
            await ctx.send(f'```py\n{type(err).__name__}:{str(err)}```')
            return
        await ctx.send(f'```py\n{result}```')

    @commands.command(name='reload_config', aliases=['flush', 'flush_config'], hidden=True)
    @commands.is_owner()
    async def reload_config(self, ctx):
        """ Reloads the global config module """
        importlib.reload(config)
        await ctx.send('```Successfully reloaded config.```')

    @commands.command(name='quit', aliases=['exit', 'die', 'logout', 'stop'], hidden=True)
    @commands.is_owner()
    async def quit(self, ctx):
        """ Stops the bot """
        msg = await ctx.send('*Goodbye.*')
        await msg.add_reaction('👋')
        await self.bot.logout()
