from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class ImportantLinks(models.Model):
    user = models.ManyToManyField(User)
    heading = models.CharField(max_length=255, null=False, verbose_name='Heading')
    description = models.CharField(max_length=1024, null=False, verbose_name='Description')
    link = models.CharField(max_length=50, null=False,help_text="Enter the full internal url without '/' e.g. 'explore/'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.heading
    
    class Meta:
        verbose_name = "link"
        verbose_name_plural = "Important links"

class LatestUpdates(models.Model):
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
    thumbnail = models.CharField(max_length=1024, null=False)
    caption = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image
    
    def img_preview(self):
        return mark_safe(f'<img loading=lazy src = "{self.thumbnail}" width="70px" />')
    
    class Meta:
        verbose_name = "image"
        verbose_name_plural = "Image gallery"
    
class UrlToGdrive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, null=False, verbose_name='File name')
    source_path = models.CharField(max_length=255, null=False,verbose_name='Source path')
    file_id = models.CharField(max_length=255, null=False)
    folder_id = models.CharField(max_length=255, null=False, verbose_name='Drive folder Id')
    is_shared = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "Cloud files"

class globalAnnouncement(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Global notifications"
