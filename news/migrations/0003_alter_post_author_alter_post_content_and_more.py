# Generated by Django 5.0.2 on 2024-04-05 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='headline',
            field=models.CharField(max_length=60, verbose_name='Headline'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Pud Date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='post',
            name='size',
            field=models.CharField(choices=[('AR', 'Article'), ('NE', 'News')], default='NE', help_text='Post size', max_length=2, verbose_name='Size'),
        ),
    ]
