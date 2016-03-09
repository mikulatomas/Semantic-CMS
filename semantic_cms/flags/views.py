from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from article.models import Article
from .models import Flag
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.

def articles_with_flag(request, slug):
    flag = get_object_or_404(Flag, slug=slug)

    articles = Article.objects.order_by('-published_date').filter(flag=flag, status='P')
    paginator = Paginator(articles, 5)

    page = request.GET.get('page')

    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/flag.html', {'flag': flag, 'article_list': article_list})
