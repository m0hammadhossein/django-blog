from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from accounts.mixins import FieldsMixin
from blog.models import Article


class ArticleList(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/home.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)

class ArticleCreate(LoginRequiredMixin, FieldsMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.status = 'd'
        return super().form_valid(form)
