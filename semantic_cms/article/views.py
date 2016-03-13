from .models import Article
from rest_framework import viewsets
from .serializers import ArticleSerializer, ArticleEdgeSerializer
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

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
    template_name = 'blog/homepage.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        article_list = Article.objects.order_by('-published_date').filter(status='P')
        # article_list = Article.objects.all()
        paginator = Paginator(article_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['article_list'] = articles
        return context

class ArticleDetailView(DetailView):
    """
    View for detail of the article
    """

    model = Article
    context_object_name = 'article'
    template_name = 'blog/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = context['article']

        context['similar_articles'] = article.return_similar_articles(4)
        return context
