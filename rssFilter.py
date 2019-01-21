import logging
import re
from time import mktime, gmtime

logger = logging.getLogger(__name__)


class RssFilter():
    def __init__(self, feedEntries):
        '''
        param: feedEntries feedparser.entries
        see: https://pythonhosted.org/feedparser/index.html
        '''
        if not feedEntries:
            self.feedEntries = []
            return
        if not isinstance(feedEntries, list):
            raise Exception(
                'RssFilter Error: unexpected feedEntries type {}'.format(type(feedEntries)))
        self.feedEntries = feedEntries

    def __getattr__(self, attr):
        if not isinstance(attr, str) or not attr.startswith('filter_'):
            # return lambda id: RssFilter(self.feedEntries)
            raise Exception(
                'RssFilter Error: unexpected attribute \'{}\''.format(attr))

        filterAttr = attr[len('filter_'):]
        return lambda reg: self.rssFilter(filterAttr, reg)

    def rssFilter(self, filterAttr, regex):
        pattern = re.compile(regex)
        feedEntriesAfter = list(
            filter(lambda entity: pattern.match(entity[filterAttr]), self.feedEntries))
        return RssFilter(feedEntriesAfter)

    def filterTime(self, time):
        feedEntriesAfter = list(
            filter(lambda entity: (mktime(gmtime()) - mktime(entity.updated_parsed)) < time, self.feedEntries))
        return RssFilter(feedEntriesAfter)
