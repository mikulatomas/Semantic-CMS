from .models import Semantic
from .models import SemanticEdge
from rest_framework import viewsets
from .serializers import SemanticNodeSerializer, SemanticEdgeSerializer


class SemanticNodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see semantic categories.
    """
    queryset = Semantic.objects.all().order_by('-created_date')
    serializer_class = SemanticNodeSerializer

class SemanticEdgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see semantic categories.
    """
    queryset = SemanticEdge.objects.all().order_by('-created_date')
    serializer_class = SemanticEdgeSerializer
