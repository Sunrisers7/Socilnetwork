from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='list'),
    path('<int:pk>/', views.ChatRoomView.as_view(), name='room'),
    path('<int:pk>/send/', views.send_message, name='send_message'),
    path('<int:pk>/settings/', views.ChatSettingsView.as_view(), name='settings'),
    path('<int:pk>/my-settings/', views.UserChatSettingsView.as_view(), name='user_settings'),
    path('start/<int:user_id>/', views.start_chat, name='start'),
]