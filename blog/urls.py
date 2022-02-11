from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('articles/<str:slug>/', views.ArticleView.as_view(), name='detail'),
    path('preview/<int:pk>/', views.ArticlePreview.as_view(), name='preview'),
    path('category/<str:slug>/', views.CategoryView.as_view(), name='category'),
    path('author/<slug:username>/', views.AuthorView.as_view(), name='author'),
    path('search/', views.SearchView.as_view(), name='search'),
]
