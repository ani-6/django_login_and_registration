from .models import *

def get_ImportantLinks(user,active):
    objects = ImportantLinks.objects.filter(user=user, is_active=active)
    return objects

def get_LatestUpdates(user):
    objects = LatestUpdates.objects.filter(user=user).order_by('-created_at')[:4]
    return objects

def get_GalleryObjects(user):
    objects = Image_Gallery.objects.filter(user__exact=user)
    return objects

def get_AllDriveObjects(user):
    objects = UrlToGdrive.objects.filter(user=user)
    return objects

def IfDriveObjectExists(user,file,url):
    exists = UrlToGdrive.objects.filter(user=user, file_name=file, source_path=url).exists()
    return exists

def get_Announcements():
    objects = globalAnnouncement.objects.filter(is_active=True).order_by('-created_at')[:6]
    return objects