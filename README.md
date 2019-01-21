# rssbot

a simple implementation of a rss reader bot for telegram.

## Usage

- Clone this repo.
- Install dependencies using pip `pip install -r requirements.txt`.
- Config. `cp config.dev.yml config.yml` and edit `config.yml`.
- You can simply run `loop.py` script or add cron look like this`*/5 * * * * python3 /path/to/rssbot/main.py >> /path/to/rssbot/log.log 2>&1`

## Feature

- filter rss by title/author/description and so on

## Thanks to

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [feedparser](https://pythonhosted.org/feedparser/index.html)
