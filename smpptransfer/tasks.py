from __future__ import absolute_import, unicode_literals

from celery import shared_task

from smpptransfer.utils.reader_helper import init_messages_fetch
from smpptransfer.utils.sender_helper import init_sending_scheduled_messages


@shared_task(name="fetch_messages", bind=True)
def fetch_messages(self):
    init_messages_fetch()
    return "Job Completed"


@shared_task(name="retry_unsent_messages", bind=True)
def sent_unsent_message(self):
    init_sending_scheduled_messages()
    return "Job Completed"
