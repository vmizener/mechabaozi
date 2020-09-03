import asyncio
import csv
import datetime
import discord
import json
import requests

from discord.ext import commands

from lib.base_cog import BaseCog
from lib.command import command
from lib.globals import \
        COMMAND_PREFIX, COMMAND_REACTION_APPROVE, COMMAND_REACTION_DENY, COMMAND_REACTION_SUCCESS, \
        PLAYER_INFO_PATH

OPEN_DOTA_API_PATH = 'https://api.opendota.com/api'
OPEN_DOTA_WEBSITE_PATH = 'https://www.opendota.com'
STEAM_CDN_ADDRESS = 'https://steamcdn-a.akamaihd.net'


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
        self._ability_id_map = None
        self._ability_info_map = None
        self._game_mode_dict = None
        self._hero_dict = None
        self._permanent_buff_map = None
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

    @property
    def ability_id_map(self):
        if not self._ability_id_map:
            self._ability_id_map = self.api_request('GET', '/constants/ability_ids')
        return self._ability_id_map

    @property
    def ability_info_map(self):
        if not self._ability_info_map:
            self._ability_info_map = self.api_request('GET', '/constants/abilities')
        return self._ability_info_map

    @property
    def game_mode_dict(self):
        if not self._game_mode_dict:
            self._game_mode_dict = self.api_request('GET', '/constants/game_mode')
        return self._game_mode_dict

    @property
    def hero_dict(self):
        if not self._hero_dict:
            self._hero_dict = self.api_request('GET', '/constants/heroes')
        return self._hero_dict

    @property
    def permanent_buff_map(self):
        if not self._permanent_buff_map:
            self._permanent_buff_map = self.api_request('GET', '/constants/permanent_buffs')
        return self._permanent_buff_map

    @staticmethod
    def api_request(method, resource_path):
        url = OPEN_DOTA_API_PATH + resource_path
        return json.loads(requests.request(method, url).text)

    def parse_game_mode(self, match_id):
        match_data = self.api_request('GET', f'/matches/{match_id}')
        game_mode_id = str(match_data['game_mode'])
        raw_name = self.game_mode_dict[game_mode_id]['name']
        parsed_name = ' '.join([word.capitalize() for word in raw_name[10:].split('_')])
        game_mode_info = {}
        for player_data in match_data['players']:
            player_slot = player_data['player_slot']
            game_mode_info[player_slot] = {}
            if parsed_name == 'Ability Draft':
                # Return dict of abilities mapped to player slot
                ability_upgrades = set(player_data['ability_upgrades_arr'])
                player_ability_info = []
                for ability_id in ability_upgrades:
                    try:
                        ability_name = self.ability_id_map[str(ability_id)]
                    except KeyError:
                        # Bad ability ID
                        self.log.warning('Unknown ability parsed')
                        continue
                    if ability_name.startswith('special') or ability_name.startswith('ad_special'):
                        # Ignore talents
                        continue
                    # TODO: use icons
                    ability_info = self.ability_info_map[ability_name]
                    player_ability_info.append(ability_info['dname'])
                game_mode_info[player_slot]['abilities'] = player_ability_info
            if player_data['permanent_buffs']:
                game_mode_info[player_slot]['permanent_buffs'] = {}
                for buff_info in player_data['permanent_buffs']:
                    buff_id = buff_info['permanent_buff']
                    stacks = buff_info['stack_count']
                    try:
                        buff_name = self.ability_info_map[self.permanent_buff_map[str(buff_id)]]['dname']
                    except KeyError:
                        buff_name = ' '.join(
                            [word.capitalize() for word in self.permanent_buff_map[str(buff_id)].split('_')]
                        )
                    game_mode_info[player_slot]['permanent_buffs'][buff_name] = stacks
                self.log.info(game_mode_info[player_slot]['permanent_buffs'])
        return parsed_name, game_mode_info

    # ---------------
    # Commands
    # ---------------

    @command(aliases=['register'])
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
            # TODO: don't always write immediately
            self.write_player_id_map()

    @command(aliases=['lookup'])
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

    @command()
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
        hero_icon = STEAM_CDN_ADDRESS + self.hero_dict[hero_id]['icon']
        team = 'Radiant' if match_data['player_slot'] < 128 else 'Dire'
        game_date = datetime.datetime.fromtimestamp(int(match_data['start_time']))
        player_slot = match_data['player_slot']
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
        game_mode, game_mode_info = self.parse_game_mode(match_id)
        game_mode_embed_value = game_mode
        if game_mode == 'Ability Draft':
            game_mode_embed_value += ''.join(
                [f'\n- *{ability_name}*' for ability_name in game_mode_info[player_slot]['abilities']]
            )
        embed.add_field(
            name='Game Mode',
            value=game_mode_embed_value,
        )
        embed.add_field(
            name='KDA',
            value=f"{match_data['kills']}/{match_data['deaths']}/{match_data['assists']}",
        )
        if 'permanent_buffs' in game_mode_info[player_slot]:
            buff_info = game_mode_info[player_slot]['permanent_buffs']
            value = '\n'.join([f"*{buff_name}*: {stacks}" for buff_name, stacks in buff_info.items()])
            embed.add_field(
                name='Permanent Buffs',
                value=value,
            )
        await ctx.send(embed=embed)
