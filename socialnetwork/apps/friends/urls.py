from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.FriendsListView.as_view(), name='list'),
    path('requests/', views.FriendRequestsView.as_view(), name='requests'),
    path('send/<int:user_id>/', views.send_friend_request, name='send_request'),
    path('accept/<int:friendship_id>/', views.accept_friend_request, name='accept'),
    path('reject/<int:friendship_id>/', views.reject_friend_request, name='reject'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove'),
]