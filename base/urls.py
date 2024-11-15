"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

admin.site.site_header = "Hub Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    #Registered apps
    path('', include('main.urls', namespace='main')),
    path('account/', include('account.urls', namespace='account')),
    #Social Login
    re_path(r'^auth/', include('social_django.urls', namespace='social')),
    #maintenance mode
    re_path(r"^maintenance-mode/", include("maintenance_mode.urls")),
]
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error pages
handler404 = 'main.views.custom_404_view'
handler500 = 'main.views.custom_500_view'
handler503 = 'main.views.custom_503_view'
handler403 = 'main.views.custom_403_view'
handler400 = 'main.views.custom_400_view'