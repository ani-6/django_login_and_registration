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

@admin.register(Messages)
class messages_admin(admin.ModelAdmin):
    fieldsets = (
        ('Select Users', {
        'fields': ['sender','receiver']
        }),
        ('Chat', {
        'classes': ('wide',),
        'fields': ('message',),
        }),
    )
    list_display = ["sender","receiver","message","created_at"]

@admin.register(Feedback)
class feedback_admin(admin.ModelAdmin):
    fieldsets = (
        ('User Details', {
        'fields': ['user','email']
        }),
        ('Feedback', {
        'classes': ('wide',),
        'fields': ('comment',),
        }),
    )
    list_display = ["user","comment","comment","created_at"]