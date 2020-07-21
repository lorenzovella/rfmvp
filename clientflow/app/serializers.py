from rest_framework import serializers

from . import models


class CachorroEspecialSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CachorroEspecial
        fields = [
            "created",
            "last_updated",
        ]

class EntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Entrega
        fields = [
            "last_updated",
            "created",
        ]

class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Pedido
        fields = [
            "last_updated",
            "created",
        ]

class PlanosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Planos
        fields = [
            "last_updated",
            "created",
        ]

class CachorroSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cachorro
        fields = [
            "last_updated",
            "created",
        ]

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cliente
        fields = [
            "created",
            "last_updated",
        ]
