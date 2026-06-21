from django import forms
from .models import ChatRoom, ChatCustomization


class ChatThemeForm(forms.ModelForm):
    """Форма для зміни теми чату (для всіх учасників)"""
    class Meta:
        model = ChatRoom
        fields = ['theme', 'chat_image']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'chat_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserChatCustomizationForm(forms.ModelForm):
    """Персональна кастомізація чату"""
    class Meta:
        model = ChatCustomization
        fields = ['custom_theme', 'custom_image']
        widgets = {
            'custom_theme': forms.Select(attrs={'class': 'form-control'}),
            'custom_image': forms.FileInput(attrs={'class': 'form-control'}),
        }