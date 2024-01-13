from django.contrib import admin
from .models import *

# Register your models here.
class Home_ImportantLinks_Admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Link Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['heading','description','link','is_active'],
        }),
        )
    list_display = ('heading',)
    list_filter = ['user']

class Home_LatestUpdates_Admin(admin.ModelAdmin):
    list_display = ('user','update')
    list_filter = ['user']

class Image_Gallery_Admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Image Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['image','thumb','caption'],
        }),
        )
    readonly_fields = ['img_preview']
    list_display = ('img_preview','caption','created_at')
    list_filter = ['user']

class UrlToGdrive_Admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('File Details', {
        'classes': ('wide','collapse', 'expanded'),
        'fields': ['filename','original_path','fileid','folderid','shared'],
        }),
        )
    
    list_display = ('user','filename','created_at')
    list_filter = ['user']

class globalAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at')

admin.site.register(Home_ImportantLinks,Home_ImportantLinks_Admin)
admin.site.register(Home_LatestUpdates,Home_LatestUpdates_Admin)
admin.site.register(Image_Gallery,Image_Gallery_Admin)
admin.site.register(UrlToGdrive,UrlToGdrive_Admin)
admin.site.register(globalAnnouncement,globalAnnouncementAdmin)