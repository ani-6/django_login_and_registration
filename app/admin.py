from django.contrib import admin
# Register your models here.
from .models import *

class GalleryContentAdmin(admin.ModelAdmin):
    list_display = ("user","tags")

class HomeContentAdmin(admin.ModelAdmin):
    list_display = ("user","heading")

class NotebookAdmin(admin.ModelAdmin):
    list_display = ("user","title")   

class HomeUpdatesAdmin(admin.ModelAdmin):
    list_display = ("user","update")

    
admin.site.register(Profile)
admin.site.register(UrlDownloaderGdrive)
admin.site.register(Notebook,NotebookAdmin)
admin.site.register(HomeContent,HomeContentAdmin)
admin.site.register(HomeUpdates,HomeUpdatesAdmin)
admin.site.register(GalleryContent, GalleryContentAdmin)