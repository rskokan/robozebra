import logging
from threading import Thread

from django.utils import timezone
from slacker import Slacker
from slacksocket import SlackSocket


def background(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


class SlackLog(object):
    # TODO: change to RTM
    logger = logging.getLogger('robozebra.SlackLog')

    def log(self, level, msg):
        try:
            slack = Slacker('zzz')  # zlatokopka
            slack.chat.post_message('#syslog', '[{}] {}: {}'.format(timezone.now(), level, msg))
        except Exception as ex:
            self.logger.error('Error logging to Slack: {}. Original message: {}'.format(ex, msg))

    def info(self, msg):
        self.log('INFO', msg)

    def error(self, msg):
        self.log('ERROR', msg)

    def debil(self, channel, user):
        try:
            slack = Slacker('zzz')  # zlatokopka
            slack.chat.post_message('#debilog', '[{}] {}'.format(channel, user))
        except:
            pass


class SlackCleaner(object):
    logger = logging.getLogger('robozebra.SlackCleaner')
    slack_logger = SlackLog()
    socket = None

    def __init__(self, token):
        self.socket = SlackSocket(token, translate=True)

    @background
    def listen(self):
        try:
            # self.logger('Listening for Slack events...') # TODO: ask why am I getting "'Logger' object is not callable"
            for event in self.socket.events():
                if not 'type' in event.event or not 'channel' in event.event or not 'user' in event.event:
                    continue

                if not event.event['channel'].startswith('zonky-') or event.event['user'] == 'zlatokopka':
                    continue

                if 'subtype' in event.event and (event.event['subtype'] == 'channel_join'
                                                 or event.event['subtype'] == 'channel_leave'):
                    continue

                if event.event['type'] == 'user_typing':
                    self.warn_user(event.event['user'])
                if event.event['type'] == 'message':
                    self.logger.warn(
                        'Debil: channel: {}, user: {}; event: {}'.format(event.event['channel'], event.event['user'],
                                                                         event.event))
                    self.slack_logger.debil(event.event['channel'], event.event['user'])
        except Exception as ex:
            self.logger.error('Error while listening to Slack: {}'.format(ex))
            self.slack_logger.error('Listening loop probably down! {}'.format(ex))

    def warn_user(self, username):
        try:
            im = self.socket.get_im_channel(user_name=username)
            self.socket.send_msg(
                "Prosim nepis nic do kanalu 'zonky-X' at nespoustis plane notifikace. Kanaly 'zonky-X' jsou urceny jen pro notifikace o novych pujckach.",
                channel_id=im['id'], confirm=False)
        except Exception as ex:
            self.logger.error('Error warning user via Slack: {}'.format(ex))

    def delete_message(self, channel, ts):
        # http://stackoverflow.com/questions/37923772/cannot-delete-a-chat-message-via-slack-api
        pass
