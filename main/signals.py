from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LatestUpdates

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        LatestUpdates.objects.create(user=instance,update='Welcome to the Hub!')