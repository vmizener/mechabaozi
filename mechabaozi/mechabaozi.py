#!/usr/bin/env python3

import asyncio
import datetime
import discord
import logging
import sys
import traceback
import yaml

from discord.ext import commands

from lib.base_cog import BaseCog
from lib.globals import \
    COMMAND_PREFIX, CLIENT_CONFIG_PATH, BOT_DESCRIPTION, DEFAULT_LOGGER, \
    LOGFORMAT, LOGPATH,  STARTUP_EXTENSIONS, \
    COMMAND_REACTION_DEBUG


class MechaBaozi:
    def __init__(self, *, client_config_path=CLIENT_CONFIG_PATH, log_level=logging.INFO):
        self.log = logging.getLogger(DEFAULT_LOGGER)
        self.log.info('Initializing.')

        log_path = LOGPATH
        log_formatter = logging.Formatter(LOGFORMAT)

        logfile_handler = logging.FileHandler(log_path)
        logfile_handler.setFormatter(log_formatter)
        self.log.addHandler(logfile_handler)

        logstrm_handler = logging.StreamHandler(sys.stdout)
        logstrm_handler.setFormatter(log_formatter)
        self.log.addHandler(logstrm_handler)

        self._log_level = None
        self.log_level = log_level
        self.log.info('Logging set up successfully')

        self.log.info(f'Reading client config @ {client_config_path}')
        try:
            with open(client_config_path, 'r') as file_handle:
                client_token = yaml.safe_load(file_handle)['client_token']
            self.log.info('Successfully parsed token')
        except:
            # TODO
            raise

        self.token = client_token
        self.log.debug(f'Token set: {self.token}.')

        bot = commands.Bot(
            description=BOT_DESCRIPTION,
            command_prefix=COMMAND_PREFIX,
            help_command=None,
        )
        self.bot = bot
        self.log.info('Bot spawned.')

        self.register_on_ready()
        self.register_on_command_error()

        self.log.info('Loading extensions:')
        for extension_import_path in STARTUP_EXTENSIONS:
            self.bot.load_extension(extension_import_path)
            self.log.info(f'- {extension_import_path}')

        self.log.info('Initialization complete')

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level):
        self._log_level = level
        self.log.setLevel(level)

    def run(self):
        self.log.info('Activating bot.')
        self.bot.run(self.token, bot=True, reconnect=True)

    def register_on_ready(self):
        async def on_ready():
            server_strings = '\n'.join([f'- {s.name}::{s.id}' for s in self.bot.guilds])
            self.log.info(f'Logged in as: {self.bot.user.name}#{self.bot.user.id}')
            self.log.info(f'Discord API v{discord.__version__}')
            self.log.info(f'Running on {len(self.bot.guilds)} servers:')
            for server in [f'{s.name}::{s.id}' for s in self.bot.guilds]:
                self.log.info(f'- {server}')
        self.bot.event(on_ready)
        self.log.info('Registered "on_ready" method.')

    def register_on_command_error(self):
        async def on_command_error(ctx, exception):
            fmt_tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.log.error(f"Encountered exception:\n\t{exception}\n{fmt_tb}")
            if isinstance(exception, commands.errors.MissingPermissions):
                await ctx.send(
                    f"```Oy, {ctx.message.author.name}, you don't have permissions for that.```"
                )
            elif isinstance(exception, commands.errors.CheckFailure):
                await ctx.send(
                    f"```Oy, {ctx.message.author.name}, you don't have the required roles for that.```"
                )
            elif isinstance(exception, TimeoutError):
                # TODO: indicate timeout?
                pass
            else:
                error_message = await BaseCog.report_error(
                    ctx,
                    title='',
                    message=f'```py\n{exception}```\nSee log for details.',
                    footer=str(type(exception).__name__),
                )
                # await error_message.add_reaction(COMMAND_DEBUG_REACTION)
                # try:
                #     reaction, user = await ctx.bot.wait_for(
                #         'reaction_add',
                #         timeout=15.0,
                #         check=lambda rct, usr: usr != ctx.bot.user and str(rct.emoji) == COMMAND_DEBUG_REACTION,
                #     )
                # except asyncio.TimeoutError:
                #     pass
                # else:
                #     error_embed.add_field(
                #         name='Details',
                #         value=f'{exception.__doc__}',
                #         inline=False,
                #     )
                #     error_embed.add_field(
                #         name='Cause',
                #         value=f'{exception.__cause__}',
                #         inline=False,
                #     )
                #     error_embed.add_field(
                #         name='Traceback',
                #         value=f'<See Log>',
                #         inline=False,
                #     )
                #     await error_message.edit(embed=error_embed)
                # finally:
                #     await error_message.remove_reaction(COMMAND_DEBUG_REACTION, ctx.bot.user)
        self.bot.event(on_command_error)
        self.log.info('Registered "on_command_error" method.')


if __name__ == '__main__':
    mb = MechaBaozi()
    mb.run()
