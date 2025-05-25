from django.contrib import admin
from .models import Message
# Register your models here.

@admin.register(Message)
class Message_admin(admin.ModelAdmin):
    fieldsets = (
        ('Message Details', {
            'fields': ('sender', 'receiver', 'content', 'timestamp')
        }),
    )
    list_display = ("sender", "receiver", "content", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("timestamp","sender", "receiver")
    readonly_fields = ("timestamp",)
    