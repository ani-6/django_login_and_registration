from .models import *

def GetImportantLinks(user,active):
    objects = Home_ImportantLinks.objects.filter(user=user,is_active=active)
    return objects

def GetLatestUpdates(user):
    objects = Home_LatestUpdates.objects.filter(user=user).order_by('-created_at')[:4]
    return objects

def GetGalleryObjects(user):
    objects = Image_Gallery.objects.filter(user__exact=user)
    return objects

def GetAllDriveObjects(user):
    objects = UrlToGdrive.objects.filter(user=user)
    return objects

def IfDriveObjectExists(user,file,url):
    exists = UrlToGdrive.objects.filter(user=user,filename=file,original_path=url).exists()
    return exists

def getAnnouncements():
    objects = globalAnnouncement.objects.filter(is_active=True).order_by('-created_at')[:6]
    return objects