import os

LOGPATH = '/tmp/mechabaozi_logs/'
OPENDOTA_API = 'https://api.opendota.com/api'

fabspath = os.path.abspath(os.path.dirname(__file__))
PLAYER_INFO_PATH = os.path.join(fabspath, 'data/stats_playerids.csv')
CLIENT_INFO_PATH = os.path.join(fabspath, 'data/client_info.json')
