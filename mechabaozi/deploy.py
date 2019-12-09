import code
import logging
import sys
import time

from config import LOGPATH

from mechabaozi import MechaBaozi

def main():
    log_path = f'{LOGPATH}/{time.strftime("%Y%m%d-%H%M%S")}.discord.log'
    log_formatter = logging.Formatter('//@%(asctime)s [%(levelname)s]\n%(message)s')
    logger = logging.getLogger('mechabaozi')

    logfile_handler = logging.FileHandler(log_path)
    logfile_handler.setFormatter(log_formatter)
    logger.addHandler(logfile_handler)

    logstrm_handler = logging.StreamHandler(sys.stdout)
    logstrm_handler.setFormatter(log_formatter)
    logger.addHandler(logstrm_handler)

    logger.setLevel(logging.DEBUG)
    logger.info('Logging set up successfully')
    mb = MechaBaozi()
    mb.run()

if __name__ == '__main__':
    main()
