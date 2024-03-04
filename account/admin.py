from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Profile)
class profile_admin(admin.ModelAdmin):
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