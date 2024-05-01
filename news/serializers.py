from django.contrib.auth.models import User

from .models import Post, Author, Category
from rest_framework import serializers


# AuthorSerializer for PostSerializer.fields['author']
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'url', ]
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'pk'}
        }


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.CharField(source="author.user.username", read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    content = serializers.SerializerMethodField()

    # slice text-content
    def get_content(self, obj):
        return obj.content[:100] + '...'

    class Meta:
        model = Post
        fields = ['id', 'size', 'author', 'pub_date', 'headline', 'content', 'category', ]
        extra_kwargs = {
            'url': {'view_name': 'post-detail', 'lookup_field': 'pk'}
        }


# UserSerializer for AuthorSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_login', ]


# AuthorSerializer for PostSerializer.fields['author']
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ['id', 'url', 'user', 'rating', ]
        extra_kwargs = {
            'url': {'view_name': 'author-detail', 'lookup_field': 'pk'}
        }
