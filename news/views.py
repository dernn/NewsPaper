from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# миксин для проверки прав доступа
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
import re


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


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'You have successfully subscribed to the category newsletter...'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})  # рендерим страницу
