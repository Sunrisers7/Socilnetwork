from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Like, Comment
from .forms import PostForm
from apps.notifications.utils import create_notification


class PostListView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Пост створено!')
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:feed')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('posts:feed')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        else:
            create_notification(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                message=f'{request.user.username} лайкнув ваш пост',
                link=f'/posts/{post.pk}/'
            )
    return redirect('posts:feed')


def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content', '')
        if content.strip():
            Comment.objects.create(user=request.user, post=post, content=content)
            create_notification(
                recipient=post.author,
                sender=request.user,
                notification_type='comment',
                message=f'{request.user.username} прокоментував ваш пост: {content[:50]}',
                link=f'/posts/{post.pk}/'
            )
            messages.success(request, 'Коментар додано!')
    return redirect('posts:detail', pk=pk)