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
from semantic_admin.views import CreateArticleFlagView
from semantic_admin.views import UpdateArticleFlagView
from semantic_admin.views import DeleteArticleFlagView
from semantic_admin.views import UpdateUserProfileView
from semantic_admin.views import UpdateBlogSettingsView
import semantic_admin.views as semantic_admin_views

content_patterns = [
    url(r'^$', ContentView.as_view(), name='index'),
    url(r'^create/$', CreateArticleView.as_view(), name='create_article'),
    url(r'^edit/(?P<slug>[-_\w]+)$', UpdateArticleView.as_view(), name='edit_article'),
    url(r'^delete/(?P<slug>[-_\w]+)$', DeleteArticleView.as_view(), name='delete_article'),
]

article_types_patterns = [
    url(r'^$', CreateArticleFlagView.as_view(), name='index'),
    url(r'^edit/(?P<slug>[-_\w]+)$', UpdateArticleFlagView.as_view(), name='edit_article_flag'),
    url(r'^delete/(?P<slug>[-_\w]+)$', DeleteArticleFlagView.as_view(), name='delete_article_flag'),
]

settings_patterns = [
    url(r'^$', UpdateBlogSettingsView.as_view(), name='index'),
    url(r'^user/$', UpdateUserProfileView.as_view(), name='user'),
]

semantic_patterns = [
    url(r'^$', SemanticView.as_view(), name='index'),
    url(r'^add_edge/$', semantic_admin_views.add_edge),
    url(r'^save_graph/$', semantic_admin_views.save_graph),
    url(r'^request_article_nodes/$', semantic_admin_views.request_article_nodes),
    url(r'^save_article_nodes/$', semantic_admin_views.save_article_nodes),
    url(r'^article/(?P<slug>[-_\w]+)/$', SemanticView.as_view(), name='article'),
]

urlpatterns = [
    url(r'^', include(content_patterns)),
    url(r'^content/', include(content_patterns, namespace="content")),
    url(r'^article-types/', include(article_types_patterns, namespace="article_types")),
    url(r'^semantic/', include(semantic_patterns, namespace="semantic")),
    url(r'^settings/', include(settings_patterns, namespace="settings")),
    # url(r'^$', DashboardView.as_view(), name='index'),

    url(r'^login/$', auth_views.login, {'template_name': 'semantic_admin/login.html'}, name='login'),
    url(r'^login$', auth_views.login, {'template_name': 'semantic_admin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
]
