import asyncio
import datetime
import discord
import json
import logging

from discord.ext import commands

from lib.globals import \
    COMMAND_PREFIX, BOT_DESCRIPTION, CLIENT_INFO_PATH, STARTUP_EXTENSIONS, \
    COMMAND_DEBUG_REACTION


class MechaBaozi:
    def __init__(self):
        """
        HEY WORLD
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing.')

        description = 'Baozi of the less edible variety.'
        bot = commands.Bot(
            description=BOT_DESCRIPTION,
            command_prefix=COMMAND_PREFIX,
        )
        self.logger.info('Bot spawned.')

        @bot.event
        async def on_ready():
            self.logger.info(f'Logged in as: {bot.user.name}#{bot.user.id}')
            self.logger.info(f'Version: {discord.__version__}')
            server_strings = '\n'.join([f'- {s.name}::{s.id}' for s in bot.guilds])
            self.logger.info(f'Running on {len(bot.guilds)} servers:\n{server_strings}')
        self.logger.info('Registered "on_ready" method.')

        @bot.event
        async def on_command_error(ctx, exception):
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
                    description=f'```py\n{exception}```',
                    color=discord.Color.from_rgb(200, 0, 0),
                )
                error_embed.set_author(
                    name=str(ctx.message.author),
                    icon_url=str(ctx.message.guild.get_member(ctx.message.author.id).avatar_url),
                )
                error_embed.set_footer(text=str(type(exception).__name__))
                error_message = await ctx.send(embed=error_embed)
                await error_message.add_reaction(COMMAND_DEBUG_REACTION)
                try:
                    reaction, user = await ctx.bot.wait_for(
                        'reaction_add',
                        timeout=15.0,
                        check=lambda rct, usr: usr != ctx.bot.user and str(rct.emoji) == COMMAND_DEBUG_REACTION,
                    )
                except asyncio.TimeoutError:
                    pass
                else:
                    error_embed.add_field(
                        name='Details',
                        value=f'{exception.__doc__}',
                        inline=False,
                    )
                    error_embed.add_field(
                        name='Cause',
                        value=f'{exception.__cause__}',
                        inline=False,
                    )
                    await error_message.edit(embed=error_embed)
                finally:
                    await error_message.remove_reaction(COMMAND_DEBUG_REACTION, ctx.bot.user)
        self.logger.info('Registered "on_command_error" method.')

        self.logger.info('Loading extensions:')
        for extension_import_path in STARTUP_EXTENSIONS:
            bot.load_extension(extension_import_path)
            self.logger.info(f'- {extension_import_path}')

        self.logger.info(f'Reading client info @ {CLIENT_INFO_PATH}')
        with open(CLIENT_INFO_PATH, 'r') as file_handle:
            json_dict = json.load(file_handle)
            self.logger.debug(json.dumps(json_dict))
            self.client_id = json_dict['client_id']
            self.token = json_dict['client_token']
            self.logger.debug(f'Token set: {self.token}.')

        self.bot = bot
        self.logger.info('Bot initialized successfully.')

    def run(self):
        self.logger.info('Activating bot.')
        self.bot.run(self.token, bot=True, reconnect=True)
