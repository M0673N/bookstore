# Generated by Django 4.0.3 on 2022-04-08 09:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0002_article_date_posted"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ArticleReview",
            new_name="ArticleComment",
        ),
    ]
