from datetime import datetime
from pprint import pprint

from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.shortcuts import redirect

from mailing.utils import send_notification
from news.models import PostCategory, Post


# в ресивер передаем событие присваивания категории публикации
# изменение связи many2many_changed в модели PostCategory
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):  # instance : объект статьи
    # будет реагировать только на создание нового поста
    if kwargs['action'] == 'post_add':
        # получаем список всех категорий новой публикации
        categories = instance.category.all()
        subscribers = set()

        # проходимся for'ом по всем категориям
        for cat in categories:
            # set пользователей вместо list;
            subscribers = subscribers.union(cat.subscribers.all())

        send_notification(instance.preview, instance.pk, instance.category, instance.headline, subscribers)


# ресивер для: "Один пользователь не может публиковать более трёх постов в сутки" [D9.4]
@receiver(pre_save, sender=Post)
def post_limit_exceeded(sender, instance, **kwargs):
    qty_posts = sender.objects.filter(author=instance.author_id,
                                      # число постов за сегодняшнюю дату [без времени]
                                      pub_date__date=datetime.now().date(),)

    if qty_posts.count() > 2:
        raise ValidationError('You cannot publish more than 3 posts per day.')
