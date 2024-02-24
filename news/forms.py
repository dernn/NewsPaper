from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        # убрали поле 'author', исключив возможность его редактировать
        fields = ['size', 'category', 'headline', 'content']
        widgets = {'category': CheckboxSelectMultiple}
