from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from .apis import *

app_name = 'main'

urlpatterns = [
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

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
