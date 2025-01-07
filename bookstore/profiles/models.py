from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe

from bookstore.accounts.models import BookstoreUser
import cloudinary.models as cloudinary_models

from bookstore.profiles.misc import list_of_countries
from bookstore.profiles.validators import (
    validate_city,
    validate_phone_number,
    validate_name,
)

UserModel = get_user_model()


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type="image")

    country = models.CharField(
        choices=[(country, country) for country in list_of_countries],
        blank=True,
        max_length=44,
    )
    city = models.CharField(max_length=200, blank=True)
    street_address = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(
        validators=[validate_phone_number], max_length=30, blank=True
    )
    is_author = models.BooleanField(default=False)

    is_complete = models.BooleanField(default=False)
    user = models.OneToOneField(
        BookstoreUser, on_delete=models.CASCADE, primary_key=True, blank=True
    )

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = "Current Image"

    def __str__(self):
        return self.first_name + " " + self.last_name


class AuthorLike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class AuthorDislike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class AuthorReview(models.Model):
    text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
