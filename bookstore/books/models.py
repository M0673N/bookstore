from django.db import models
import cloudinary.models as cloudinary_models

from bookstore.accounts.models import BookstoreUser
from bookstore.books.misc import list_of_genres


class Book(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    genre = models.CharField(choices=[(genre, genre) for genre in list_of_genres], blank=True, max_length=35)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')
    author = models.OneToOneField(BookstoreUser, on_delete=models.CASCADE, primary_key=True, blank=True)
