#!/usr/bin/env python3
import main
import time
import logging
from config import config

logger = logging.getLogger(__name__)


def loop():
    while True:
        main.main()
        logger.info('sleep {}s...'.format(config['interval']))
        time.sleep(config['interval'])


if __name__ == '__main__':
    loop()
