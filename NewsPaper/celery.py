import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# для запуска воркера/периодических задач [в разных окнах терминала]:
# celery -A <project_name> worker -l INFO --pool=solo
# celery -A <project_name> beat -l INFO

# for D10.5: Periodic Tasks #crontab
app.conf.beat_schedule = {
    'mailing_every_monday_8am': {
        'task': 'mailing.tasks.celery_weekly_mailing',
        # каждый понедельник в 8.00 утра
        'schedule': crontab(minute=0, hour=8, day_of_week='mon'),
        'args': (),
    },
}
