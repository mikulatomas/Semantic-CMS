import django_filters
from .models import Article
from django.db import models

class ArticleFilter(django_filters.FilterSet):
    # filter_overrides = {
    #     models.DateTimeField: {
    #         'filter_class': django_filters.DateFromToRangeFilter,
    #         'extra': lambda f: {
    #             'lookup_type': 'icontains',
    #         }
    #     }
    # }

    class Meta:
        model = Article
        # fields = ['title', 'created_date', 'flag', 'status']
        fields = {
                'created_date': ['lt', 'gt'],
                'flag': ['exact'],
                'status': ['exact'],
                'title': ['icontains'],
                # 'sub_title': ['icontains'],
                }
        # together = ['rating', 'price']

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)

        self.filters['flag'].extra.update(
            {'empty_label': 'All article flags'})

        self.filters['status'].field.choices.insert(0, ('', u'All article status'))

        # self.filters['title__icontains'].extra.update(
        #     {'empty_label': 'All article status'})
