from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Что у вас нового?'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': 'Текст',
            'image': 'Фото',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Написать комментарий...'
            }),
        }
        labels = {'content': ''}