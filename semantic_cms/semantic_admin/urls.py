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


content_patterns = [
    url(r'^$', ContentView.as_view(), name='index'),
    url(r'^create/$', CreateArticleView.as_view(), name='create_article'),
]

urlpatterns = [
    url(r'^content/$', include(content_patterns, namespace="content")),
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^login/$', views.login, {'template_name': 'semantic_admin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'semantic_admin/logged_out.html'}, name='logout'),

]
