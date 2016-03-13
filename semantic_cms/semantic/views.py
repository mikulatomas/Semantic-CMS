from .models import Semantic
from .models import SemanticEdge
from article.models import Article
from rest_framework import viewsets
from .serializers import SemanticNodeSerializer, SemanticEdgeSerializer
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

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
    articles = Article.objects.order_by('-published_date').filter(semantic__in=semantic_set, status='P').distinct()
    paginator = Paginator(articles, 5)

    page = request.GET.get('page')

    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/semantic.html', {'semantic': semantic, 'article_list': article_list})
