# Generated by Django 4.0.3 on 2022-04-08 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_articlereview_articlecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlelike',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlelike',
            name='user',
        ),
        migrations.DeleteModel(
            name='ArticleDislike',
        ),
        migrations.DeleteModel(
            name='ArticleLike',
        ),
    ]
