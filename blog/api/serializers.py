from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Post, Category, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'avatar', 'biography', 'is_staff')
        read_only_fields = ('username', 'is_staff')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Post
        exclude = ('updated_at', 'created_at', 'users_liked', 'body')
        read_only_fields = ('author', 'likes', 'comments', 'status', 'category')


class CreatePostSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        exclude = ('updated_at', 'id', 'created_at', 'users_liked',)
        read_only_fields = ('author', 'likes', 'comments', 'published_at', 'slug')


class PostRetrieveSerializer(PostSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return obj.users_liked.filter(pk=self.context['request'].user.pk).exists()

    class Meta(PostSerializer.Meta):
        exclude = ('updated_at', 'created_at', 'users_liked')
        read_only_fields = ('author', 'is_liked', 'category')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    avatar = serializers.ImageField(source='author.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = ('author', 'created_at', 'content', 'avatar')
        read_only_fields = ('author', 'created_at', 'avatar')
