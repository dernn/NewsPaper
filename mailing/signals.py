from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from mailing.utils import send_notification
from news.models import PostCategory


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
