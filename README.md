# robozebra

Robozebra is a Slack notification service for a Czech P2P lending portal http://zonky.cz.

http://robozebra.cz/


Can be ran by e.g. scheduling a cron job:

    * * * * * /usr/bin/curl --silent localhost:8000/notif/fetch-loans/
