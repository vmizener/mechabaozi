import discord
import git
import importlib
import inspect
import traceback

from discord.ext import commands

import lib.globals as config
from lib.base_cog import BaseCog


def setup(bot):
    bot.add_cog(OwnerCog(bot))


class OwnerCog(BaseCog, name="Owner"):
    """
    OwnerCog

    Cog defining owner-only functionality:
        - Loading/unloading cogs
        - Manipulating git repository state
        - Executing arbitrary code

    """

    @commands.command(name='eval', aliases=['debug'])
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """
        Evaluates input code and outputs the result.
        """
        code = code.strip('` ')
        channel = ctx.message.channel
        author = ctx.message.author
        self.logger.info(f'Parsed debug request from {author}@{channel}:\n"""{code}"""')
        env = {
            'bot':      self.bot,
            'ctx':      ctx,
            'message':  ctx.message,
            'server':   ctx.guild,
            'channel':  channel,
            'author':   author,
        }.update(globals())

        result = None
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as err:
            fmt_tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            err_msg = f'{type(err).__name__}: {str(err)}\n{fmt_tb}'
            await ctx.send(f'```py\n{err_msg}```')
            self.logger.info(err_msg)
        else:
            await ctx.send(f'```py\n{result}```')
            self.logger.info(f'Result:\n"""{result}"""')

    @commands.command(name='quit', aliases=['exit'])
    @commands.is_owner()
    async def quit(self, ctx):
        """ Stops the bot """
        self.logger.info('Disconnecting')
        msg = await ctx.send('*Goodbye.*')
        await msg.add_reaction('👋')
        await self.bot.logout()
        self.logger.info('Successfully disconnected')

    @commands.command(name='update')
    @commands.is_owner()
    async def update(self, ctx):
        """ Updates the bot, then restarts it """
        pass

    # ---------------
    # Hidden commands
    # ---------------

    @commands.command(name='load_extension', aliases=['l', 'lo', 'load'], hidden=True)
    @commands.is_owner()
    async def load_extension(self, ctx, *, extension: str):
        """
        Load the specified bot extension.

        Extension uses import path syntax (e.g. "lib.cogs.owner").
        """
        try:
            self.bot.load_extension(extension)
        except (AttributeError, ImportError) as err:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nFailed to load {extension}: {type(error).__name__} - {err}\n```')
        else:
            await ctx.message.add_reaction('👌')

    @commands.command(name='unload_extension', aliases=['ul', 'unl', 'unload'], hidden=True)
    @commands.is_owner()
    async def unload_extension(self, ctx, *, extension: str):
        """
        Unload the specified bot extension.

        Extension uses import path syntax (e.g. "lib.cogs.owner").
        """
        try:
            self.bot.unload_extension(extension)
        except (AttributeError, ImportError) as err:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nFailed to unload {extension}: {type(error).__name__} - {err}\n```')
        else:
            await ctx.message.add_reaction('👌')

    @commands.command(name='reload_extension', aliases=['r', 'rl', 'reload'], hidden=True)
    @commands.is_owner()
    async def reload_extension(self, ctx, *, extension: str):
        """
        Unload, then reload the specified bot extension.

        Extension uses import path syntax (e.g. "lib.cogs.owner").
        """
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        except (AttributeError, ImportError) as err:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nFailed to reload {extension}: {type(error).__name__} - {err}\n```')
        else:
            await ctx.message.add_reaction('👌')

    @commands.command(name='flush_config', aliases=['flush'], hidden=True)
    @commands.is_owner()
    async def flush_config(self, ctx):
        """ Reloads the global config module """
        importlib.reload(config)
        await ctx.message.add_reaction('👌')

