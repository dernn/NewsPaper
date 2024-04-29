from django.utils import timezone  # Time localization [D17.5]
import pytz  # стандартный модуль для работы с часовыми поясами


def tz_ctime(request):
    return {
        'current_time': timezone.localtime(),
        'timezones': pytz.common_timezones,  # добавляем все доступные часовые пояса
    }
