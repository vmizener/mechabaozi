import os
import os.path
import time


BOT_DESCRIPTION = 'Baozi of the less edible variety'
COMMAND_PREFIX = '!'

COMMAND_REACTION_DEBUG = '\N{WHITE QUESTION MARK ORNAMENT}'
COMMAND_REACTION_APPROVE = '\N{THUMBS UP SIGN}'
COMMAND_REACTION_DENY = '\N{THUMBS DOWN SIGN}'
COMMAND_REACTION_SUCCESS = '\N{OK HAND SIGN}'
COMMAND_REACTION_FAIL = '\N{CROSS MARK}'

STARTUP_EXTENSIONS = [
    'lib.cogs.general',
    'lib.cogs.opendotastats',
    'lib.cogs.owner',
    'lib.cogs.social',
]

LOGFORMAT = '//@%(asctime)s [%(levelname)s] %(name)s\n%(message)s'
LOGPATH =f'/tmp/mechabaozi_logs/{time.strftime("%Y%m%d-%H%M%S")}.discord.log'
if not os.path.exists(os.path.dirname(LOGPATH)):
    os.makedirs(os.path.dirname(LOGPATH))

_fabspath = os.path.abspath(os.path.dirname(__file__))
CLIENT_CONFIG_PATH = os.path.join(_fabspath, '..', '..', 'client_config.yaml')
CLIENT_LAUNCHER_PATH = os.path.join(_fabspath, '..', 'mechabaozi.py')

_datpath = os.path.join(_fabspath, '..', 'data')
PLAYER_INFO_PATH = os.path.join(_datpath, 'stats_playerids.csv')

_extpath = os.path.join(_fabspath, '..', '..', 'include')


class DOTACONSTANTS:
    CDN_ADDRESS = 'https://steamcdn-a.akamaihd.net'
    HERO_INFO_PATH = os.path.join(_extpath, 'dotaconstants/build/heroes.json') 
    GAME_MODE_INFO_PATH = os.path.join(_extpath, 'dotaconstants/build/game_mode.json')
