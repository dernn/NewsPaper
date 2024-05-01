import re

# миксин для проверки прав доступа
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache  # cache import
# raises 'Http404' instead of the model’s 'DoesNotExist' exception
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect  # for set_timezone function view [D17.5]
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import django_filters
from mailing.utils import post_limit_exceeded
from rest_framework import viewsets

from .filters import PostFilter
from .forms import PostForm
from .models import Category, Post, Author

from .serializers import PostSerializer, AuthorSerializer, CategorySerializer


class PostsListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 5


class PostsDetailView(DetailView):
    model = Post
    template_name = 'news/single.html'
    context_object_name = 'single'

    # for D11.4: The low-level cache API
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        # Кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, и если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


# отдельная вьюшка под поиск
class SearchListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news/news.html'
    context_object_name = 'news'
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

    # альтернативное решение Field.initial/Field.disabled
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        # for D9.4
        if post_limit_exceeded(Post, post):
            return render(self.request, 'news/news_create_restrict.html')
        else:
            # for upd. requirements D7.7
            if self.request.path == '/articles/add/':
                post.size = 'AR'
            else:
                post.size = 'NE'
            post.save()
            # alt. for D10.5: вызов таски при сохранении объекта
            # celery_notify_new_post.delay(form.instance.pk)
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


class CategoryListView(PostsListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        # добавляем в queryset атрибут 'category' с текущим инстансом Category
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # берем текущего пользователя из request'a
        # и проверяем его наличие в списке всех пользователей подписанных на категорию
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(size='NE')
    serializer_class = PostSerializer
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ["choose_news", "category"]


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(size='AR')
    serializer_class = PostSerializer


# AuthorViewSet and CategoryViewSet for PostSerializer.fields[]
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'You have successfully subscribed to the category newsletter'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})  # рендерим страницу


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'You have successfully unsubscribed from the category newsletter'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})  # рендерим страницу


#  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться кастомным middleware
def set_timezone(request):
    request.session['django_timezone'] = request.POST['timezone']
    return redirect(request.META.get('HTTP_REFERER'))  # redirects to the previous page
