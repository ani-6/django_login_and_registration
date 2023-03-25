from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    GENDER =(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile_images/default.jpg', upload_to='profile_images',null=True,blank=True)
    gender = models.CharField(max_length=50, null=True,choices=GENDER)
    headline = models.CharField(max_length=80,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_pic.path)        
        img.save(self.profile_pic.path)


class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    note = RichTextUploadingField(blank=True, null=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class GalleryContent(models.Model):
    Quality=(
        ('HD','HD'),
        ('SD','SD'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=1024, null=False)
    thumb = models.CharField(max_length=1024, null=False)
    tags = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=5, null=True,choices=Quality)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class HomeContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1024, null=False)
    link = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.heading
        
class HomeUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.update

class UrlDownloaderGdrive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null=False)
    local_path = models.CharField(max_length=255, null=False)
    fileid = models.CharField(max_length=255, null=False)
    folderid = models.CharField(max_length=255, null=False)
    shared = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)