from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Friendship
from apps.notifications.utils import create_notification


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            Q(friendships_sent__to_user=user, friendships_sent__status='accepted') |
            Q(friendships_received__from_user=user, friendships_received__status='accepted')
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['pending_requests'] = Friendship.objects.filter(to_user=user, status='pending')
        context['all_users'] = User.objects.exclude(id=user.id).exclude(
            id__in=self.get_queryset().values_list('id', flat=True)
        )[:20]
        return context


class FriendRequestsView(LoginRequiredMixin, ListView):
    template_name = 'friends/requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Friendship.objects.filter(to_user=self.request.user, status='pending')


def send_friend_request(request, user_id):
    if request.method == 'POST':
        to_user = get_object_or_404(User, id=user_id)
        friendship, created = Friendship.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
            defaults={'status': 'pending'}
        )
        if created:
            create_notification(
                recipient=to_user,
                sender=request.user,
                notification_type='friend_request',
                message=f'{request.user.username} хоче додати вас в друзі',
                link=f'/accounts/profile/{request.user.username}/'
            )
            messages.success(request, f'Запит відправлено {to_user.username}!')
        else:
            messages.info(request, 'Запит вже існує')
    return redirect('friends:list')


def accept_friend_request(request, friendship_id):
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user, status='pending')
        friendship.status = 'accepted'
        friendship.save()
        create_notification(
            recipient=friendship.from_user,
            sender=request.user,
            notification_type='friend_accept',
            message=f'{request.user.username} прийняв ваш запит в друзі',
            link=f'/accounts/profile/{request.user.username}/'
        )
        messages.success(request, f'{friendship.from_user.username} тепер ваш друг!')
    return redirect('friends:requests')


def reject_friend_request(request, friendship_id):
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
        friendship.status = 'rejected'
        friendship.save()
    return redirect('friends:requests')


def remove_friend(request, user_id):
    if request.method == 'POST':
        user = request.user
        friend = get_object_or_404(User, id=user_id)
        Friendship.objects.filter(
            Q(from_user=user, to_user=friend) | Q(from_user=friend, to_user=user),
            status='accepted'
        ).delete()
        messages.success(request, f'{friend.username} видалено з друзів')
    return redirect('friends:list')