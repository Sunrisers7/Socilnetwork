from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='list'),
    path('create/', views.GroupCreateView.as_view(), name='create'),
    path('<int:pk>/', views.GroupDetailView.as_view(), name='detail'),
    path('<int:pk>/join/', views.join_group, name='join'),
    path('<int:pk>/leave/', views.leave_group, name='leave'),
]