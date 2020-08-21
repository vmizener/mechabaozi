import asyncio
import datetime
import discord
import json
import logging
import sys
import traceback

from discord.ext import commands

from lib.globals import \
    COMMAND_PREFIX, BOT_DESCRIPTION,  STARTUP_EXTENSIONS, \
    COMMAND_DEBUG_REACTION


class MechaBaozi:
    def __init__(self, client_token):
        """
        HEY WORLD
        """
        print("logger:", __name__)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing.')

        self.token = client_token
        self.logger.debug(f'Token set: {self.token}.')

        bot = commands.Bot(
            description=BOT_DESCRIPTION,
            command_prefix=COMMAND_PREFIX,
            help_command=None,
        )
        self.bot = bot
        self.logger.info('Bot spawned.')

        self.register_on_ready()
        self.register_on_command_error()

        self.logger.info('Loading extensions:')
        for extension_import_path in STARTUP_EXTENSIONS:
            self.bot.load_extension(extension_import_path)
            self.logger.info(f'- {extension_import_path}')

        self.logger.info('Bot initialized successfully.')

    def run(self):
        self.logger.info('Activating bot.')
        self.bot.run(self.token, bot=True, reconnect=True)

    def register_on_ready(self):
        async def on_ready():
            server_strings = '\n'.join([f'- {s.name}::{s.id}' for s in self.bot.guilds])
            self.logger.info(
                f'Logged in as: {self.bot.user.name}#{self.bot.user.id}\n'
                f'Discord API v{discord.__version__}\n'
                f'Running on {len(self.bot.guilds)} servers:\n{server_strings}'
            )
        self.bot.event(on_ready)
        self.logger.info('Registered "on_ready" method.')

    def register_on_command_error(self):
        async def on_command_error(ctx, exception):
            fmt_tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.logger.error(f"Encountered exception:\n\t{exception}\n{fmt_tb}")
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
                error_embed = discord.Embed(
                    title='',
                    timestamp=datetime.datetime.utcnow(),
                    description=f'```py\n{exception}```\nSee log for details.',
                    color=discord.Color.from_rgb(200, 0, 0),
                )
                error_embed.set_author(
                    name=str(ctx.message.author),
                    icon_url=str(ctx.message.author.avatar_url),
                )
                error_embed.set_footer(text=str(type(exception).__name__))
                error_message = await ctx.send(embed=error_embed)
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
        self.logger.info('Registered "on_command_error" method.')
