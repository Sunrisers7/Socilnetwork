from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Group, GroupMembership, GroupPost
from .forms import GroupForm


class GroupListView(ListView):
    model = Group
    template_name = 'groups/list.html'
    context_object_name = 'groups'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/create.html'
    success_url = reverse_lazy('groups:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group = form.save()
        GroupMembership.objects.create(user=self.request.user, group=group, role='admin')
        messages.success(self.request, f'Група {group.name} створена!')
        return redirect(self.success_url)


class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/detail.html'
    context_object_name = 'group'


def join_group(request, pk):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=pk)
        membership, created = GroupMembership.objects.get_or_create(user=request.user, group=group)
        if created:
            messages.success(request, f'Ви приєдналися до {group.name}!')
        else:
            messages.info(request, 'Ви вже учасник цієї групи')
    return redirect('groups:detail', pk=pk)


def leave_group(request, pk):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=pk)
        GroupMembership.objects.filter(user=request.user, group=group).delete()
        messages.success(request, 'Ви покинули групу')
    return redirect('groups:list')