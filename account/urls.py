from django.urls import path, include, re_path
from .views import *
from . import views
from .forms import login_form
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
#from .apis import *

app_name = 'account'

urlpatterns = [
     #Account
     path('login/', customLogin.as_view(redirect_authenticated_user=True, template_name='account/login_cover.html',
                                             authentication_form=login_form), name='login'),
     path('logout/', views.logoutUser_view, name='logout'),
     path('register/', registerView.as_view(), name='users-register'),
     path('profile/', views.profile_view, name='profile'),
     path('settings/', views.settings_view, name='users-settings'),
     path('password-change/', ChangePasswordView.as_view(), name='password_change'),
     path('password-reset/', resetPassword.as_view(), name='password_reset'),
     path('da/', views.deleteAvtar_view, name='da'),
     path('chats/', views.chats_view, name='chats'),
     path('chat/<int:id>/', views.chat_view, name='chat'),

     re_path(r'^oauth/', include('social_django.urls', namespace='social')),

     #apis
     #path('api/v1/login', LoginView.as_view()),
     #path('api/v1/profile', ProfileAPI.as_view()),

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
