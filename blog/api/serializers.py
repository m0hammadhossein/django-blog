from rest_framework import serializers

from blog.models import Post, Category, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Post
        exclude = ('updated_at', 'id', 'created_at', 'users_liked', 'body')
        read_only_fields = ('author',)


class PostRetrieveSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    def get_is_liked(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return obj.users_liked.filter(pk=self.context['request'].user.pk).exists()

    class Meta:
        model = Post
        exclude = ('updated_at', 'created_at', 'users_liked')
        read_only_fields = ('author', 'is_liked')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('author', 'created_at', 'content')
        read_only_fields = ('author', 'created_at')
