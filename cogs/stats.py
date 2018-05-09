import csv
import discord

from discord.ext import commands

from config import OPENDOTA_API
from config import PLAYER_INFO_PATH

class Stats:
    def __init__(self, bot):
        self.bot = bot
        self.player_dict = {}
        self._load_player_ids()

    def _load_player_ids(self):
        with open(PLAYER_INFO_PATH, 'r') as fh:
            for line in csv.reader(fh):
                if len(line) > 0:
                    player_name, player_id = line
                    self.player_dict[player_name] = player_id

    @commands.command(pass_context=True, no_pm=True)
    async def thing(self):
        pass
