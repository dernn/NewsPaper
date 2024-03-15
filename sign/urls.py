from django.urls import path
# представления "из коробки"
from django.contrib.auth.views import LoginView

from .views import UserUpdateView
from .views import upgrade_me

# добавляем представления в файл конфигурации URL
urlpatterns = [
    # связываем кнопку "Get Author!" из шаблона с функцией-представлением
    path('upgrade/', upgrade_me, name='upgrade'),
    # здесь редактирование профиля
    path('profile/', UserUpdateView.as_view(), name='profile'),
]
