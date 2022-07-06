from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news.html'
    context_object_name = 'news'
    # paginate_by = 10


class PostsDetail(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'single'
    pk_url_kwarg = 'id'
