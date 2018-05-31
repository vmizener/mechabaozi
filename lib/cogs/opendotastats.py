import csv
import discord
import json
import logging
import requests

from discord.ext import commands

from config import HERO_INFO_PATH
from config import PLAYER_INFO_PATH

BASE_PATH = 'https://api.opendota.com/api'

class OpenDotaStats:
    def __init__(self, bot):
        self.bot = bot
        self.player_dict = {}
        self.hero_info_dict = {}
        self.logger = logging.getLogger(__name__)
        self._load_info()

    def _load_info(self):
        # Load player IDs
        with open(PLAYER_INFO_PATH, 'r') as fh:
            for line in csv.reader(fh):
                if len(line) > 0:
                    player_name, player_id = line
                    self.player_dict[player_name] = player_id
        # Load hero info
        with open(HERO_INFO_PATH, 'r') as fh:
            self.hero_dict = json.load(fh)

    def request(self, method, url):
        return json.loads(requests.request(method, url).text)

    @commands.command(pass_context=True, no_pm=False)
    async def lastmatch(self, ctx, player=''):
        if not player:
            player = ctx.message.author.display_name
        try:
            player_id = self.player_dict[player]
        except KeyError:
            msg = 'i don\'t know this "{}" guy.'.format(player)
            await self.bot.say(msg)
            return
            
        j = self.request('GET', BASE_PATH + '/players/{}/recentMatches'.format(player_id))[0]
        hero = self.hero_dict[str(j['hero_id'])]['localized_name'].lower()
        team = 'Radiant' if j['player_slot'] < 128 else 'Dire'
        if bool(j['radiant_win']) and team == 'Radiant' or not bool(j['radiant_win']) and team == 'Dire':
            await self.bot.say('grats on the w as {}'.format(hero))
        else:
            await self.bot.say('feeding as {} yet again'.format(hero))
