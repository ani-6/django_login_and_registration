# myapp/context_processors.py
from django.core.cache import cache
from django.conf import settings

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
