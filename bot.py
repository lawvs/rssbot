import telegram
import logging
import html

from config import config

logger = logging.getLogger(__name__)


def escapeMarkdown(s: str) -> str:
    return s.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')


def formatRss(subInfo, item, parseMode=None) -> str:
    def escape(s: str) -> str: return s
    if parseMode == 'Markdown':
        escape = escapeMarkdown
    if parseMode == 'HTML':
        escape = html.escape

    template = subInfo.get('template') or config['template']
    return template.format(
        name=escape(subInfo['name'] or 'Unknown'),
        title=escape(item.get('title') or 'Unknown'),
        updated=escape(item.get('updated') or 'Unknown'),
        author=escape(item.get('author') or 'Unknown'),
        link=item.get('link')
    )


def sendRssUpdateMessage(self, configInfo, rss, **kw):
    chatId = configInfo.get('chat_id') or config['telegram']['default_chat_id']
    parseMode = configInfo.get(
        'parse_mode') or config['telegram'].get('parse_mode')
    text = formatRss(configInfo, rss, parseMode)

    if isinstance(chatId, str):
        self.send_message(chatId, text, parse_mode=parseMode, **kw)
        return

    if isinstance(chatId, list):
        for i in chatId:
            self.send_message(i, text, parse_mode=parseMode, **kw)
        return
    raise Exception('unexpected type of chat_id in {}, expected \'str|list|None\' but {}'.format(
        configInfo, type(chatId)))


def initBot():
    botToken = config['telegram']['access_token']
    bot = telegram.Bot(token=botToken, request=telegram.utils.request.Request(
        proxy_url=config.get('proxy')))

    # patch
    telegram.Bot.sendRssUpdateMessage = sendRssUpdateMessage
    if config.get('local'):
        telegram.Bot.send_message = lambda *a, **kw: None  # do nothing
    return bot


bot = initBot()
