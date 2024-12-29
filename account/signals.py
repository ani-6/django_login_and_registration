from base.Gdrive.gdriveOps import *
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()

@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.remote_folder_id:
            foldername = instance.user.username
            parentID = settings.GDRIVEFOLDERID
            instance.remote_folder_id = CreateFolder(foldername,parentID)
            instance.save()

@receiver([post_save, post_delete], sender=Profile)
def invalidate_user_thumbnail_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the user's thumbnail URL whenever the profile is updated or deleted.
    """
    cache_key = f'user_{instance.user.id}_thumbnail_url'
    cache.delete(cache_key)