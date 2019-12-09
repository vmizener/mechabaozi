import os

COMMAND_PREFIX = '!'

LOGPATH = '/tmp/mechabaozi_logs'
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)

fabspath = os.path.abspath(os.path.dirname(__file__))
CLIENT_INFO_PATH = os.path.join(fabspath, 'data/client_info.json')
HERO_INFO_PATH = os.path.join(fabspath, '..', 'include/dotaconstants/build/heroes.json')
PLAYER_INFO_PATH = os.path.join(fabspath, 'data/stats_playerids.csv')
