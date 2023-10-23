from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from .filters import PostFilter
from .models import Post, Category, User, Author
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-rating']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_res = PostFilter(
            self.request.GET, queryset=queryset)
        return queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['num_of_posts'] = len(Post.objects.all())
        context['filter'] = self.filter_res
        context['post_type_choices'] = Post.post_type_choices
        context['categories'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = [
            category.name for category in self.request.user.subscriptions.all()]
        return context


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'news/post_edit.html'
    context_object_name = 'post'


class PostAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    form_class = PostForm
    template_name = 'news/post_add.html'
    context_object_name = 'post'

    def form_valid(self, form):
        response = super().form_valid(form)
        post = self.object
        users_for_mailing = set()
        for category in post.categories.all():
            for subscriber in category.subscribers.all():
                if subscriber.email:
                    users_for_mailing.add(subscriber)
        if users_for_mailing:
            for user in users_for_mailing:
                html_content = render_to_string(
                    'news/mailing_post_add.html', {'post': post, 'username': user.username})
                msg = EmailMultiAlternatives(
                    subject=post.title,
                    from_email='iliab02@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        return response


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post'
    success_url = '/news/'


@login_required
def become_author(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if group not in user.groups.all():
        user.groups.add(group)
    if not Author.objects.filter(user=user).exists():
        author = Author.objects.create(user=user)
        author.save()
    return redirect('/')


@login_required
def become_common(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if group in user.groups.all():
        user.groups.remove(group)
    author = Author.objects.filter(user=user)
    if author.exists():
        author[0].delete()
    return redirect('/')


@login_required
def subscribe_to(request):
    category = Category.objects.get(name=request.GET['category'])
    user = request.user
    if category not in user.subscriptions.all():
        user.subscriptions.add(category)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_to(request):
    category = Category.objects.get(name=request.GET['category'])
    user = request.user
    if category in user.subscriptions.all():
        user.subscriptions.remove(category)
    return redirect(request.META.get('HTTP_REFERER'))
