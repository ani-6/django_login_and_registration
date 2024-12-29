from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from . import views
from .apis import *
from .forms import *
from .views import *

app_name = 'account'

urlpatterns = [
     #Account
     path('login/', customLoginView.as_view(), name='login'),
     path('logout/', views.logoutUser_view, name='logout'),
     path('register/', registerView.as_view(), name='users-register'),
     path('profile/', views.profile_view, name='profile'),
     path('settings/', views.settings_view, name='users-settings'),
     path('password-change/', ChangePasswordView.as_view(), name='password_change'),
     path('password-reset/', resetPassword.as_view(), name='password_reset'),
     path('da/', views.deleteAvtar_view, name='da'),
     path('chats/', views.chats_view, name='chats'),
     path('chat/<int:id>/', views.chat_view, name='chat'),
     path('feedback/', views.feedback_view, name='feedback'),

     re_path(r'^oauth/', include('social_django.urls', namespace='social')),

     #apis
     path('apis/v1/login', accountLogin.as_view()),
     path('apis/v1/profile', accountProfile.as_view()),
     path('apis/v1/delete-avtar',accountDeleteAvtar.as_view()),
     path('apis/v1/logout', accountLogout.as_view()),
     path('apis/v1/feedback', accountFeedback.as_view()),
     path('apis/v1/settings', accountSettings.as_view()),
     path('apis/v1/change-password', accountChangePassword.as_view()),
     path('apis/v1/check-auth', CheckAuthView.as_view()),

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
