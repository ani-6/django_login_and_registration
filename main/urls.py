from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .apis import *
from .views import *

app_name = 'main'

urlpatterns = [
     path('secure_media/<path:path>/', serve_main_media_view, name='serve_media'),
     #Main App
     path('', home_view, name='home'),
     #Notifications
     path('notifications/', notifications_view, name='notifications'),
     #Image Gallery
     path('gallery/', imageGallery_view, name='gallery'),
     path('localgallery/', localGallery_view, name='localgallery'),
     #Downloader
     path("urldownloader/", downlaodUrlToGdrive_view, name="urldownloader"),
     path("get-file-size", get_file_size, name="get_file_size"),

     #Apis
     path('apis/v1/home', mainHome.as_view()),
     path('apis/v1/gallery', mainImageGallery.as_view()),
     path('apis/v1/announcement', mainGlobalAnnouncement.as_view()),
]


urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
