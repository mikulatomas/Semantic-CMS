from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from article.models import Article
from .models import Flag
# Create your views here.

def articles_with_flag(request, slug):
    flag = get_object_or_404(Flag, slug=slug)
    articles = Article.objects.order_by('-published_date').filter(flag=flag, status='P')

    return render_to_response('blog/flag.html', {'flag': flag, 'article_list': articles})
