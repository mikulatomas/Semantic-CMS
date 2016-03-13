from django.contrib import admin

from .models import Semantic
from .models import SemanticEdge

admin.site.register(Semantic)
admin.site.register(SemanticEdge)
