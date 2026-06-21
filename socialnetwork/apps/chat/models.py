from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('private', 'Приватний'),
        ('group', 'Груповий'),
    ]

    THEMES = [
        ('default', 'Стандартна'),
        ('dark', 'Темна'),
        ('blue', 'Синя'),
        ('green', 'Зелена'),
        ('pink', 'Рожева'),
        ('purple', 'Фіолетова'),
    ]

    name = models.CharField(max_length=100, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='private')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chat_rooms')
    theme = models.CharField(max_length=20, choices=THEMES, default='default')
    chat_image = models.ImageField(upload_to='chat_backgrounds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.room_type == 'private':
            others = self.participants.exclude(id=self.created_by.id)
            if others.exists():
                return f"Чат з {others.first().username}"
            return f"Чат {self.id}"
        return self.name or f"Груповий чат {self.id}"

    def get_theme_colors(self):
        """Повертає кольори теми"""
        themes = {
            'default': {'bg': '#ffffff', 'bubble_sent': '#0d6efd', 'bubble_recv': '#f1f1f1', 'text_sent': '#ffffff',
                        'text_recv': '#000000'},
            'dark': {'bg': '#1a1a1a', 'bubble_sent': '#333333', 'bubble_recv': '#2a2a2a', 'text_sent': '#ffffff',
                     'text_recv': '#cccccc'},
            'blue': {'bg': '#e3f2fd', 'bubble_sent': '#1976d2', 'bubble_recv': '#bbdefb', 'text_sent': '#ffffff',
                     'text_recv': '#000000'},
            'green': {'bg': '#e8f5e9', 'bubble_sent': '#388e3c', 'bubble_recv': '#c8e6c9', 'text_sent': '#ffffff',
                      'text_recv': '#000000'},
            'pink': {'bg': '#fce4ec', 'bubble_sent': '#e91e63', 'bubble_recv': '#f8bbd0', 'text_sent': '#ffffff',
                     'text_recv': '#000000'},
            'purple': {'bg': '#f3e5f5', 'bubble_sent': '#9c27b0', 'bubble_recv': '#e1bee7', 'text_sent': '#ffffff',
                       'text_recv': '#000000'},
        }
        return themes.get(self.theme, themes['default'])


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


class ChatCustomization(models.Model):
    """Кастомізація чату для кожного користувача"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_customizations')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='customizations')
    custom_theme = models.CharField(max_length=20, choices=ChatRoom.THEMES, blank=True, null=True)
    custom_image = models.ImageField(upload_to='chat_backgrounds/', blank=True, null=True)

    class Meta:
        unique_together = ['user', 'room']

    def __str__(self):
        return f"{self.user.username} customization for {self.room}"