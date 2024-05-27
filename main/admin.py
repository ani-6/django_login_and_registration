from django.contrib import admin
from .models import *

# Register your models here.

# Important links admin 
@admin.register(ImportantLinks)
class ImportantLinks_admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Link Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['heading','description','link','is_active'],
        }),
        )
    list_display = ('heading','last_updated_at')
    list_filter = ['user']

# Latest updates admin
@admin.register(LatestUpdates)
class LatestUpdates_admin(admin.ModelAdmin):
    list_display = ('user','update')
    list_filter = ['user']

# Image gallery admin
@admin.register(Image_Gallery)
class imageGallery_admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Image Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['image','thumbnail','caption'],
        }),
        )
    search_fields = ('image', 'caption')
    readonly_fields = ('img_preview',)
    list_display = ('img_preview','caption','created_at')
    list_filter = ['user']

# UrlToGdrive admin
@admin.register(UrlToGdrive)
class urlToGdrive_admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('File Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['file_name','source_path','file_id','folder_id','is_shared'],
        }),
        )
    search_fields = ('file_name', 'source_path')
    list_display = ('user','file_name','created_at')
    list_filter = ['user']

# Global announcement admin
@admin.register(globalAnnouncement)
class globalAnnouncement_admin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at','last_updated_at')
    search_fields = ('title','description')
