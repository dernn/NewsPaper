from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rate = int(self.post_set.all().aggregate(rate=models.Sum('rating') * 3).get('rate') or 0)
        comment_rate = int(self.user.comment_set.all().aggregate(rate=models.Sum('rating')).get('rate') or 0)

        feedback_users = sum([int(Comment.objects.filter(post=post).exclude(user=self.user).aggregate(
            rate=models.Sum('rating')).get('rate') or 0) for post in self.post_set.all()])

        # feedback_users = 0
        # for post in self.post_set.all():
        #     rate = int(Comment.objects.filter(post_id=post.pk).exclude(user_id=self.user_id).aggregate(
        #         rate=models.Sum('rating')).get('rate') or 0)
        #     feedback_users += rate

        self.rating = post_rate + comment_rate + feedback_users
        self.save()

    def __str__(self):
        return self.user.username.title()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    SIZE = [
        (article, 'Article'),
        (news, 'News')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    size = models.CharField(max_length=2,
                            choices=SIZE,
                            default=news)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=60)
    content = models.TextField()
    rating = models.IntegerField(default=0)

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
