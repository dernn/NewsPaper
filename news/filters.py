from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateInput
from .models import Post


class PostFilter(FilterSet):
    author__user__username = CharFilter(lookup_expr='icontains', label='Author contains')
    pub_date = DateTimeFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'headline': ['icontains'],
        }
