from django.conf.urls import patterns, url, include
from keywords import views

urlpatterns = [
    url(r'^list$', views.list_keywords, name='keywords-list'),
]
