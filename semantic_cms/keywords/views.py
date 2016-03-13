from django.http import HttpResponse
from .models import Keyword
from django.core import serializers
from article.models import Article
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import json

def list_keywords(request):
	"""Create json list tag for some GET request - (some first letter)"""
	try:
		raw_data = serializers.serialize('python', Keyword.objects.filter(name__istartswith=request.GET['term']), fields=('name'))
		# Filter just "fields"
		actual_data = [d['fields'] for d in raw_data]
		# filter just "name" of keywords
		actual_data = [d['name'] for d in actual_data]
		# create json
		tags = json.dumps(actual_data)
	except MultiValueDictKeyError:
		pass

	return HttpResponse(tags, content_type='application/json')

def articles_with_keyword(request, slug):
	keyword = get_object_or_404(Keyword, slug=slug)
	articles = Article.objects.order_by('-published_date').filter(keywords=keyword, status='P')
	paginator = Paginator(articles, 5)
	page = request.GET.get('page')
	try:
		article_list = paginator.page(page)
	except PageNotAnInteger:
		article_list = paginator.page(1)
	except EmptyPage:
		article_list = paginator.page(paginator.num_pages)

	return render(request, 'blog/keyword.html', {'keyword': keyword, 'article_list': article_list})
