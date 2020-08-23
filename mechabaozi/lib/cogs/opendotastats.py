import asyncio
import csv
import discord
import json
import requests

from discord.ext import commands

from lib.base_cog import BaseCog
from lib.globals import COMMAND_PREFIX, COMMAND_REACTION_APPROVE, COMMAND_REACTION_DENY, PLAYER_INFO_PATH
from lib.globals import DOTACONSTANTS

OPEN_DOTA_API_PATH = 'https://api.opendota.com/api'


def setup(bot):
    bot.add_cog(OpenDotaStatsCog(bot))


class OpenDotaStatsCog(BaseCog, name="OpenDotaStats"):
    def __init__(self, bot):
        super().__init__(bot)
        self.player_id_map = {}
        with open(DOTACONSTANTS.HERO_INFO_PATH, 'r') as fh:
            self.hero_dict = json.load(fh)
        self.refresh_player_id_map()

    def refresh_player_id_map(self):
        try:
            with open(PLAYER_INFO_PATH, 'r') as fh:
                for line in csv.reader(fh):
                    if len(line) > 0:
                        player_name, player_id = line
                        self.player_id_map[player_name] = player_id
        except FileNotFoundError:
            open(PLAYER_INFO_PATH, 'w').close()

    def api_request(self, method, resource_path):
        url = OPEN_DOTA_API_PATH + resource_path
        return json.loads(requests.request(method, url).text)

    # ---------------
    # Commands
    # ---------------

    @commands.command(aliases=['register'])
    async def register_player(self, ctx, steamid, player_name=None):
        """ Register someone's steam ID """
        if not player_name:
            player_name = ctx.message.author.display_name
        confirmation = True
        if player_name in self.player_id_map:
            confirmation = await self.request_confirmation(
               ctx,
               message=f'I already have {player_name} registered to ID "{self.player_id_map[player_name]}".  Overwrite?',
            )
            print(confirmation)
        elif confirmation:
            self.player_id_map[player_name] = steamid

    @commands.command(aliases=['lookup'])
    async def lookup_players(self, ctx, *player_names):
        """ Lookup someone's steam ID """
        if not player_names:
            await ctx.send('Uh, need a player name to lookup dude')
            return
        player_ids = []
        bad_names = []
        for player_name in player_names:
            try:
                player_ids.append(str(self.player_id_map[player_name]))
            except KeyError:
                bad_names.append(player_name)
        msg = '\n'.join(player_ids)
        if bad_names:
            msg += f'\nUnknown name(s): {bad_names}'
        await ctx.send(msg)

    @commands.command()
    async def lastmatch(self, ctx, player_name=None):
        """
        the future is now
        """
        if not player_name:
            player_name = ctx.message.author.display_name
        try:
            player_id = self.player_id_map[player_name]
        except KeyError:
            msg = 'i don\'t know this "{}" guy.'.format(player_name)
            await self.bot.say(msg)
            return

        j = self.api_request('GET', '/players/{}/recentMatches'.format(player_id))[0]
        hero = self.hero_dict[str(j['hero_id'])]['localized_name'].lower()
        team = 'Radiant' if j['player_slot'] < 128 else 'Dire'
        if bool(j['radiant_win']) and team == 'Radiant' or not bool(j['radiant_win']) and team == 'Dire':
            await self.bot.say('grats on the w as {}'.format(hero))
        else:
            await self.bot.say('feeding as {} yet again'.format(hero))
