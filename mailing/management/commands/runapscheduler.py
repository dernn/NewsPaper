"""
Дополнительная команда 'runapscheduler' для manage.py.
Созданные здесь задания можно также запустить из админки.
"""
import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail, EmailMultiAlternatives

from news.models import Post, Category

logger = logging.getLogger(__name__)


# функция еженедельной рассылки
def weekly_mailing():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(pub_date__gte=last_week)  # lookup __gte
    categories = set(posts.values_list('category__name', flat=True))
    categories.remove(None)
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'mailing/weekly_news.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    # время отправки без микросекунд для заголовка
    sending_time = datetime.datetime.now().replace(microsecond=0)

    msg = EmailMultiAlternatives(
        subject=f'News from last week {sending_time}',  # тема письма
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print(f'msg sent {sending_time}')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(day_of_week="wed", hour="16", minute="30"),  # еженедельная рассылка
            id="weekly_mailing",  # уникальный id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mailing'.")

        # и работу по удалению устаревших задач
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
