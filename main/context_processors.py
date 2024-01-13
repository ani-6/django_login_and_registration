from .models import globalAnnouncement


def announcement_context_processor(request):
    """
    Adds the active announcements to the context
    """
    return {
        'announcements': globalAnnouncement.objects.filter(is_active=True).order_by('-created_at')[:4]
    }