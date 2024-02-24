from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
import re


class PostsListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news.html'
    context_object_name = 'news'
    # пагинацию на основной странице поставил на 5 для наглядности,
    # чтобы в разбивке получилось больше страниц
    paginate_by = 5


class PostsDetailView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'single'


# отдельная вьюшка под поиск
class SearchListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news.html'
    context_object_name = 'news'
    # и в ней также немного пагинации
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        try:
            context['params'] = re.sub(r'page=\d*\&', '', context['filter'].data.urlencode())
        except AttributeError:
            context['params'] = None
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs


class PostCreateView(CreateView):
    template_name = 'news_create.html'
    # здесь передаем в атрибут модельную форму для создания/редактирования
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        # for upd. requirements D7.7
        if self.request.path == '/articles/add/':
            post.size = 'AR'
        else:
            post.size = 'NE'
        post.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    context_object_name = 'single'
    success_url = '/news/'
