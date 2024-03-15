from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from mailing.tasks import celery_notify_new_post
from news.models import PostCategory


# в ресивер передаем событие присваивания категории публикации
# изменение связи many2many_changed в модели PostCategory
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):  # instance : объект статьи
    # будет реагировать только на создание нового поста
    if kwargs['action'] == 'post_add':
        # при срабатывании вызываем celery-задачу (@shared_task)
        celery_notify_new_post.delay(instance.pk)  # delay() передаём не объект, но только id
        # вся логика сигнала теперь в mailing.tasks [celery, D10.5]
