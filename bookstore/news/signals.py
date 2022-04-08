import cloudinary.uploader
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from bookstore.news.models import Article


@receiver(pre_save, sender=Article)
def delete_old_image_on_article_change(sender, instance, **kwargs):
    try:
        old_image = sender.objects.get(pk=instance.pk).image
        if old_image:
            new_image = instance.image
            if not old_image == new_image:
                cloudinary.uploader.destroy(old_image.public_id)
    except instance.DoesNotExist:
        return


@receiver(pre_delete, sender=Article)
def delete_image_on_article_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
