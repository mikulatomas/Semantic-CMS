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
        semanticNodes = [Semantic(**item, created_date=timezone.now()) for item in validated_data]
        return Semantic.objects.bulk_create(semanticNodes)

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        # print("UPDATE")
        # semantic_mapping = {semantic.id: semantic for semantic in instance}
        # data_mapping = {item['id']: item for item in validated_data}
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


    # is_root_node = serializers.BooleanField(source = 'is_root')
    # is_root_node = serializers.ReadOnlyField(source = 'is_root')
    # is_leaf_node = serializers.ReadOnlyField(source = 'is_leaf')
    type = serializers.ReadOnlyField()
    # number_of_descendants = serializers.IntegerField(source = 'descendants_set_size')
    number_of_descendants = serializers.ReadOnlyField(source = 'descendants_set_size')
    # slug = serializers.ReadOnlyField()
    slug = serializers.CharField()

    class Meta:
        list_serializer_class = SemanticNodeListSerializer
        # fields = ('id', 'name')
        # read_only_fields = (
        #     'is_root_node',
        #     'number_of_descendants'
        # )

    def create(self, validated_data):
        semanticNode = Semantic(
            name=validated_data['name'],
            # slug=slugify(validated_data['name'])
        )
        semanticNode.save()
        return semanticNode

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.edited_date = timezone.now()
        instance.save()
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
            # else:
                # ret.append(self.child.update(semanticEdge, data))

        # Perform deletions.
        for semanticEdge_id, semanticEdge in semanticEdge_mapping.items():
            if semanticEdge_id not in data_mapping:
                # print("DELETE EDGE")
                # print(semanticEdge)
                semanticEdge.delete()

        return ret

class SemanticEdgeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # parent = serializers.IntegerField(source = 'parentId')
    # child = serializers.IntegerField(source = 'childId')
    parent = serializers.ReadOnlyField(source = 'parentId')
    child = serializers.ReadOnlyField(source = 'childId')
    parent_slug = serializers.CharField(source = 'parentSlug')
    child_slug = serializers.CharField(source = 'childSlug')

    class Meta:
        list_serializer_class = SemanticEdgeListSerializer
        # fields = ('id', 'parent', 'child')

    def create(self, validated_data):
        print(validated_data)
        semanticEdge = SemanticEdge(
            # parent = Semantic.objects.get(pk=validated_data['parentId']),
            # child = Semantic.objects.get(pk=validated_data['childId']),
            # created_date = timezone.now()
            parent = Semantic.objects.get(slug=validated_data['parentSlug']),
            child = Semantic.objects.get(slug=validated_data['childSlug']),
        )
        semanticEdge.save()
        return semanticEdge

    # def update(self, instance, validated_data):
    #     print(instance.parent)
    #     print(Semantic.objects.get(pk=validated_data['parentId']))
    #     print(instance.child)
    #     print(Semantic.objects.get(pk=validated_data['childId']))
    #     # instance.parent = validated_data.get('parent', instance.parent)
    #     # instance.child = validated_data.get('child', instance.child
    #     instance.parent = Semantic.objects.get(pk=validated_data['parentId'])
    #     instance.child = Semantic.objects.get(pk=validated_data['childId'])
    #     instance.edited_date = timezone.now()
    #     instance.save()
    #     return instance
