from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.api.serializers import PostSerializer, PostRetrieveSerializer, CategorySerializer
from blog.core.paginate import StandardResultsSetPagination
from blog.models import Post, Category


class PostList(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        category = self.request.query_params.get('category', None)
        if category:
            try:
                category = int(category)
                queryset = queryset = Post.objects.filter(status='published', category__pk=category)
            except ValueError:
                queryset = queryset.none()
        return queryset


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
