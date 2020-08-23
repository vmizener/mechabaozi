import datetime
import discord
import git
import importlib
import inspect
import os
import pprint
import sys
import time
import traceback

from discord.ext import commands

from lib.base_cog import BaseCog
from lib.globals import CLIENT_LAUNCHER_PATH, STARTUP_EXTENSIONS
from lib.globals import COMMAND_REACTION_SUCCESS


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
    def __init__(self, bot):
        super().__init__(bot)
        self.git = git.Git('.')

    @commands.command(name='quit', aliases=['exit'])
    @commands.is_owner()
    async def quit(self, ctx):
        """ Stops the bot """
        self.log.info('Disconnecting')
        msg = await ctx.send('*Goodbye.*')
        await msg.add_reaction('👋')
        await self.bot.logout()
        self.log.info('Successfully disconnected')

    @commands.command(name='restart')
    @commands.is_owner()
    async def restart(self, ctx):
        """ Restarts the bot """
        # TODO: clean this up, make safer
        self.log.info('Restarting')
        msg = await ctx.send('*Restarting*')
        await self.bot.logout()
        time.sleep(5)
        #os.fsync()
        os.execv(CLIENT_LAUNCHER_PATH, sys.argv)

    @commands.command(name='update', aliases=['up'])
    @commands.is_owner()
    async def update(self, ctx):
        """ Updates the bot environment and reloads it """
        if len(out := self.git.status('--porcelain')) > 0:
            await self.report_error(
                ctx, 
                title='Bad Environment State', 
                message=f'Bot environment is not in a clean state!  Cannot automatically update!\n```{out}```',
            )
            return
        response = self.git.pull()
        self.log.info(response)
        await ctx.send(f'```{response}```')
        if 'Already' in response:
            await ctx.message.add_reaction('👌')
        else:
            await self.reload_extensions(ctx)

    @commands.command(name='eval', aliases=['debug'], hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """
        Evaluates input code and outputs the result.
        """
        code = code.strip('` ')
        channel = ctx.message.channel
        author = ctx.message.author
        self.log.info(f'Parsed debug request from "{author}" @ "{channel}":\n"""{code}"""')
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
        self.log.info(msg)
        p = commands.Paginator(prefix='```py')
        for line in msg.split('\n'):
            p.add_line(line)
        for page in p.pages:
            await ctx.send(page)

    # ---------------
    # Git commands
    # ---------------

    @commands.group(name='git', hidden=True)
    @commands.is_owner()
    async def git(self, ctx):
        """ Invokes git in the bot's local repository """
        if ctx.invoked_subcommand is None:
            #await ctx.invoke(self.bot.get_command('git status'))
            await ctx.invoke(self.bot.get_command('help'), keyword='git')

    @git.group(name='status')
    @commands.is_owner()
    async def status(self, ctx):
        """ Displays the bot's local repository status """
        out = self.git.status()
        self.log.info(out)
        await ctx.send(f'```{out}```')

    # ---------------
    # Cog state commands
    # ---------------

    @commands.command(name='load_extension', aliases=['l', 'load'], hidden=True)
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
            self.log.error(msg)
            await ctx.send(f'```py\n{msg}\n```')
        else:
            self.log.info(f'Loaded extension "{extension}"')
            await ctx.message.add_reaction('👌')

    @commands.command(name='unload_extension', aliases=['ul', 'unload'], hidden=True)
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
            self.log.error(msg)
            await ctx.send(f'```py\n{msg}\n```')
        else:
            self.log.info(f'Unloaded extension "{extension}"')
            await ctx.message.add_reaction('👌')

    @commands.command(name='reload_extensions', aliases=['r', 'rl', 'reload'], hidden=True)
    @commands.is_owner()
    async def reload_extensions(self, ctx, *extensions):
        """
        Unload, then reload the specified bot extensions, delmited by comma.

        Extension uses import path syntax (e.g. "lib.cogs.owner").
        """
        if len(extensions) == 0:
            self.log.info('Reloading all extensions')
            extensions = STARTUP_EXTENSIONS
        fail = False
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
            except (AttributeError, ImportError) as err:
                fail = True
                msg = f'Failed to reload {extension}: {type(error).__name__} - {err}'
                self.log.error(msg)
                await ctx.send(f'```py\n{msg}\n```')
            else:
                self.log.info(f'Reloaded extension "{extension}"')
        if fail:
           await ctx.message.add_reaction('👎')
        else:
           await ctx.message.add_reaction('👌')

    @commands.command(name='flush_config', aliases=['flush'], hidden=True)
    @commands.is_owner()
    async def flush_config(self, ctx):
        """ Reloads the global config module """
        config_module = importlib.import_module('lib.globals')
        importlib.reload(config_module)
        await ctx.message.add_reaction(COMMAND_REACTION_SUCCESS)

