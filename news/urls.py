from django.urls import path
from .views import PostsList, PostsDetail

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:id>', PostsDetail.as_view()),
]
