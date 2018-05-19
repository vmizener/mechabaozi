import json
import logging

from config import COMMAND_PREFIX
from config import CLIENT_INFO_PATH

from discord.ext import commands

from cogs.interactions import Interactions
from cogs.opendotastats import OpenDotaStats

class MechaBaozi:
    def __init__(self):
        """
        HEY WORLD
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing.')

        description = 'Baozi of the less edible variety.'
        bot = commands.Bot(description=description, command_prefix=COMMAND_PREFIX, pm_help=False)
        self.logger.debug('Bot instantiated.')

        @bot.event
        async def on_ready():
            self.logger.info('Logged in as: {}'.format(bot.user.name))

        self.logger.debug('Adding cogs.')
        bot.add_cog(Interactions(bot))
        bot.add_cog(OpenDotaStats(bot))

        self.bot = bot
        self.logger.info('Initialization completed.')

    def run(self):
        self.logger.debug('Reading client info @ {}'.format(CLIENT_INFO_PATH))
        with open(CLIENT_INFO_PATH, 'r') as fh:
            j = json.load(fh)
            self.logger.debug(json.dumps(j))
            self.client_id = j['client_id']
            self.token = j['client_token']
            self.logger.debug('Token set: {}.'.format(self.token))

        self.logger.info('Activating bot.')
        self.bot.run(self.token)

if __name__ == '__main__':
    mb = MechaBaozi()
    mb.run()
