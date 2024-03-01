from django.conf import settings  # LazySettings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_notification(preview, pk, headline, subscribers):
    html_content = render_to_string(
        'mailing/post_created_email.html',
        {
            # обрезает до 124 символов, чтобы было чуть больше текста, чем ничего;
            'text': preview,  # preview здесь метод из модели Post;
            'link': f'{settings.SITE_URL}/news/{pk}',
            # 'username': username,
        }
    )

    msg = EmailMultiAlternatives(
        subject=headline,
        body='',  # body задаем выше в шаблоне
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
