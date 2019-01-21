import os
import sys
import yaml
import logging

logger = logging.getLogger(__name__)


def loadEnv():
    env = os.environ.get('ENV')
    if env:
        return env
    if '.dev' in os.listdir():
        return 'dev'
    elif '.prod' in os.listdir():
        return 'prod'
    return None


def loadConfig():
    env = loadEnv()
    configFileName = 'config.yml'
    if env:
        configFileName = 'config.{}.yml'.format(env)
    logger.debug('load config {}'.format(configFileName))
    configPath = os.path.join(sys.path[0], configFileName)
    with open(configPath, 'r', encoding='utf8') as f:
        config = yaml.load(f)
    return config


config = loadConfig()
