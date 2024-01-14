from django.urls import path
from .views import *
#from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
     #Main App
     path('', Home_View, name='home'),
     #Notifications
     path('notifications/', notifications, name='notifications'),
     #Image Gallery
     path('gallery/', Image_Gallery_View, name='gallery'),
     path('localgallery/', Local_Gallery, name='localgallery'),
     #Downloader
     path("urldownloader/", DownlaodUrlToGdrive, name="urldownloader"),

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
