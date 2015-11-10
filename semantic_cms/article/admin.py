from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'statut', 'flag','author', 'created_date')
    exclude = ("markdown",)
    filter_horizontal = ("semantic",)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
