from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from articles.models import Articles
from articles.serializers import (ArticleCreateSerializer, ArticleCreateResponseSerializer, ArticlesListSerializer,
                                  ArticlesRetrieveSerializer, ArticlesPartialUpdateSerializer,
                                  ArticlesAnalyzeSerializer)


class ArticlesViewSet(viewsets.ViewSet):
    queryset = Articles.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = str(request.user._id)

        article = serializer.save()
        response_serializer = ArticleCreateResponseSerializer(article)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        search_filter = request.query_params.get("search")
        tag_filter = request.query_params.get("tag")
        if search_filter:
            self.queryset = self.queryset.filter(
                Q(title__icontains=search_filter) | Q(content__icontains=search_filter)
            )
        if tag_filter:
            self.queryset = self.queryset.filter(tags__icontains=tag_filter)

        serializer = ArticlesListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        article = self.queryset.get(pk=pk)
        serializer = ArticlesRetrieveSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        article = self.queryset.get(pk=pk)
        if article.author != request.user._id:
            raise PermissionDenied
        serializer = ArticlesPartialUpdateSerializer(instance=article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        article = self.queryset.get(pk=pk)
        if article.author != request.user._id:
            raise PermissionDenied
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleAnalyzeView(RetrieveUpdateAPIView):
    serializer_class = ArticlesAnalyzeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Articles.objects.all()

    def partial_update(self, request, pk=None):
        article = self.queryset.get(pk=pk)

        words_content_count = len(article.content.split())
        unique_tags_count = len(set(article.tags))

        article.analysis = {
            "word_count": words_content_count,
            "unique_tags": unique_tags_count
        }
        article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
