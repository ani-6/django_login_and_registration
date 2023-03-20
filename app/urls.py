from django.urls import path, include, re_path
from .views import home, RegisterView
from . import views
from django.contrib.auth import views as auth_views
from app.views import CustomLoginView, ResetPasswordView, ChangePasswordView
from app.forms import LoginForm

urlpatterns = [
     ##Account
     path('', home, name='users-home'),
     path('register/', RegisterView.as_view(), name='users-register'),
     path('settings/', views.Settings, name='users-settings'),
     path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                             authentication_form=LoginForm), name='login'),
     path('logout/', views.logoutUser, name='logout'),
     path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
          name='password_reset_complete'),
     path('password-change/', ChangePasswordView.as_view(), name='password_change'),
     path('profile/', views.ProfileView, name='profile'),
     path('da/', views.DeleteAvtar, name='da'),
     re_path(r'^oauth/', include('social_django.urls', namespace='social')),


     #Notebook
     path('notebook/', views.NotebookView, name='notebook'),
     
     #Gallery
     path('maingallery/', views.MainGallery, name='maingallery'),
     path('extgallery/', views.Gallery, name='extgallery'),

     #Markdown
     path('markdown/', views.MarkdownView, name='markdown'),

     #Downloader
     path("urldownloader/", views.Downloadfile, name="urldownloader"),
     
]
