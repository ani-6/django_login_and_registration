from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *
# Register your models here.
@admin.register(LogEntry)
class customLogEntry_admin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_flag',)
    search_fields = ('user__username','object_repr','change_message')

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
    list_display = ['user','gender']

@admin.register(Messages)
class messages_admin(admin.ModelAdmin):
    fieldsets = (
        ('Users', {
        'fields': ['sender','receiver']
        }),
        ('Chat', {
        'classes': ('wide',),
        'fields': ('message','created_at','last_updated_at'),
        }),
    )
    search_fields = ('user__username', 'message')
    list_display = ['sender','receiver','message','created_at']
    readonly_fields = ['sender','receiver','message','created_at','last_updated_at']

@admin.register(Feedback)
class feedback_admin(admin.ModelAdmin):
    fieldsets = (
        ('User Details', {
        'fields': ['user','email']
        }),
        ('Feedback', {
        'classes': ('wide',),
        'fields': ('comment','created_at','last_updated_at'),
        }),
    )
    search_fields = ('user__username','change_message')
    list_display = ['user','comment','created_at']
    readonly_fields = ['user','email','comment','created_at','last_updated_at']