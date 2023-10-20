import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'author': ['exact'], 
            'title': ['icontains'], 
            'created_at': ['gt']
        }
