import discord
import json
import logging

from discord.ext import commands

from lib.globals import COMMAND_PREFIX
from lib.globals import BOT_DESCRIPTION
from lib.globals import CLIENT_INFO_PATH
from lib.globals import STARTUP_EXTENSIONS

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
        self.logger.debug('Bot instantiated.')

        @bot.event
        async def on_ready():
            self.logger.info(f'Logged in as: {bot.user.name}#{bot.user.id}')
            self.logger.info(f'Version: {discord.__version__}')
            server_strings = '\n'.join([f'- {s.name}::{s.id}' for s in bot.guilds])
            self.logger.info(f'Running on {len(bot.guilds)} servers:\n{server_strings}')

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
        self.logger.info('Initialization completed.')

    def run(self):
        self.logger.info('Activating bot.')
        self.bot.run(self.token, bot=True, reconnect=True)
