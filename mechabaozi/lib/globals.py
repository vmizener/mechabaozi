import os


BOT_DESCRIPTION = 'Baozi of the less edible variety'
COMMAND_PREFIX = '!'
COMMAND_DEBUG_REACTION = ':grey_question:'
STARTUP_EXTENSIONS = [
    'lib.cogs.help',
    'lib.cogs.opendotastats',
    'lib.cogs.owner',
    'lib.cogs.social',
]

LOGPATH = '/tmp/mechabaozi_logs'
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)

_fabspath = os.path.abspath(os.path.dirname(__file__))

_extpath = os.path.join(_fabspath, '..', '..', 'include')
HERO_INFO_PATH = os.path.join(_extpath, 'dotaconstants/build/heroes.json')

_datpath = os.path.join(_fabspath, '..', 'data')
CLIENT_INFO_PATH = os.path.join(_datpath, 'client_info.json')
PLAYER_INFO_PATH = os.path.join(_datpath, 'stats_playerids.csv')
