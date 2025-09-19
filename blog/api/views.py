from django.utils.text import slugify
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.api.serializers import PostSerializer, PostRetrieveSerializer, CategorySerializer, CommentSerializer, \
    UserSerializer, CreatePostSerializer
from blog.core.paginate import StandardResultsSetPagination
from blog.core.throttle import CustomeThrottle
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
    throttle_classes = (CustomeThrottle,)
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


class PostComment(ListCreateAPIView):
    throttle_classes = (CustomeThrottle,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=Post(pk=self.kwargs['pk']))

    def get_queryset(self):
        return Comment.objects.filter(is_approved=True, post__pk=self.kwargs['pk']).select_related('author')


class PostsAuthor(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostAuthor(RetrieveUpdateDestroyAPIView):
    throttle_classes = (CustomeThrottle,)
    serializer_class = CreatePostSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Post.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, author=self.request.user, pk=self.kwargs['pk'])


class UserProfile(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class NewPost(CreateAPIView):
    throttle_classes = (CustomeThrottle,)
    serializer_class = CreatePostSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, slug=slugify(serializer.validated_data['title'], allow_unicode=True))
