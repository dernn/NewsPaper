from django.urls import path
from django.views.decorators.cache import cache_page  #

from .views import PostsListView, PostsDetailView, SearchListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import subscribe, unsubscribe, set_timezone
# for D9.2
from .views import CategoryListView

urlpatterns = [
    # кэширование главной страницы новостей, 1 минута
    path('', cache_page(60 * 1)(PostsListView.as_view())),
    # кэширование на страницу отдельной новости, 5 минут
    path('<int:pk>', PostsDetailView.as_view(), name='single_detail'),
    # страничка фильтра поиска
    path('search/', SearchListView.as_view(), name='news_search'),
    # страничка создания записи
    path('add/', PostCreateView.as_view(), name='news_create'),
    # здесь редактирование записи
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_update'),
    # и удаления
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    # for D9.2
    path('category/<int:pk>', CategoryListView.as_view(), name='category_news'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('set_timezone/', set_timezone, name='set_timezone'),
]
