from django.db import models
from django.contrib.auth.models import User
from news.models import *

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
base1 = User.objects.create_user('username8')
base2 = User.objects.create_user('username9')
base3 = User.objects.create_user('username0')

# 2. Создать два объекта модели Author, связанные с пользователями.
user1 = Author.objects.create(user=base1)
user2 = Author.objects.create(user=base2)

# 3. Добавить 4 категории в модель Category.
cate1 = Category.objects.create(name='Education')
cate2 = Category.objects.create(name='Sony')
cate3 = Category.objects.create(name='Films')
cate4 = Category.objects.create(name='Politics')

# 4. Добавить 2 статьи и 1 новость.
post1 = Post.objects.create(author=user1, size=Post.article, headline='Something in the World', content='Some text.')
post2 = Post.objects.create(author=user2, size=Post.article, headline='Something Again', content='Another text.')
post3 = Post.objects.create(author=user2, size=Post.news, headline='Again & again', content='Another text.')

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
post1.category.add(Category.objects.get(pk=cate4.pk))
post2.category.add(Category.objects.get(pk=cate4.pk))
post2.category.add(Category.objects.get(pk=cate2.pk))
post3.category.add(Category.objects.get(pk=cate3.pk))

# 6. Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).
comm1 = Comment.objects.create(post=post1, user=base1, content='Some comment')
comm2 = Comment.objects.create(post=post1, user=base2, content='Some comment')
comm3 = Comment.objects.create(post=post2, user=base2, content='Comment')
comm4 = Comment.objects.create(post=post3, user=base1, content='Comment again')
comm5 = Comment.objects.create(post=post3, user=base3, content='Comment forever')
comm6 = Comment.objects.create(post=post2, user=base3, content='Comment')

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post1.like()
post1.like()
post1.like()
post1.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.dislike()
post2.dislike()
post2.dislike()
post3.dislike()
post2.dislike()
post2.dislike()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
post3.dislike()
post3.dislike()
post3.dislike()
post3.like()
post3.like()
post3.dislike()

comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm2.like()
comm2.like()
comm2.like()
comm2.like()
comm2.like()
comm2.dislike()
comm2.dislike()
comm2.dislike()
comm3.dislike()
comm3.like()
comm3.like()
comm3.like()
comm3.dislike()
comm3.dislike()
comm3.like()
comm3.like()
comm4.like()
comm4.like()
comm4.like()
comm4.like()
comm4.like()
comm4.dislike()
comm4.dislike()
comm5.dislike()
comm5.dislike()
comm5.like()
comm5.like()
comm5.like()
comm5.dislike()
comm5.dislike()
comm5.like()
comm5.like()
comm5.like()
comm5.like()
comm5.like()
comm6.dislike()
comm6.like()
comm6.like()
comm6.like()
comm6.dislike()
comm6.dislike()
comm6.like()
comm6.like()

# 8. Обновить рейтинги пользователей.
user1.update_rating()
user2.update_rating()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.order_by('-rating').values('user__username', 'rating').first()

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
post = Post.objects.order_by('-rating').first()
post_dict = Post.objects.order_by('-rating').values('pub_date', 'author__user__username', 'rating', 'headline').first()
post_dict.update({'preview': post.preview()})
post_dict

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
post.comment_set.all().values('pub_date', 'user__username', 'rating', 'content')
