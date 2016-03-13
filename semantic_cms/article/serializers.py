from .models import Article
from semantic.models import Semantic
from semantic.serializers import SemanticNodeSerializer
# from django_dag.models import *
from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source = "title")
    type = serializers.CharField()

class ArticleEdgeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    semantic = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
