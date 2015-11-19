from django.http import HttpResponse
from .models import Keyword
from django.core import serializers
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
