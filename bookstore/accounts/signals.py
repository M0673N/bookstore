import cloudinary.uploader
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from bookstore.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


@receiver(pre_delete, sender=Profile)
def image_delete_on_profile_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)


@receiver(pre_save, sender=Profile)
def delete_old_image_on_change(sender, instance, **kwargs):
    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        cloudinary.uploader.destroy(old_image.public_id)


@receiver(pre_save, sender=Profile)
def check_is_complete(sender, instance, **kwargs):
    if all([instance.first_name, instance.last_name, instance.country, instance.city, instance.street_address,
            instance.phone, instance.post_code]):
        instance.is_complete = True
