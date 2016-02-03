from .models import Semantic
from .models import SemanticEdge
# from django_dag.models import *
from rest_framework import serializers
#time
import datetime
from django.utils import timezone

class SemanticNodeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        semanticNodes = [Semantic(**item, created_date=timezone.now()) for item in validated_data]
        return Semantic.objects.bulk_create(semanticNodes)

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        # print("UPDATE")
        semantic_mapping = {semantic.id: semantic for semantic in instance}
        data_mapping = {item['id']: item for item in validated_data}

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
    # is_root_node = serializers.BooleanField(source = 'is_root')
    is_root_node = serializers.ReadOnlyField(source = 'is_root')
    # number_of_descendants = serializers.IntegerField(source = 'descendants_set_size')
    number_of_descendants = serializers.ReadOnlyField(source = 'descendants_set_size')

    class Meta:
        list_serializer_class = SemanticNodeListSerializer
        fields = ('id', 'name')
        read_only_fields = (
            'is_root_node',
            'number_of_descendants'
        )

    def create(self, validated_data):
        semanticNode = Semantic(
            name=validated_data['name'],
            created_date=timezone.now()
        )
        semanticNode.save()
        return semanticNode

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.edited_date = timezone.now()
        return instance

class SemanticEdgeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        SemanticEdges = [SemanticEdge(**item, created_date=timezone.now()) for item in validated_data]
        return SemanticEdge.objects.bulk_create(SemanticEdges)

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        # print("UPDATE")
        semanticEdge_mapping = {semanticEdge.id: semanticEdge for semanticEdge in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for semanticEdge_id, data in data_mapping.items():
            semanticEdge = semanticEdge_mapping.get(semanticEdge_id, None)
            if semanticEdge is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(semanticEdge, data))

        # Perform deletions.
        for semanticEdge_id, semanticEdge in semanticEdge_mapping.items():
            if semanticEdge_id not in data_mapping:
                semanticEdge.delete()

        return ret

class SemanticEdgeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.IntegerField(source = 'parentId')
    child = serializers.IntegerField(source = 'childId')

    class Meta:
        list_serializer_class = SemanticEdgeListSerializer
        fields = ('id', 'parent', 'child')

    def create(self, validated_data):
        semanticEdge = SemanticEdge(
            parent=validated_data['parent'],
            child=validated_data['child'],
            created_date=timezone.now()
        )
        semanticEdge.save()
        return semanticEdge

    def update(self, instance, validated_data):
        instance.parent = validated_data.get('parent', instance.parent)
        instance.child = validated_data.get('child', instance.child)
        instance.edited_date = timezone.now()
        return instance
