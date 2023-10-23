from django.contrib import admin
from .models import Post, Comment, Category, Author


admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
