import json
import logging

from discord.ext import commands

from lib.cogs.interactions import SocialInteractions
from lib.cogs.opendotastats import OpenDotaStats
from lib.globals import COMMAND_PREFIX
from lib.globals import CLIENT_INFO_PATH

class MechaBaozi:
    def __init__(self):
        """
        HEY WORLD
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing.')

        description = 'Baozi of the less edible variety.'
        bot = commands.Bot(
            description=description,
            command_prefix=COMMAND_PREFIX,
            pm_help=False,
        )
        self.logger.debug('Bot instantiated.')

        @bot.event
        async def on_ready():
            self.logger.info(f'Logged in as: {bot.user.name}')

        self.logger.debug('Adding cogs.')
        bot.add_cog(SocialInteractions(bot))
        bot.add_cog(OpenDotaStats(bot))

        self.logger.debug(f'Reading client info @ {CLIENT_INFO_PATH}')
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
        self.bot.run(self.token)
