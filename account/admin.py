from django.contrib import admin
from .models import *
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Pictures', {
        'classes': ('wide',),
        'fields': ('profile_pic', 'cover_pic'),
        }),
        ('Other Details', {
        'classes': ('wide',),
        'fields': ('gender','headline','bio'),
        }),
        ('Remote Storage Details', {
        'classes': ('wide',),
        'fields': ['remote_fol_id'],
        }),
        )
    list_display = ["user","gender"]

admin.site.register(Profile,ProfileAdmin)