from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chats', views.user_list, name='user_list'),
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
]
