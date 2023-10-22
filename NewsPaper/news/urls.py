from django.urls import path
from .views import PostList, PostDetail, PostAdd, PostEdit, PostDelete, \
    become_author, become_common

app_name = 'news'
urlpatterns = [
    path('', PostList.as_view()),
    path('search/', PostList.as_view()), 
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('create/', PostAdd.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('become_author', become_author, name='become_author'),
    path('become_common', become_common, name='become_common'),
]
