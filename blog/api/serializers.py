from rest_framework import serializers

from ..models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name')
    hits = serializers.SerializerMethodField('hits_count')
    category = serializers.CharField(source='category_to_str')
    publish = serializers.CharField(source='jpublish')

    def hits_count(self, obj):
        return obj.hits.count()

    class Meta:
        model = Article
        exclude = ('created', 'updated', 'status', 'slug')
