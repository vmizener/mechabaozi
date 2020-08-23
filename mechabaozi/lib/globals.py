import os
import os.path
import time


BOT_DESCRIPTION = 'Baozi of the less edible variety'
COMMAND_PREFIX = '!'
COMMAND_DEBUG_REACTION = '\N{WHITE QUESTION MARK ORNAMENT}'
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

_datpath = os.path.join(_fabspath, '..', 'data')
PLAYER_INFO_PATH = os.path.join(_datpath, 'stats_playerids.csv')

_extpath = os.path.join(_fabspath, '..', '..', 'include')


class DOTACONSTANTS:
    HERO_INFO_PATH = os.path.join(_extpath, 'dotaconstants/build/heroes.json') 
