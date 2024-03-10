from celery import shared_task

from mailing.utils import send_notification
from news.models import Post


@shared_task
def celery_notify_new_post(pk):
    instance = Post.objects.get(pk=pk)  # вызываем вновь объект
    categories = instance.category.all()
    subscribers = set()

    # проходимся for'ом по всем категориям
    for cat in categories:
        # set пользователей вместо list;
        subscribers = subscribers.union(cat.subscribers.all())

    send_notification(instance.preview, instance.pk, instance.category, instance.headline, subscribers)

