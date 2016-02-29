from .models import Semantic
from .models import SemanticEdge
from article.models import Article
from rest_framework import viewsets
from .serializers import SemanticNodeSerializer, SemanticEdgeSerializer
from django.shortcuts import render_to_response, get_object_or_404


class SemanticNodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see semantic categories.
    """
    queryset = Semantic.objects.all().order_by('-created_date')
    serializer_class = SemanticNodeSerializer

class SemanticEdgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see semantic categories.
    """
    queryset = SemanticEdge.objects.all().order_by('-created_date')
    serializer_class = SemanticEdgeSerializer

def articles_from_semantic(request, slug):
    semantic = get_object_or_404(Semantic, slug=slug)
    semantic_set = semantic.descendants_set()
    semantic_set.add(semantic)
    # articles = Article.objects.filter(semantic__in=semantic_set).distinct()
    articles = Article.objects.order_by('-published_date').filter(semantic__in=semantic_set, status='P').distinct()

    return render_to_response('blog/semantic.html', {'semantic': semantic, 'article_list': articles})
