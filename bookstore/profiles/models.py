from django.db import models

from bookstore.accounts.models import BookstoreUser
import cloudinary.models as cloudinary_models

from bookstore.profiles.misc import list_of_countries
from bookstore.profiles.validators import validate_city, validate_phone_number


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')

    country = models.CharField(choices=[(country, country) for country in list_of_countries], blank=True, max_length=44)
    city = models.CharField(max_length=200, validators=[validate_city], blank=True)
    street_address = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(validators=[validate_phone_number], max_length=30, blank=True)

    is_complete = models.BooleanField(default=False)
    user = models.OneToOneField(BookstoreUser, on_delete=models.CASCADE, primary_key=True, blank=True)
