from modeltranslation.translator import register, TranslationOptions
from news.models import Category, Post


@register(Category)  # декоратор-регистратор
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # поля, которое надо перевести


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('headline', 'content',)
