from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Group(models.Model):
    """Модель групи/спільноти"""
    name = models.CharField(max_length=100, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    avatar = models.ImageField(upload_to='group_avatars/', default='group_avatars/default.png', blank=True)
    cover_image = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False, verbose_name='Приватна група')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:detail', kwargs={'pk': self.pk})

    @property
    def members_count(self):
        return self.memberships.filter(is_banned=False).count()


class GroupMembership(models.Model):
    """Членство в групі"""
    ROLE_CHOICES = [
        ('admin', 'Адміністратор'),
        ('moderator', 'Модератор'),
        ('member', 'Учасник'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'group']
        verbose_name = 'Членство в групі'
        verbose_name_plural = 'Членства в групах'

    def __str__(self):
        return f"{self.user.username} в {self.group.name} як {self.role}"


class GroupPost(models.Model):
    """Пост в групі"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='group_post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост групи'
        verbose_name_plural = 'Пости груп'

    def __str__(self):
        return f"Пост в {self.group.name} від {self.author.username}"