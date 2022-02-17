from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'blog'
router = routers.SimpleRouter()
router.register('articles',views.ArticleAPIView, basename='api')

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('articles/<str:slug>/', views.ArticleView.as_view(), name='detail'),
    path('api/', include(router.urls)),
    path('preview/<int:pk>/', views.ArticlePreview.as_view(), name='preview'),
    path('category/<str:slug>/', views.CategoryView.as_view(), name='category'),
    path('author/<slug:username>/', views.AuthorView.as_view(), name='author'),
    path('search/', views.SearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)