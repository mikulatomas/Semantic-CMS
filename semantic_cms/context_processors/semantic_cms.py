from semantic_admin.models import BlogSettings
from semantic.models import Semantic
from keywords.models import Keyword
from django.db.models import Count

def basic(request):
    blog_settings = BlogSettings.objects.filter(pk = 1)
    context = {}

    popular_semantic = Semantic.objects.annotate(article_count=Count('article')).order_by('-article_count')

    popular_keywords = Keyword.objects.annotate(article_count=Count('article')).order_by('-article_count')

    if (blog_settings.count() != 0):
        context['blog_settings'] = blog_settings[0]

    context['popular_semantic'] = popular_semantic
    context['popular_keywords'] = popular_keywords

    return context;
