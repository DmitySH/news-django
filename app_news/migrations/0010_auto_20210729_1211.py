# Generated by Django 3.2.5 on 2021-07-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0009_auto_20210729_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='news',
        ),
        migrations.AddField(
            model_name='tag',
            name='news',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='app_news.News'),
        ),
    ]
