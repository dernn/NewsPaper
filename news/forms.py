from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'size', 'category', 'headline', 'content']
        widgets = {'category': CheckboxSelectMultiple}
