from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from blog.api.serializers import ArticleSerializer
from blog.models import Article


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


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
