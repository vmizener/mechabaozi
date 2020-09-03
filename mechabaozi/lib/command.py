import functools
import inspect
import logging

from discord.ext import commands

from lib.globals import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


def command(*args, **kwargs):
    def wrapper(method):
        if inspect.isfunction(method):
            method_name = method.__qualname__
        else:
            # TODO: handle non-functions? (methods?)
            method_name = '<Unknown Method>'

        @commands.command(*args, **kwargs)
        @functools.wraps(method)
        async def cmd_wrapper(self, ctx, *cmd_args, **cmd_kwargs):
            logger.info(f'User "{ctx.message.author.name}" invoked {method_name}')
            result = await method(self, ctx, *cmd_args, **cmd_kwargs)
            logger.info(f'{method_name} returned successfully')
            return result
        return cmd_wrapper

    return wrapper
