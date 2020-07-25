from rest_framework import viewsets, permissions

from . import serializers
from . import models


class CachorroEspecialViewSet(viewsets.ModelViewSet):
    """ViewSet for the CachorroEspecial class"""

    queryset = models.CachorroEspecial.objects.all()
    serializer_class = serializers.CachorroEspecialSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntregaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Entrega class"""

    queryset = models.Entrega.objects.all()
    serializer_class = serializers.EntregaSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Pedido class"""

    queryset = models.Pedido.objects.all()
    serializer_class = serializers.PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlanoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Plano class"""

    queryset = models.Plano.objects.all()
    serializer_class = serializers.PlanoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CachorroViewSet(viewsets.ModelViewSet):
    """ViewSet for the Cachorro class"""

    queryset = models.Cachorro.objects.all()
    serializer_class = serializers.CachorroSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    """ViewSet for the Cliente class"""

    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
