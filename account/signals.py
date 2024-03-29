from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from base.Gdrive.gdriveOps import *
from dotenv import load_dotenv
load_dotenv()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.remote_fol_id:
            foldername = instance.user.username
            parentID = str(os.getenv('DriveFolderId'))
            instance.remote_fol_id = CreateFolder(foldername,parentID)
            instance.save()
 