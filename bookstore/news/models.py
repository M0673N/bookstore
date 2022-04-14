from django.contrib.auth import get_user_model
from django.db import models
import cloudinary.models as cloudinary_models
from django.utils.safestring import mark_safe

UserModel = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    image = cloudinary_models.CloudinaryField(blank=True, resource_type='image')
    date_posted = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = 'Current Image'

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
