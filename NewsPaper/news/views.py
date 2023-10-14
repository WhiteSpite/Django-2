from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

class NewsList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
