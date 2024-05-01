"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from news.views import NewsViewSet, ArticlesViewSet, AuthorViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'articles', ArticlesViewSet, basename='article')
router.register(r'authors', AuthorViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    # эндпоинты для работы с локализацией [переключение языка]
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    # for upd. requirements D7.7
    path('articles/', include('articles.urls')),
    # переадресуем корневую страницу на приложение 'protect'
    path('', include('protect.urls')),
    # и добавим ссылку на приложение регистрации
    path('sign/', include('sign.urls')),
    # подключаем также ссылки из приложения 'allauth'
    path('accounts/', include('allauth.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('api/', include(router.urls)),  # DRF url's [D18.6]
]
