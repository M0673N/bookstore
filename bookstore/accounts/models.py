from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

import cloudinary.models as cloudinary_models

from .misc import list_of_countries
from .validators import validate_phone_number, validate_city


class BookstoreUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class BookstoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = BookstoreUserManager()


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')
    is_author = models.BooleanField(default=False)

    country = models.CharField(choices=[(country, country) for country in list_of_countries], blank=True, max_length=44)
    city = models.CharField(max_length=200, validators=[validate_city], blank=True)
    street_address = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(validators=[validate_phone_number], max_length=30, blank=True)

    is_complete = models.BooleanField(default=False)
    user = models.OneToOneField(BookstoreUser, on_delete=models.CASCADE, primary_key=True, blank=True)


from .signals import *
