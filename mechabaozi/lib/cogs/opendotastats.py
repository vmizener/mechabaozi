import asyncio
import csv
import datetime
import discord
import json
import requests

from discord.ext import commands

from lib.base_cog import BaseCog
from lib.globals import \
        COMMAND_PREFIX, COMMAND_REACTION_APPROVE, COMMAND_REACTION_DENY, COMMAND_REACTION_SUCCESS, \
        PLAYER_INFO_PATH
from lib.globals import DOTACONSTANTS

OPEN_DOTA_API_PATH = 'https://api.opendota.com/api'
OPEN_DOTA_WEBSITE_PATH = 'https://www.opendota.com'


def setup(bot):
    bot.add_cog(OpenDotaStatsCog(bot))

def teardown(bot):
    print('in teardown')
    bot.get_cog('OpenDotaStats').write_player_id_map()
    print('complete teardown')


class OpenDotaStatsCog(BaseCog, name="OpenDotaStats"):
    def __init__(self, bot):
        super().__init__(bot)
        self.player_id_map = {}
        with open(DOTACONSTANTS.HERO_INFO_PATH, 'r') as fh:
            self.hero_dict = json.load(fh)
        with open(DOTACONSTANTS.GAME_MODE_INFO_PATH, 'r') as fh:
            self.game_mode_dict = json.load(fh)
        self.refresh_player_id_map()

    def __del__(self):
        print('del')
        self.write_player_id_map()

    def refresh_player_id_map(self):
        try:
            with open(PLAYER_INFO_PATH, 'r') as fh:
                for line in csv.reader(fh):
                    if len(line) > 0:
                        player_name, player_id = line
                        self.player_id_map[player_name] = player_id
        except FileNotFoundError:
            open(PLAYER_INFO_PATH, 'w').close()

    def write_player_id_map(self):
        self.log.info("Writing player ID map")
        with open(PLAYER_INFO_PATH, 'w') as fh:
            writer = csv.writer(fh)
            for player_name, player_id in self.player_id_map.items():
                writer.writerow([player_name, player_id])
        self.log.info("Wrote player ID map")

    def api_request(self, method, resource_path):
        url = OPEN_DOTA_API_PATH + resource_path
        return json.loads(requests.request(method, url).text)

    def parse_game_mode(self, match_data):
        game_mode_id = str(match_data['game_mode'])
        raw_name = self.game_mode_dict[game_mode_id]['name']
        return ' '.join([word.capitalize() for word in raw_name[10:].split('_')])

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
        if confirmation:
            self.player_id_map[player_name] = steamid
            await ctx.message.add_reaction(COMMAND_REACTION_SUCCESS)

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
            msg += f'\nUnknown name(s): {bad_names}\nUse `{COMMAND_PREFIX}register to teach me'
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
            await ctx.send(f'I dunno this "{player_name}" guy.  Use `{COMMAND_PREFIX}register` to teach me')
            return

        match_data = self.api_request('GET', '/players/{}/recentMatches'.format(player_id))[0]
        match_id = match_data['match_id']
        hero_id = str(match_data['hero_id'])
        hero = self.hero_dict[hero_id]['localized_name']
        hero_icon = DOTACONSTANTS.CDN_ADDRESS + self.hero_dict[hero_id]['icon']
        team = 'Radiant' if match_data['player_slot'] < 128 else 'Dire'
        game_date = datetime.datetime.fromtimestamp(int(match_data['start_time']))
        embed = discord.Embed(
            timestamp=game_date,
            color=discord.Color.dark_blue(),
            description=f'[OpenDota match link]({OPEN_DOTA_WEBSITE_PATH}/matches/{match_id})',
        )
        duration = str(datetime.timedelta(seconds=match_data['duration']))
        if bool(match_data['radiant_win']) and team == 'Radiant' or not bool(match_data['radiant_win']) and team == 'Dire':
            embed.title = f'Victory in {duration} as {hero}'
        else:
            embed.title = f'Defeat in {duration} as {hero}'
        embed.set_thumbnail(url=hero_icon)
        embed.add_field(
            name='Game Mode',
            value=f'{self.parse_game_mode(match_data)}',
        )
        embed.add_field(
            name='KDA',
            value=f"{match_data['kills']}/{match_data['deaths']}/{match_data['assists']}",
        )
        await ctx.send(embed=embed)
