from django.contrib import admin

from .models import Semantic
from .models import SemanticEdge
# from .models import Relationship
#
# class RelationshipInline(admin.TabularInline):
#     model = Relationship
#     fk_name = 'parent'
#     extra = 1

# class SemanticAdmin(admin.ModelAdmin):
#     inlines = (RelationshipInline,)


# admin.site.register(Semantic, SemanticAdmin)
# admin.site.register(Relationship)

admin.site.register(Semantic)
admin.site.register(SemanticEdge)
