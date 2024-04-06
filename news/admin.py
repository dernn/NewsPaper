from django.contrib import admin
from modeltranslation.admin import TranslationAdmin  # импортируем модель-перевод амдинки

from .models import *


# удобный вывод и фильтры для админки [D14.5]
class PostAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'headline', 'author')  # список со всеми полями, которые будут в таблице
    list_filter = ('author',)  # простой фильтр для админки
    search_fields = ('pub_date', 'category__name')  # поиск по дате и категории
    model = Post  # same as below


# Регистрируем модели для перевода в админке [D17.4]
class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
