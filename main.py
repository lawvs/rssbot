#!/usr/bin/env python3
import os
import sys
import logging
import requests
import feedparser

from rssFilter import RssFilter
from bot import bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - [%(levelname)s] %(message)s",
    level=logging.INFO
)

from config import config

logger = logging.getLogger(__name__)

if sys.version_info[0] < 3:
    logger.warn("NOTICE: Your python version is lower than 3!")

if config.get('debug'):
    logging.getLogger('root').setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)


def getFeedEntries(url):
    proxy = config.get('proxy')
    if proxy:
        proxies = {
            'https': proxy
        }
        resp = requests.get(url, proxies=proxies)
        feed = feedparser.parse(resp.text)
    else:
        feed = feedparser.parse(url)
    entries = feed.get('entries', [])
    if len(entries) == 0:
        logger.warn('empty entries!')
    return entries


def main():
    subscriptionList = config.get('subscriptions', [])
    for subInfo in subscriptionList:
        logger.debug('checking {}...'.format(subInfo['name']))
        try:
            entries = getFeedEntries(subInfo['url'])
            # filter
            rssFilter = RssFilter(entries)
            interval = config.get('interval')
            if interval:
                rssFilter = rssFilter.filterTime(config.get('interval'))
            else:
                logger.warn('config.interval not set!')
            for key, value in subInfo.items():
                if key.startswith('filter_') and value:
                    rssFilter = getattr(rssFilter, key)(value)

            entries = rssFilter.feedEntries[::-1]  # reverse

            # send message
            for item in entries:
                bot.sendRssUpdateMessage(subInfo, item)
        except Exception:
            logger.exception('Exception in {}'.format(
                subInfo['name']))

    logger.info('done!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
