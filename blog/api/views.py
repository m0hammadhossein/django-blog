from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.api.serializers import PostSerializer, PostRetrieveSerializer, CategorySerializer, CommentSerializer
from blog.core.paginate import StandardResultsSetPagination
from blog.models import Post, Category, Comment


class PostList(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status='published')
    filterset_fields = ('category',)


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostRetrieve(RetrieveAPIView):
    serializer_class = PostRetrieveSerializer
    lookup_field = 'slug'
    queryset = Post.objects.filter(status='published')


class PostLike(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        post = get_object_or_404(Post.objects.filter(status='published'), pk=pk)
        if not post.users_liked.filter(pk=request.user.pk).exists():
            post.users_liked.add(request.user)
            post.likes += 1
            post.save(update_fields=['likes'])
            return Response({'message': 'liked'}, status=status.HTTP_200_OK)
        else:
            post.users_liked.remove(request.user)
            post.likes -= 1
            post.save(update_fields=['likes'])
            return Response({'message': 'unliked'}, status=status.HTTP_200_OK)


class PostComment(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=Post(pk=self.kwargs['pk']))

    def get_queryset(self):
        return Comment.objects.filter(is_approved=True, post__pk=self.kwargs['pk'])
