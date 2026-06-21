
from django import forms
from .models import Group, GroupPost


class GroupForm(forms.ModelForm):
    """Форма для створення та редагування групи"""
    class Meta:
        model = Group
        fields = ['name', 'description', 'avatar', 'cover_image', 'is_private']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class GroupPostForm(forms.ModelForm):
    """Форма для поста в групі"""
    class Meta:
        model = GroupPost
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
