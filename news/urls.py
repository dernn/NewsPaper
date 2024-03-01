from django.urls import path
from .views import PostsListView, PostsDetailView, SearchListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import subscribe, unsubscribe
# for D9.2
from .views import CategoryListView

urlpatterns = [
    path('', PostsListView.as_view()),
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
]
