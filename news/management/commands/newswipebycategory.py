from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all articles in the selected category.'

    # custom missing_args message error
    missing_args_message = 'Not enough arguments'
    # Если true, то будет напоминать о необходимости сделать миграции (если таковые есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you want to delete all articles in the "{options["category"]}" category? [yes/no]\n')

        # в случае неправильного подтверждения отменяем команду
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Command canceled'))
            return None
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
