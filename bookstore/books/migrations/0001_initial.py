# Generated by Django 4.0.3 on 2022-04-04 11:15

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("Action and adventure", "Action and adventure"),
                            ("Art / architecture", "Art / architecture"),
                            ("Alternate history", "Alternate history"),
                            ("Autobiography", "Autobiography"),
                            ("Anthology", "Anthology"),
                            ("Biography", "Biography"),
                            ("Business / economics", "Business / economics"),
                            ("Children's", "Children's"),
                            ("Crafts / hobbies", "Crafts / hobbies"),
                            ("Classic", "Classic"),
                            ("Cookbook", "Cookbook"),
                            ("Comic book", "Comic book"),
                            ("Diary", "Diary"),
                            ("Dictionary", "Dictionary"),
                            ("Crime", "Crime"),
                            ("Encyclopedia", "Encyclopedia"),
                            ("Drama", "Drama"),
                            ("Guide", "Guide"),
                            ("Fairytale", "Fairytale"),
                            ("Health / fitness", "Health / fitness"),
                            ("Fantasy", "Fantasy"),
                            ("History", "History"),
                            ("Graphic novel", "Graphic novel"),
                            ("Home and garden", "Home and garden"),
                            ("Historical fiction", "Historical fiction"),
                            ("Humor", "Humor"),
                            ("Horror", "Horror"),
                            ("Journal", "Journal"),
                            ("Mystery", "Mystery"),
                            ("Math", "Math"),
                            ("Paranormal romance", "Paranormal romance"),
                            ("Memoir", "Memoir"),
                            ("Picture book", "Picture book"),
                            ("Philosophy", "Philosophy"),
                            ("Poetry", "Poetry"),
                            ("Prayer", "Prayer"),
                            ("Political thriller", "Political thriller"),
                            (
                                "Religion, spirituality, and new age",
                                "Religion, spirituality, and new age",
                            ),
                            ("Romance", "Romance"),
                            ("Textbook", "Textbook"),
                            ("Satire", "Satire"),
                            ("True crime", "True crime"),
                            ("Science fiction", "Science fiction"),
                            ("Review", "Review"),
                            ("Short story", "Short story"),
                            ("Science", "Science"),
                            ("Suspense", "Suspense"),
                            ("Self help", "Self help"),
                            ("Thriller", "Thriller"),
                            ("Sports and leisure", "Sports and leisure"),
                            ("Western", "Western"),
                            ("Travel", "Travel"),
                        ],
                        max_length=35,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(blank=True, max_length=255),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
