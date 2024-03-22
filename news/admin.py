from django.contrib import admin
from .models import *


# удобный вывод и фильтры для админки [D14.5]
class PostAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'headline', 'author')  # список со всеми полями, которые будут в таблице
    list_filter = ('author',)  # простой фильтр для админки
    search_fields = ('pub_date', 'category__name')  # поиск по дате и категории


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
