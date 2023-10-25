from django.urls import path
from .views import PostList, PostDetail, PostAdd, PostEdit, PostDelete, \
    become_author, become_common, subscribe_to, unsubscribe_to
from django.views.decorators.cache import cache_page

app_name = 'news'
urlpatterns = [
    path('', cache_page(60)(PostList.as_view())),
    path('search/', cache_page(60)(PostList.as_view())), 
    path('<int:pk>/', cache_page(300)(PostDetail.as_view()), name='post'),
    path('create/', cache_page(1200)(PostAdd.as_view()), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('become_author', become_author, name='become_author'),
    path('become_common', become_common, name='become_common'),
    path('subscribe_to', subscribe_to, name='subscribe_to'),
    path('unsubscribe_to', unsubscribe_to, name='unsubscribe_to'),
]
