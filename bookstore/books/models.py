from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
import cloudinary.models as cloudinary_models
from django.utils.safestring import mark_safe

from bookstore.books.misc import list_of_genres
from bookstore.books.validators import validate_genre, validate_title

UserModel = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=200, validators=[validate_title])
    description = models.TextField(blank=True)
    genre = models.CharField(choices=[(genre, genre) for genre in list_of_genres], max_length=35,
                             validators=[validate_genre])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = 'Current Image'

    def __str__(self):
        return self.title


class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class Dislike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class BookReview(models.Model):
    text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
