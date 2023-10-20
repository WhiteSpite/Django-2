from django.urls import path
from .views import PostList, PostDetail, PostAdd, PostEdit, PostDelete

app_name = 'news'
urlpatterns = [
    path('', PostList.as_view()),
    path('search/', PostList.as_view()), 
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('create/', PostAdd.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
