import os


BOT_DESCRIPTION = 'Baozi of the less edible variety'
COMMAND_PREFIX = '!'
COMMAND_DEBUG_REACTION = '\N{WHITE QUESTION MARK ORNAMENT}'
STARTUP_EXTENSIONS = [
    'lib.cogs.help',
    'lib.cogs.opendotastats',
    'lib.cogs.owner',
    'lib.cogs.social',
]

MAX_MESSAGE_LENGTH = 1800

LOGPATH = '/tmp/mechabaozi_logs'
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)

_fabspath = os.path.abspath(os.path.dirname(__file__))
CLIENT_INFO_PATH = os.path.join(_fabspath, '..', '..', 'client_info.yaml')

_extpath = os.path.join(_fabspath, '..', '..', 'include')
HERO_INFO_PATH = os.path.join(_extpath, 'dotaconstants/build/heroes.json')

_datpath = os.path.join(_fabspath, '..', 'data')
PLAYER_INFO_PATH = os.path.join(_datpath, 'stats_playerids.csv')
