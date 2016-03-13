from django.contrib import admin
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.conf.urls import include, patterns, url
from django.shortcuts import render_to_response
from django.contrib.admin import AdminSite
from .models import Article

# Classic admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'flag','author', 'created_date')
    exclude = ("markdown",)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
