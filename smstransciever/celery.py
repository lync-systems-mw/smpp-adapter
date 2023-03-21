import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smstransciever.settings')

app = Celery('smstransciever')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "fetch-messages-every-30-mins": {
        "task": "fetch_messages",
        "schedule": crontab(minute="*/30")
    },
    "resent-unsent-messages-every-1-hour": {
        "task": "retry_unsent_messages",
        "schedule": crontab(hour="*")
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
