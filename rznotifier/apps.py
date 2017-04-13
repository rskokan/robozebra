import logging

from django.apps import AppConfig

from .utils import SlackCleaner

logger = logging.getLogger('robozebra.apps')


class RznotifierConfig(AppConfig):
    name = 'rznotifier'

    def ready(self):
        slack_cleaner = SlackCleaner('vvv')  # @viktorcistic
        slack_cleaner.listen()
        logger.info('App initialized')
