from django.contrib.auth import get_user_model
from django.db import models
import cloudinary.models as cloudinary_models

UserModel = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')
    date_posted = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class ArticleComment(models.Model):
    text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
