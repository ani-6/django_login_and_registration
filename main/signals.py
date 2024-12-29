from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import globalAnnouncement

from .models import LatestUpdates

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        LatestUpdates.objects.create(user=instance,update='Welcome to the Hub!')

@receiver([post_save, post_delete], sender=globalAnnouncement)
def invalidate_announcement_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for active announcements when an announcement is
    created, updated, or deleted.
    """
    cache_key = 'active_announcements'
    cache.delete(cache_key)