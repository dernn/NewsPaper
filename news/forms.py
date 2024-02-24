from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        # убрали поле 'author', исключив возможность его редактировать
        # drop 'size' too for upd. requirements D7.7
        fields = ['category', 'headline', 'content']
        widgets = {'category': CheckboxSelectMultiple}
