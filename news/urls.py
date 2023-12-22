from django.urls import path
from .views import PostsListView, PostsDetailView, SearchListView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', PostsListView.as_view()),
    path('<int:pk>', PostsDetailView.as_view(), name='single_detail'),
    # страничка фильтра /news/search
    path('search/', SearchListView.as_view(), name='news_search'),
    path('add/', ProductCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='news_delete'),
]
