import logging
import sys

import requests
from django.http import HttpResponse
from slacker import Slacker

from .models import Loan
from .utils import SlackLog

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('robozebra.Notifier')


def index(request):
    return HttpResponse('Hello\n')


def fetch_loans(request):
    # TODO: Make it async
    # TODO: Move last_tun to DB: unsynced when there is more workers
    marketplace_url = 'https://api.zonky.cz/loans/marketplace'
    try:
        count = '20'
        if 'count' in request.GET:
            count = request.GET['count']
        logger.debug('Fetching {} loans from {}'.format(count, marketplace_url))

        headers = {'X-Size': count, 'X-Order': '-datePublished'}
        r = requests.get(marketplace_url, headers=headers)
        loans = r.json()
        logger.debug('Fetched loans: {}'.format(loans))
        _process_loans(loans)
#        slog = SlackLog()
#        slog.info('Fetched {} loans from {}'.format(count, marketplace_url))
        return HttpResponse('OK\n')
    except Exception as ex:
        logger.error('Error while fetching/processing loans: {}'.format(ex))
        return HttpResponse('Something went wrong\n')


def _process_loans(loans_json):
    for obj in loans_json:
        existing_loan = Loan.objects.filter(loan_id=obj['id'])
        loan = None
        if existing_loan.count() == 0:
            logger.info('New loan {}'.format(obj['id']))
            loan = _save_new_loan(obj)
        else:
            logger.debug('Existing loan {}'.format(obj['id']))
            loan = existing_loan[0]
            loan.update_values(obj)
            loan.save()

        if not loan.notified and not loan.covered and loan.published:
            _notify_once(loan)


def _save_new_loan(obj):
    loan = Loan(loan_id=obj['id'])
    loan.update_values(obj)
    loan.save()
    return loan


def _notify_once(loan):
    logger.info('Notifying: loan {}'.format(loan.loan_id))
    try:
        slack = Slacker('zzz')
        slack.chat.post_message(loan.get_notif_channel(), loan, as_user=True)
        slack.chat.post_message('#zonky-all', loan, as_user=True)
        loan.notified = True
        loan.save()
    except Exception as ex:
        logger.error('Failed sending notification for loan_id={}: {}'.format(loan.loan_id, ex))
