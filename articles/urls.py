
from django.urls import path
from rest_framework import routers

from articles.views import ArticlesViewSet, ArticleAnalyzeView

router = routers.DefaultRouter()
router.register(r'articles', ArticlesViewSet)


urlpatterns = [
    path("articles/<str:pk>/analyze/", ArticleAnalyzeView.as_view(), name="articles-analyze"),
]
urlpatterns += router.urls