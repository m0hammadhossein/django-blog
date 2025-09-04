from django.urls import path

from blog.api.views import PostList, PostRetrieve, PostLike, CategoryList

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts_api'),
    path('category/', CategoryList.as_view(), name='category_api'),
    path('post/<str:slug>/', PostRetrieve.as_view(), name='post_api'),
    path('post/<int:pk>/like', PostLike.as_view(), name='post_api_like'),
]
