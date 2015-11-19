from django.http import HttpResponse
from django.core import serializers
# from taggit.models import Tag
from keywords.models import Keyword

from django.core import serializers
import json

def list_tags(request):
	try:
		# tags = Tag.objects.filter(name__istartswith=request.GET['q']).values_list('name', flat=True)
		# tags = Keyword.objects.filter(name__istartswith=request.GET['q']).values_list('name', flat=True)
		# tags = Keyword.objects.values_list('name', flat=True)
		# tags = Keyword.objects.filter(name__istartswith=request.GET['term']).values_list('name', flat=True)
		# tags_raw = Keyword.objects.filter(name__istartswith=request.GET['term'])
		raw_data = serializers.serialize('python', Keyword.objects.filter(name__istartswith=request.GET['term']), fields=('name'))
		actual_data = [d['fields'] for d in raw_data]
		actual_data = [d['name'] for d in actual_data]
		tags = json.dumps(actual_data)
		# tags = json.dumps(Keyword.objects.filter(name__istartswith=request.GET['term']).values_list('name', flat=True))
	except MultiValueDictKeyError:
		pass

	return HttpResponse(tags, content_type='application/json')
