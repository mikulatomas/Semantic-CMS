from django.contrib import admin
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.conf.urls import include, patterns, url
from django.shortcuts import render_to_response
from django.contrib.admin import AdminSite
from .models import Article

# Classic admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'statut', 'flag','author', 'created_date')
    exclude = ("markdown",)
    filter_horizontal = ("semantic",)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)

# My custom admin

class MyAdminSite(AdminSite):
    site_header = 'Semantic CMS'

    module_name_dict = {
        Article: 'content'
    }

    def get_urls(self):
        base_patterns = super(MyAdminSite, self).get_urls()
        my_patterns = patterns('',)

        for model, model_admin in self._registry.items():
            if model in self.module_name_dict:
                module_name = self.module_name_dict[model]
                my_patterns += patterns('',
                    url(r'^%s/' % (module_name),
                        include(model_admin.urls))
                )

        return my_patterns + base_patterns



class MyArticleAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(MyArticleAdmin, self).get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(self.content)),
        ]
        return my_urls + urls

    def content(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           article_list = Article.objects.all(),
        )
        return TemplateResponse(request, "admin/article/edit_article.html", context)


my_admin = MyAdminSite(name='myadmin')
my_admin.register(Article, MyArticleAdmin)
