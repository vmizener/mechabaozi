import discord
import git
import importlib
import inspect
import pprint
import traceback

from discord.ext import commands

import lib.globals as CONFIG
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

    @commands.command(name='quit', aliases=['exit'])
    @commands.is_owner()
    async def quit(self, ctx):
        """ Stops the bot """
        self.logger.info('Disconnecting')
        msg = await ctx.send('*Goodbye.*')
        await msg.add_reaction('👋')
        await self.bot.logout()
        self.logger.info('Successfully disconnected')

    @commands.command(name='update', aliases=['up'])
    @commands.is_owner()
    async def update(self, ctx):
        """ Updates the bot environment and reloads it """
        g = git.Git('.')
        if len(out := g.status('--porcelain')) > 0:
            msg = f'Bot environment is not in a clean state!  Cannot automatically update!\n```{out}```'
            self.logger.error(msg)
            await ctx.send(msg)
            await ctx.message.add_reaction('👎')
            return
        else:
            g.pull()
            self.logger.info('Updated local repository')
            await self.reload_extensions(ctx)

    # ---------------
    # Hidden commands
    # ---------------

    @commands.command(name='eval', aliases=['debug'], hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """
        Evaluates input code and outputs the result.
        """
        code = code.strip('` ')
        channel = ctx.message.channel
        author = ctx.message.author
        self.logger.info(f'Parsed debug request from "{author}" @ "{channel}":\n"""{code}"""')
        env = {
            'bot':      self.bot,
            'ctx':      ctx,
            'channel':  channel,
            'author':   author,
        }
        env.update(globals())

        result = None
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as exception:
            msg = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        else:
            msg = f'{pprint.pformat(result)}'
        self.logger.info(msg)
        if len(msg) >= CONFIG.MAX_MESSAGE_LENGTH:
            msg = f'```py\n{msg[:CONFIG.MAX_MESSAGE_LENGTH]}\n...```\nMESSAGE TRUNCATED; SEE LOG FOR FULL RESPONSE'
        else:
            msg = f'```py\n{msg}```'
        await ctx.send(msg)

    @commands.command(name='load_extension', aliases=['load'], hidden=True)
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
            msg = f'Failed to load {extension}: {type(error).__name__} - {err}'
            self.logger.error(msg)
            await ctx.send(f'```py\n{msg}\n```')
        else:
            self.logger.info(f'Loaded extension "{extension}"')
            await ctx.message.add_reaction('👌')

    @commands.command(name='unload_extension', aliases=['unload'], hidden=True)
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
            msg = f'Failed to unload {extension}: {type(error).__name__} - {err}'
            self.logger.error(msg)
            await ctx.send(f'```py\n{msg}\n```')
        else:
            self.logger.info(f'Unloaded extension "{extension}"')
            await ctx.message.add_reaction('👌')

    @commands.command(name='reload_extensions', aliases=['r', 'rl', 'reload'], hidden=True)
    @commands.is_owner()
    async def reload_extensions(self, ctx, *, extensions: str=None):
        """
        Unload, then reload the specified bot extensions, delmited by comma.

        Extension uses import path syntax (e.g. "lib.cogs.owner").
        """
        if extensions is None:
            self.logger.info('Reloading all extensions')
            extensions = CONFIG.STARTUP_EXTENSIONS
        else:
            extensions = [extension.strip(' ') for extension in extensions.split(',')]
        fail = False
        for extension in CONFIG.STARTUP_EXTENSIONS:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except (AttributeError, ImportError) as err:
                fail = True
                msg = f'Failed to reload {extension}: {type(error).__name__} - {err}'
                self.logger.error(msg)
                await ctx.send(f'```py\n{msg}\n```')
            else:
                self.logger.info(f'Reloaded extension "{extension}"')
        if fail:
           await ctx.message.add_reaction('👎')
        else:
           await ctx.message.add_reaction('👌')

    @commands.command(name='flush_config', aliases=['flush'], hidden=True)
    @commands.is_owner()
    async def flush_config(self, ctx):
        """ Reloads the global config module """
        importlib.reload(CONFIG)
        await ctx.message.add_reaction('👌')

