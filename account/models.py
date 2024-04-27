import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    GENDER =(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    profile_pic = models.ImageField(default='Account/profile_images/default.jpg', upload_to='Account/profile_images',null=True,blank=True,verbose_name="Profile Picture")
    cover_pic = models.ImageField(default='Account/cover_images/_default.jpg', upload_to='Account/cover_images',null=True,blank=True,verbose_name="Cover Picture")
    gender = models.CharField(max_length=50, null=True,choices=GENDER)
    headline = models.CharField(max_length=80,null=True, blank=True)
    bio = models.TextField(null=True, blank=True,verbose_name='About me')
    remote_fol_id = models.CharField(max_length=255,null=True, blank=True,verbose_name="Remote Folder ID")

    def __str__(self):
        return self.user.username

    def thumbnail_url(self):
        # Check if the profile picture is set and is not default.png
        if self.profile_pic and os.path.basename(self.profile_pic.name) != 'default.jpg':
            # Generate the thumbnail path
            thumbnail_path = '/media/Account/profile_images/thumbnail_' + os.path.basename(self.profile_pic.name)
            return thumbnail_path
        else:
            # Return the original profile picture URL
            return self.profile_pic.url

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Receiver")
    message = models.TextField(null=True, blank=True,verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.sender.username
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages List"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="User")
    email = email = models.EmailField(max_length=254)
    comment = models.TextField(null=True, blank=True,verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback List"