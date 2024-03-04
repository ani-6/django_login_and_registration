from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

# Create your models here.
class Home_ImportantLinks(models.Model):
    user = models.ManyToManyField(User)
    heading = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1024, null=False)
    link = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.heading
    
    class Meta:
        verbose_name = "link"
        verbose_name_plural = "Important links"

class Home_LatestUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.update

    class Meta:
        verbose_name = "update"
        verbose_name_plural = "User specific updates"

class Image_Gallery(models.Model):
    user = models.ManyToManyField(User)
    image = models.CharField(max_length=1024, null=False)
    thumb = models.CharField(max_length=1024, null=False)
    caption = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image
    
    def img_preview(self):
        return mark_safe(f'<img loading=lazy src = "{self.thumb}" width="70px" />')
    
    class Meta:
        verbose_name = "image"
        verbose_name_plural = "Image gallery"
    
class UrlToGdrive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null=False)
    original_path = models.CharField(max_length=255, null=False)
    fileid = models.CharField(max_length=255, null=False)
    folderid = models.CharField(max_length=255, null=False)
    shared = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "Cloud files"

class globalAnnouncement(models.Model):
    title = models.CharField(max_length=255, null=False)
    body = models.TextField(blank=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Global notifications"
