from django.conf import settings
from django.core.cache import cache

from .models import globalAnnouncement

def announcement_context_processor(request):
    """
    Adds the active announcements to the context with caching.
    """
    # Define a cache key for the announcements
    cache_key = 'active_announcements'

    # Try to get cached announcements
    announcements = cache.get(cache_key)

    if announcements is None:
        # If not cached, perform the query and cache the result for 1 minute
        announcements = globalAnnouncement.objects.filter(is_active=True) \
            .order_by('-created_at')[:4] \
            .only('id', 'title', 'description')

        # Cache the result for 5 minute (300 seconds)
        cache.set(cache_key, announcements, timeout=300)

    return {
        'announcements': announcements
    }

def settings_variable_processor(request):
    return {
        'HOMEURL': settings.LOGIN_REDIRECT_URL,
    }

def user_group_processor(request):
    # Cache key based on the user ID to avoid repeated database queries
    cache_key = f"user_group_{request.user.id}" if request.user.is_authenticated else None
    
    if request.user.is_authenticated:
        # Check cache first to avoid DB hit on every request
        is_in_group = cache.get(cache_key)
        
        if is_in_group is None:
            # If not cached, perform the DB lookup and store the result in cache
            is_in_group = request.user.groups.filter(name='PlusUsers').exists()
            cache.set(cache_key, is_in_group, timeout=300)  # Cache for 5 minutes (optional)
    else:
        is_in_group = False

    return {'user_in_group': is_in_group}

def user_thumbnail_url(request):
    """
    Retrieves the user's thumbnail URL from the cache or fetches it from the database.
    The cache key is based on the user's ID to ensure that each user has a separate cache.
    """
    if request.user.is_authenticated:
        user = request.user
        cache_key = f'user_{user.id}_thumbnail_url'

        # Try fetching from cache
        thumbnail_url = cache.get(cache_key)

        if thumbnail_url is None:
            # Cache miss, fetch from database and store in cache
            thumbnail_url = user.user_profile.thumbnail_url
            cache.set(cache_key, thumbnail_url, timeout=60 * 5)  # Cache for 5 minutes

        return {'user_thumbnail_url': thumbnail_url}

    return {}