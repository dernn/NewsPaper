from django.contrib.auth.models import User
from django.views.generic import UpdateView

# для апгрейда аккаунта до 'authors'
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# и записи в модель 'Author'
from news.models import Author
# редактирование профиля
from .forms import UserForm


# альтернативный способ декорирования класса
# @method_decorator(login_required, name='dispatch')
# имя декорированной функции передаем аргументов 'name='
class UserUpdateView(UpdateView):
    template_name = 'sign/profile.html'
    form_class = UserForm
    # отключаем возможность редактировать поле 'email'
    form_class.base_fields['email'].disabled = True
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        # id авторизованного пользователя получаем из request'a
        id = self.request.user.pk
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
