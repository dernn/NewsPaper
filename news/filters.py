from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateInput
from .models import Post


class PostFilter(FilterSet):
    # имя автора фильтруем через связь OneToOneField с базовой моделью User;
    author__user__username = CharFilter(lookup_expr='icontains', label='Author contains')
    # здесь простенький датапикер, фильтрующий по логике "позже какой-либо даты" ['gt']
    pub_date = DateTimeFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        # и в метакласс только фильтр по заголовку
        fields = {
            'headline': ['icontains'],
        }
