from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
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

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_edit.html'
    context_object_name = 'post'


class PostAdd(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create.html'
    context_object_name = 'post'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post'
    success_url = '/news/'
