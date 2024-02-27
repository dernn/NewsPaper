from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# миксин для проверки прав доступа
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
#
from django.shortcuts import render
from .models import Post
from .filters import PostFilter
from .forms import PostForm
import re


class PostsListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news/news.html'
    context_object_name = 'news'
    # пагинацию на основной странице поставил на 5 для наглядности,
    # чтобы в разбивке получилось больше страниц
    paginate_by = 5


class PostsDetailView(DetailView):
    model = Post
    template_name = 'news/single.html'
    context_object_name = 'single'


# отдельная вьюшка под поиск
class SearchListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news/news.html'
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


class PostCreateView(PermissionRequiredMixin, CreateView):  # <-- PermissionRequiredMixin : проверка прав доступа
    # соглашение для именования разрешений, {'action': 'view-add-delete-change'}:
    # <app>.<action>_<model>
    permission_required = ('news.add_post',)  # выдача разрешения {'action': 'add'} для модели 'post'
    template_name = 'news/news_create.html'
    # здесь передаем в атрибут модельную форму для создания/редактирования
    form_class = PostForm

    # отключаем возможность редактировать поле автор в форме 'PostForm'
    # form_class.base_fields['author'].disabled = True
    # а это удалить при следующем коммите

    # значение поля "author" по умолчанию через 'initial'
    # form_class = PostForm(initial={'author': request.user.username)})  # только как его получить из текущего юзера?

    # альтернативное решение Field.initial/Field.disabled
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


# здесь же проверка аутентификации
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):  # <-- PermissionRequiredMixin : см. выше
    permission_required = ('news.change_post',)
    template_name = 'news/news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # переопределение метода для проверки прав на редактирование
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, template_name='news/post_lock.html', context=context)
        '''
        # проверки на соответствие размера [новость/статья]
        # объявленные шаблоны необходимо добавить в 'templates'
        elif self.request.path == f'/news/{post.pk}/edit/' and post.size != 'NE':
            return render(self.request, template_name='invalid_articles_edit.html', context=context)
        elif self.request.p ath == f'/articles/{post.pk}/edit/' and post.size != 'AR':
            return render(self.request, template_name='invalid_news_edit.html', context=context)
        '''
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    context_object_name = 'single'
    success_url = '/news/'

    # переопределение метода для проверки прав на удаление
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, template_name='news/post_lock.html', context=context)
        '''
        # проверки на соответствие размера [новость/статья]
        # объявленные шаблоны необходимо добавить в 'templates'
        elif self.request.path == f'/news/{post.pk}/edit/' and post.size != 'NE':
            return render(self.request, template_name='invalid_articles_edit.html', context=context)
        elif self.request.p ath == f'/articles/{post.pk}/edit/' and post.size != 'AR':
            return render(self.request, template_name='invalid_news_edit.html', context=context)
        '''
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)