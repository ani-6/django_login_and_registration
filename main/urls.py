from django.urls import path
from .views import *
#from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
     #Main App
     path('', home_view, name='home'),
     #Notifications
     path('notifications/', notifications_view, name='notifications'),
     #Image Gallery
     path('gallery/', image_gallery_view, name='gallery'),
     path('localgallery/', local_gallery_view, name='localgallery'),
     #Downloader
     path("urldownloader/", downlaodUrlToGdrive_view, name="urldownloader"),

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
