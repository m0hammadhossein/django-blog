from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from accounts.mixins import AuthorAccessMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from blog.api.serializers import ArticleSerializer
from blog.models import Article, Category

User = get_user_model()


class Home(ListView):
    template_name = 'index.html'
    paginate_by = 10
    ordering = ('-publish',)
    context_object_name = 'articles'
    queryset = Article.objects.published()


class ArticleView(DetailView):
    template_name = 'post.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article.objects.published(), slug=self.kwargs['slug'])
        try:
            article.hits.add(self.request.user.ip_address)
        except:
            pass
        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    model = Article
    template_name = 'post.html'
    context_object_name = 'article'


class CategoryView(ListView):
    template_name = 'category.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(Category.objects.active(), slug=self.kwargs['slug'])
        return self.category.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = self.category
        return context


class AuthorView(ListView):
    template_name = 'author.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return self.author.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['author'] = self.author
        return context


class SearchView(ListView):
    template_name = 'search.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(Q(description__icontains=self.request.GET.get('q')) | Q(title__icontains=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search'] = self.request.GET.get('q')
        return context


class ArticleAPIView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ArticleSerializer
    search_fields = ('title', 'description')
    ordering_fields = ('publish',)

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.is_authenticated and self.request.user.is_special_user():
            self.filterset_fields = ('is_special',)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_special_user():
            return Article.objects.filter(status='p')
        return Article.objects.filter(status='p', is_special=False)
