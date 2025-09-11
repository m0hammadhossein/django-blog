from django.urls import path

from blog.api.views import PostList, PostRetrieve, PostLike, CategoryList, PostComment, PostsAuthor, UserProfile, \
    PostAuthor, NewPost

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts_api'),
    path('author/posts/', PostsAuthor.as_view(), name='posts_author_api'),
    path('author/post/<int:pk>/', PostAuthor.as_view(), name='post_author_api'),
    path('author/post/create/', NewPost.as_view(), name='post_create_api'),
    path('author/profile/', UserProfile.as_view(), name='profile_api'),
    path('category/', CategoryList.as_view(), name='category_api'),
    path('post/<str:slug>/', PostRetrieve.as_view(), name='post_api'),
    path('post/<int:pk>/like/', PostLike.as_view(), name='post_api_like'),
    path('post/<int:pk>/comments/', PostComment.as_view(), name='post_api_comment'),
]
