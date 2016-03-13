from .models import Semantic
from .models import SemanticEdge
# from django_dag.models import *
from rest_framework import serializers
#time
import datetime
from django.utils import timezone
from django.utils.text import slugify

class SemanticNodeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        semanticNodes = [Semantic(**item) for item in validated_data]
        return Semantic.objects.bulk_create(semanticNodes)

    def update(self, instance, validated_data):
        semantic_mapping = {semantic.slug: semantic for semantic in instance}
        data_mapping = {item['slug']: item for item in validated_data}

        # Perform creations and updates.
        ret = []

        for semantic_id, data in data_mapping.items():
            semantic = semantic_mapping.get(semantic_id, None)
            if semantic is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(semantic, data))

        # Perform deletions.
        for semantic_id, semantic in semantic_mapping.items():
            if semantic_id not in data_mapping:
                semantic.delete()

        return ret

class SemanticNodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.ReadOnlyField()
    number_of_descendants = serializers.ReadOnlyField(source = 'descendants_set_size')
    slug = serializers.CharField()

    class Meta:
        list_serializer_class = SemanticNodeListSerializer

    def create(self, validated_data):
        semanticNode = Semantic(
            name=validated_data['name'],
        )
        semanticNode.save()
        return semanticNode

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class SemanticEdgeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        SemanticEdges = [SemanticEdge(**item, created_date=timezone.now()) for item in validated_data]
        return SemanticEdge.objects.bulk_create(SemanticEdges)

    def update(self, instance, validated_data):
        semanticEdge_mapping = {semanticEdge.id: semanticEdge for semanticEdge in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for semanticEdge_id, data in data_mapping.items():
            semanticEdge = semanticEdge_mapping.get(semanticEdge_id, None)
            if semanticEdge is None:
                ret.append(self.child.create(data))

        # Perform deletions.
        for semanticEdge_id, semanticEdge in semanticEdge_mapping.items():
            if semanticEdge_id not in data_mapping:
                semanticEdge.delete()

        return ret

class SemanticEdgeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.ReadOnlyField(source = 'parentId')
    child = serializers.ReadOnlyField(source = 'childId')
    parent_slug = serializers.CharField(source = 'parentSlug')
    child_slug = serializers.CharField(source = 'childSlug')

    class Meta:
        list_serializer_class = SemanticEdgeListSerializer

    def create(self, validated_data):
        semanticEdge = SemanticEdge(
            parent = Semantic.objects.get(slug=validated_data['parentSlug']),
            child = Semantic.objects.get(slug=validated_data['childSlug']),
        )
        semanticEdge.save()
        return semanticEdge
