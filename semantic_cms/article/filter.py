import django_filters
from .models import Article
from django.db import models

class ArticleFilter(django_filters.FilterSet):

    class Meta:
        model = Article
        fields = {
                'created_date': ['lt', 'gt'],
                'flag': ['exact'],
                'status': ['exact'],
                'title': ['icontains'],
                }

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)

        self.filters['flag'].extra.update(
            {'empty_label': 'All article flags'})

        self.filters['status'].field.choices.insert(0, ('', u'All article status'))
