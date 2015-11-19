from django.conf.urls import patterns, url, include

urlpatterns = patterns('taggit_autocomplete.views',
    url(r'^list$', 'list_tags', name='taggit_autocomplete-list'),
)
