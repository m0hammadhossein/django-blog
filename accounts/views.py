from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from blog.models import Article


class ArticleList(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/home.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)

class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('author', 'title', 'category', 'slug', 'description', 'thumbnail', 'publish', 'status')
    template_name = 'registration/article-create-update.html'
