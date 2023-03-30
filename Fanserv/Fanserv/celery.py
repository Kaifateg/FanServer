import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fanserv.settings')

app = Celery('Fanserv')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_when_add_post': {
        'task': 'posts.tasks.send_notifications',
        'schedule': 3600,
    },
}

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'posts.tasks.posts_of_the_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}