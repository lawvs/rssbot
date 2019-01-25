import telegram
from textwrap import dedent
import logging

from config import config

logger = logging.getLogger(__name__)


def formatRss(subInfo, item) -> str:
    return dedent('''
    {name}
    {title}
    Updated: {updated}
    Author: {author}
    [Read More]({link})
    '''.format(
        name=subInfo['name'],
        title=item.title,
        updated=item.updated,
        author=item.author,
        link=item.link
    ))


def sendMessageToDefaultGroup(self, text, **kw):
    chat_id = config['telegram']['default_chat_id']
    return telegram.Bot.send_message(self, chat_id, text, **kw)


def sendRssUpdateMessage(self, configInfo, rss, **kw):
    text = formatRss(configInfo, rss)
    logger.info(text)
    chatId = configInfo.get('chat_id')
    if not chatId:
        self.sendMessageToDefaultGroup(text, parse_mode='Markdown', **kw)
        return

    if isinstance(chatId, str):
        self.send_message(chatId, text, parse_mode='Markdown', **kw)
        return

    if isinstance(chatId, list):
        for i in chatId:
            self.send_message(i, text, parse_mode='Markdown', **kw)
        return
    raise Exception('unexpected type of chat_id in {}, expected \'str|list|None\' but {}'.format(
        configInfo, type(chatId)))


def initBot():
    botToken = config['telegram']['access_token']
    bot = telegram.Bot(token=botToken, request=telegram.utils.request.Request(
        proxy_url=config.get('proxy')))

    # patch
    telegram.Bot.sendMessageToDefaultGroup = sendMessageToDefaultGroup
    telegram.Bot.sendRssUpdateMessage = sendRssUpdateMessage
    if config.get('local'):
        telegram.Bot.send_message = lambda *a, **kw: None  # do nothing
    return bot


bot = initBot()
