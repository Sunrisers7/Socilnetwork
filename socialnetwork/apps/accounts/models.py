from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    THEMES = [
        ('default', 'Стандартна (синя)'),
        ('sunset', 'Захід сонця'),
        ('ocean', 'Океан'),
        ('forest', 'Ліс'),
        ('night', 'Нічне небо'),
        ('purple_haze', 'Фіолетовий туман'),
        ('fire', 'Вогонь'),
        ('neon', 'Неон'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True, null=True)
    cover_image = models.ImageField(upload_to='profile_pics/covers/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    theme = models.CharField(max_length=20, choices=THEMES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/media/default.png'

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    def get_theme_gradient(self):
        """Повертає CSS градієнт для теми"""
        themes = {
            'default': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'sunset': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'ocean': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'forest': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'night': 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
            'purple_haze': 'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
            'fire': 'linear-gradient(135deg, #f12711 0%, #f5af19 100%)',
            'neon': 'linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%)',
        }
        return themes.get(self.theme, themes['default'])

    def get_theme_class(self):
        """Повертає CSS клас для теми"""
        return f'theme-{self.theme}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()