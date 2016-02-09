from .models import Article
from semantic.models import Semantic
from semantic.serializers import SemanticNodeSerializer
# from django_dag.models import *
from rest_framework import serializers
#time
import datetime
from django.utils import timezone

# class SemanticNodeListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         semanticNodes = [Semantic(**item, created_date=timezone.now()) for item in validated_data]
#         return Semantic.objects.bulk_create(semanticNodes)
#
#     def update(self, instance, validated_data):
#         # Maps for id->instance and id->data item.
#         # print("UPDATE")
#         semantic_mapping = {semantic.id: semantic for semantic in instance}
#         data_mapping = {item['id']: item for item in validated_data}
#
#         # Perform creations and updates.
#         ret = []
#         for semantic_id, data in data_mapping.items():
#             semantic = semantic_mapping.get(semantic_id, None)
#             if semantic is None:
#                 ret.append(self.child.create(data))
#             else:
#                 ret.append(self.child.update(semantic, data))
#
#         # Perform deletions.
#         for semantic_id, semantic in semantic_mapping.items():
#             if semantic_id not in data_mapping:
#                 semantic.delete()
#
#         return ret

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source = "title")
    type = serializers.CharField()


    # # is_root_node = serializers.BooleanField(source = 'is_root')
    # is_root_node = serializers.ReadOnlyField(source = 'is_root')
    # is_leaf_node = serializers.ReadOnlyField(source = 'is_leaf')
    # # number_of_descendants = serializers.IntegerField(source = 'descendants_set_size')
    # number_of_descendants = serializers.ReadOnlyField(source = 'descendants_set_size')

    # class Meta:
        # list_serializer_class = SemanticNodeListSerializer
        # fields = ('id', 'name')
        # read_only_fields = (
        #     'is_root_node',
        #     'number_of_descendants'
        # )

    # def create(self, validated_data):
    #     semanticNode = Semantic(
    #         name=validated_data['name'],
    #         created_date=timezone.now()
    #     )
    #     semanticNode.save()
    #     return semanticNode
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.edited_date = timezone.now()
    #     return instance

# class SemanticSerializer(serializers.ModelSerializer):
#     # id = serializers.IntegerField()
#
#     class Meta:
#         model = Semantic
#         fields = ("__all__")

class ArticleEdgeSerializer(serializers.Serializer):
    parent = serializers.IntegerField(source = "id")
    semantic = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
