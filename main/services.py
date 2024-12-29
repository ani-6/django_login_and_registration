from .models import *
from django.core.cache import cache

def get_ImportantLinks(user,active):
    objects = ImportantLinks.objects.filter(user=user, is_active=active).only('heading', 'description', 'link')
    return objects

def get_LatestUpdates(user):
    # First, try fetching the data from the cache
    cache_key = f"latest_updates_{user.id}"
    cached_updates = cache.get(cache_key)

    if cached_updates is None:
        # Fetch the latest updates for the user
        cached_updates = LatestUpdates.objects.filter(user=user) \
            .only('id', 'created_at', 'update') \
            .order_by('-created_at')[:5]

        # Cache the result for 5 minutes (300 seconds)
        cache.set(cache_key, cached_updates, timeout=300)

    return cached_updates

def get_GalleryObjects(user):
    objects = Image_Gallery.objects.filter(user__exact=user)
    return objects

def get_AllDriveObjects(user):
    objects = UrlToGdrive.objects.filter(user=user)
    return objects

def IfDriveObjectExists(user,file,url):
    exists = UrlToGdrive.objects.filter(user=user, file_name=file, source_path=url).exists()
    return exists

def get_Announcements():
    """
    Returns active announcements with caching.
    """
    # Define a cache key for the active announcements
    cache_key = 'active_announcements'

    # Try to get the cached result
    objects = cache.get(cache_key)

    if objects is None:
        # If the result is not cached, query the database
        objects = globalAnnouncement.objects.filter(is_active=True) \
            .order_by('-created_at')[:6] \
            .only('id', 'title', 'description', 'created_at', 'last_updated_at')

        cache.set(cache_key, objects, timeout=300)  # Cache timeout in seconds (5 minutes)

    return objects