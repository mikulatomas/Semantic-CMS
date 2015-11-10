from django.contrib import admin

from .models import Semantic
from .models import Relationship

class RelationshipInline(admin.TabularInline):
    model = Relationship
    fk_name = 'parent'
    extra = 1

class SemanticAdmin(admin.ModelAdmin):
    inlines = (RelationshipInline,)


admin.site.register(Semantic, SemanticAdmin)
admin.site.register(Relationship)
