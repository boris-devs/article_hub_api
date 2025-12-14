from rest_framework import serializers

from articles.models import Articles


class ArticleBaseSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["_id"] = str(instance._id)
        return data


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "tags")


class ArticleCreateResponseSerializer(ArticleBaseSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "tags", "author", "created_at")


class ArticlesListSerializer(ArticleBaseSerializer):
    class Meta:
        model = Articles
        fields = ("title", "tags", "author",)


class ArticlesRetrieveSerializer(ArticleBaseSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "tags", "author", "created_at")

class ArticlesPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "tags")


class ArticlesAnalyzeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "tags", "analysis")