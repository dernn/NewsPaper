from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
# from .forms import BaseRegisterForm  # созданная нами модель
# для апгрейда аккаунта до 'authors'
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# и записи в модель 'Author'
from news.models import Author
# редактирование профиля
from .forms import UserForm


# представление к модели BaseRegisterForm
# class BaseRegisterView(CreateView):
#     # модель формы, которую реализует данный дженерик
#     model = User
#     # форма, которая будет заполняться пользователем
#     form_class = BaseRegisterForm
#     # URL для редиректа пользователя после успешного ввода данных в форму
#     success_url = '/'


class UserUpdateView(UpdateView):
    template_name = 'sign/profile.html'
    form_class = UserForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)


# проверка аутентификации через декоратор
@login_required
def upgrade_me(request):
    # объект текущего пользователя
    user = request.user
    # группа 'authors' из модели Group
    authors_group = Group.objects.get(name='authors')
    # проверяем наличие пользователя в группе
    if not user.groups.filter(name='authors').exists():
        # и добавляем, в случае его отсутствия
        authors_group.user_set.add(user)
        # а также создаем запись к модели Author
        Author.objects.create(user=user)
    # перенаправляем пользователя на корневую страницу
    return redirect('/')
