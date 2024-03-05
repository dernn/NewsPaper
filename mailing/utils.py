from datetime import datetime

from django.conf import settings  # LazySettings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_notification(preview, pk, category, headline, subscribers):
    # каждому пользователю отдельное письмо
    for subscriber in subscribers:
        html_content = render_to_string(
            'mailing/post_created_email.html',
            {
                # обрезает до 124 символов, чтобы было чуть больше текста, чем ничего;
                'text': preview,  # preview здесь метод из модели Post;
                'link': f'{settings.SITE_URL}/news/{pk}',
                # username в контекст
                'username': subscriber.username,
                # строка с перечислением всех категорий
                'category': ' '.join([f'#{cat.name}' for cat in category.all()]),
            }
        )

        msg = EmailMultiAlternatives(
            subject=headline,
            body='',  # body задаем выше в шаблоне
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# функция для [D9.4]: "Один пользователь не может публиковать более трёх постов в сутки"
def post_limit_exceeded(sender, instance, **kwargs):
    qty_posts = sender.objects.filter(author=instance.author,
                                      # число постов за сегодняшнюю дату [без времени]
                                      pub_date__date=datetime.now().date(), )

    if qty_posts.count() > 2:
        return True
