import django_filters
from .models import Article
from django.db import models

class ArticleFilter(django_filters.FilterSet):
    search = django_filters.MethodFilter(action='search_filter')

    class Meta:
        model = Article
        fields = {
                'created_date': ['lt', 'gt'],
                'flag': ['exact'],
                'status': ['exact'],
                'search': [],
                }

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)

        self.queryset = self.queryset.order_by('-published_date')
        self.filters['flag'].extra.update(
            {'empty_label': 'All article flags'})

        self.filters['status'].field.choices.insert(0, ('', u'All article status'))

    def search_filter(self, queryset, value):
        return queryset.filter(
            title__icontains=value,
        ) | queryset.filter(sub_title__icontains=value,) | queryset.filter(content__icontains=value,) | queryset.filter(keywords__name__icontains=value,)
