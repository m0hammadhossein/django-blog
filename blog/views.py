from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from blog.models import Article, Category

User = get_user_model()

class Home(ListView):
    template_name = 'index.html'
    paginate_by = 10
    ordering = ('-publish',)
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.published()



class ArticleView(DetailView):
    template_name = 'post.html'
    context_object_name = 'article'

    def get_object(self):
        return get_object_or_404(Article.objects.published(), slug=self.kwargs['slug'])


class CategoryView(ListView):
    template_name = 'category.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(Category.objects.active(),slug=self.kwargs['slug'])
        return self.category.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list,**kwargs)
        context['category'] = self.category
        return context

class AuthorView(ListView):
    template_name = 'author.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        self.author = get_object_or_404(User,username=self.kwargs['username'])
        return self.author.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list,**kwargs)
        context['author'] = self.author
        return context


