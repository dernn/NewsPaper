from django.contrib.auth.models import User
# Кастомизируем форму регистрации SignupForm из пакета allauth,
# чтобы при успешном прохождении регистрации добавлять пользователя к базовой группе
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  )


# наследуем и переопределяем allauth.account.forms.SignupForm
class BasicSignupForm(SignupForm):

    # переопределим метод save
    def save(self, request):
        # вызываем метод класса-родителя
        user = super(BasicSignupForm, self).save(request)
        # получаем объект модели группы basic
        basic_group = Group.objects.get(name='common')
        # user_set возвращаем список пользователей группы,
        # add(user) добавляет нового пользователя в список
        basic_group.user_set.add(user)
        return user
