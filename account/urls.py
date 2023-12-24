from django.urls import path, include, re_path
from .views import *
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
#from .apis import *

app_name = 'account'

urlpatterns = [
     #Account
     path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='account/login_cover.html',
                                             authentication_form=LoginForm), name='login'),
     path('logout/', views.logoutUser, name='logout'),
     path('register/', RegisterView.as_view(), name='users-register'),
     path('profile/', views.ProfileView, name='profile'),
     path('settings/', views.SettingsView, name='users-settings'),
     path('password-change/', ChangePasswordView.as_view(), name='password_change'),
     path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
     path('da/', views.DeleteAvtar, name='da'),
     re_path(r'^oauth/', include('social_django.urls', namespace='social')),

     #apis
     #path('api/v1/login', LoginView.as_view()),
     #path('api/v1/profile', ProfileAPI.as_view()),

] 
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
