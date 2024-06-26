from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rate = int(self.post_set.all().aggregate(rate=models.Sum('rating') * 3).get('rate') or 0)
        comment_rate = int(self.user.comment_set.all().aggregate(rate=models.Sum('rating')).get('rate') or 0)

        feedback_users = sum([int(Comment.objects.filter(post=post).exclude(user=self.user).aggregate(
            rate=models.Sum('rating')).get('rate') or 0) for post in self.post_set.all()])

        self.rating = post_rate + comment_rate + feedback_users
        self.save()

    def __str__(self):
        return self.user.username.title()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # User.<related_name>.all() : вернет все категории, к которым подписан пользователь
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    SIZE = [
        (article, 'Article'),
        (news, 'News')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name=_('Author'),
                               )
    size = models.CharField(max_length=2,
                            choices=SIZE,
                            default=news,
                            help_text=_('Post size'),
                            verbose_name=_('Size')
                            )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Pud Date'))
    category = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=60, verbose_name=_('Headline'))
    content = models.TextField(verbose_name=_('Content'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    def __str__(self):
        return f'{self.headline}: {self.content[:40]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    # for D11.4: The low-level cache API
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
