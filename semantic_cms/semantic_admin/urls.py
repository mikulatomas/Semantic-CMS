"""semantic_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from semantic_admin import views
from semantic_admin.views import DashboardView
from semantic_admin.views import ContentView
from semantic_admin.views import CreateArticleView
from semantic_admin.views import DeleteArticleView
from semantic_admin.views import UpdateArticleView
from semantic_admin.views import SemanticView
# from semantic_admin.views import ContentViewFilter


content_patterns = [
    url(r'^$', ContentView.as_view(), name='index'),
    # url(r'^filter/$', ContentViewFilter.as_view(), name='index_filter'),
    url(r'^create/$', CreateArticleView.as_view(), name='create_article'),
    url(r'^edit/(?P<pk>\d+)$', UpdateArticleView.as_view(), name='edit_article'),
    url(r'^delete/(?P<pk>\d+)$', DeleteArticleView.as_view(), name='delete_article'),
]

semantic_patterns = [
    url(r'^$', SemanticView.as_view(), name='index'),
]

urlpatterns = [
    url(r'^content/', include(content_patterns, namespace="content")),
    url(r'^semantic/', include(semantic_patterns, namespace="semantic")),
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^login/$', views.login, {'template_name': 'semantic_admin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),

]
