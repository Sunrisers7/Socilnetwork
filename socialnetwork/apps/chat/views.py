from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from .models import ChatRoom, Message, ChatCustomization
from .forms import ChatThemeForm


class ChatListView(LoginRequiredMixin, ListView):
    template_name = 'chat/list.html'
    context_object_name = 'chat_rooms'

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user).order_by('-updated_at')


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat/room.html'
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages_list'] = self.object.messages.all().order_by('created_at')

        # Отримуємо кастомізацію для поточного користувача
        customization, created = ChatCustomization.objects.get_or_create(
            user=self.request.user,
            room=self.object,
            defaults={'custom_theme': self.object.theme}
        )
        context['customization'] = customization
        return context


class ChatSettingsView(LoginRequiredMixin, UpdateView):
    """Налаштування чату"""
    model = ChatRoom
    form_class = ChatThemeForm
    template_name = 'chat/settings.html'
    success_url = reverse_lazy('chat:list')

    def get_object(self, queryset=None):
        room = get_object_or_404(ChatRoom, pk=self.kwargs['pk'])
        # Тільки учасники можуть змінювати налаштування
        if self.request.user not in room.participants.all():
            raise PermissionError("Ви не учасник цього чату")
        return room

    def form_valid(self, form):
        room = form.save()
        messages.success(self.request, f'Налаштування чату оновлено!')
        return redirect('chat:room', pk=room.pk)


class UserChatSettingsView(LoginRequiredMixin, UpdateView):
    """Персональні налаштування чату для користувача"""
    model = ChatCustomization
    template_name = 'chat/user_settings.html'
    fields = ['custom_theme', 'custom_image']

    def get_object(self, queryset=None):
        room = get_object_or_404(ChatRoom, pk=self.kwargs['pk'])
        customization, created = ChatCustomization.objects.get_or_create(
            user=self.request.user,
            room=room,
            defaults={'custom_theme': room.theme}
        )
        return customization

    def get_success_url(self):
        return reverse_lazy('chat:room', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'Ваші налаштування збережено!')
        return super().form_valid(form)


def send_message(request, pk):
    """Відправка повідомлення з текстом або фото"""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, pk=pk)
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if content or image:
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content if content else '',
                file=image
            )

    return redirect('chat:room', pk=pk)


def start_chat(request, user_id):
    """Почати чат з користувачем"""
    other_user = get_object_or_404(User, id=user_id)

    room = ChatRoom.objects.filter(
        room_type='private',
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not room:
        room = ChatRoom.objects.create(
            room_type='private',
            created_by=request.user
        )
        room.participants.add(request.user, other_user)

    return redirect('chat:room', pk=room.pk)