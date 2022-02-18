from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import Home, ArticleView, ArticlePreview, CategoryView, AuthorView, SearchView
from .api.views import ArticleAPIView

app_name = 'blog'
router = routers.SimpleRouter()
router.register('articles', ArticleAPIView, basename='api')

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('articles/<str:slug>/', ArticleView.as_view(), name='detail'),
    path('api/', include(router.urls)),
    path('preview/<int:pk>/', ArticlePreview.as_view(), name='preview'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('author/<slug:username>/', AuthorView.as_view(), name='author'),
    path('search/', SearchView.as_view(), name='search'),
]
