from django.urls import path
# представления "из коробки"
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import LogoutView
# from .views import BaseRegisterView

from .views import UserUpdateView
from .views import upgrade_me

# добавляем представления в файл конфигурации URL
urlpatterns = [
    path('login/',
         # для представлений "из коробки" указываем шаблон
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    # path('logout/',
    #      LogoutView.as_view(template_name='sign/logout.html'),
    #      name='logout'),
    # path('signup/',
    #      BaseRegisterView.as_view(template_name='sign/signup.html'),
    #      name='signup'),
    # связываем кнопку "Get Author!" из шаблона с функцией-представлением
    path('upgrade/', upgrade_me, name='upgrade'),
    # здесь редактирование профиля
    path('profile/', UserUpdateView.as_view(), name='profile'),
]
