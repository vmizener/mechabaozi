#!/usr/bin/env python3

import logging
import sys
import time
import yaml

from lib.globals import CLIENT_INFO_PATH, LOGPATH

from mechabaozi import MechaBaozi


def main():
    log_path = f'{LOGPATH}/{time.strftime("%Y%m%d-%H%M%S")}.discord.log'
    log_formatter = logging.Formatter('//@%(asctime)s [%(levelname)s] %(name)s\n%(message)s')
    logger = logging.getLogger("mechabaozi")

    logfile_handler = logging.FileHandler(log_path)
    logfile_handler.setFormatter(log_formatter)
    logger.addHandler(logfile_handler)

    logstrm_handler = logging.StreamHandler(sys.stdout)
    logstrm_handler.setFormatter(log_formatter)
    logger.addHandler(logstrm_handler)

    logger.setLevel(logging.INFO)
    logger.info('Logging set up successfully')

    logger.info(f'Reading client info @ {CLIENT_INFO_PATH}')
    with open(CLIENT_INFO_PATH, 'r') as file_handle:
        client_token = yaml.safe_load(file_handle)['client_token']
    logger.info('Successfully parsed token')
    mb = MechaBaozi(client_token)
    mb.run()

if __name__ == '__main__':
    main()
