from .models import Article
from rest_framework import viewsets
from .serializers import ArticleSerializer, ArticleEdgeSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see Articles.
    """
    queryset = Article.objects.all().order_by('-created_date')
    serializer_class = ArticleSerializer

class ArticleEdgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see Articles connections.
    """
    queryset = Article.objects.all().order_by('-created_date')
    serializer_class = ArticleEdgeSerializer
