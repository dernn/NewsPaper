from django.urls import path
from news.views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # for upd. requirements D7.7
    path('add/', PostCreateView.as_view(), name='articles_create'),
    # path('<int:pk>/edit/', PostUpdateView.as_view(), name='articles_edit'),
    # path('<int:pk>/delete/', PostDeleteView.as_view(), name='articles_delete'),
]
