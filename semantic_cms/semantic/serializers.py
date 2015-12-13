from .models import Semantic
from .models import SemanticEdge
# from django_dag.models import *
from rest_framework import serializers


# class SemanticSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Semantic
#         fields = ('id', 'name', 'children')

class SemanticNodeSerializer(serializers.ModelSerializer):
    is_root_node = serializers.BooleanField(source = 'is_root')
    number_of_descendants = serializers.IntegerField(source = 'descendants_set_size')

    class Meta:
        model = Semantic
        fields = ('id', 'name', 'is_root_node', 'number_of_descendants')
        read_only_fields = (
            'is_root_node',
            'number_of_descendants'
        )

class SemanticEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemanticEdge
        fields = ('parent', 'child')
