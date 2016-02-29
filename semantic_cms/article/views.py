from .models import Article
from rest_framework import viewsets
from .serializers import ArticleSerializer, ArticleEdgeSerializer
from django.views.generic import ListView, DetailView

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

class ArticleListView(ListView):
    """
    View for blog article list
    """

    model = Article
    queryset = Article.objects.select_related().order_by('-published_date').filter(status='P')
    context_object_name = 'article_list'
    template_name = 'blog/homepage.html'

class ArticleDetailView(DetailView):
    """
    View for detail of the article
    """

    model = Article
    context_object_name = 'article'
    template_name = 'blog/article.html'
