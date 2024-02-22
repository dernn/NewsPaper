# UserCreationForm базовая форма для создания пользователя
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Кастомизируем форму регистрации SignupForm из пакета allauth,
# чтобы при успешном прохождении регистрации добавлять пользователя к базовой группе
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from django.forms import ModelForm


# # Базовая реализация SignIn/SignUp
# class BaseRegisterForm(UserCreationForm):
#     # добавляем в форму-наследницу новые поля
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     # и передаем в Meta-класс
#     class Meta:
#         # в модели User(AbstractUser) поля почта, имя и фамилия есть по умолчанию
#         model = User
#         fields = ("username",  # поля "из коробки" UserCreationForm
#                   "first_name",  # поля модели User(AbstractUser)
#                   "last_name",  # поля модели User(AbstractUser)
#                   "email",  # поля модели User(AbstractUser)
#                   "password1",  # поля "из коробки" UserCreationForm
#                   "password2",)  # поля "из коробки" UserCreationForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


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
