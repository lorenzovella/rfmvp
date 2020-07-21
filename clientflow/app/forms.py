from django import forms
from . import models


class CachorroEspecialForm(forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = []



class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = []



class PedidoForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = [
            "idClient",
            "idPlano",
            "idEntrega",
            "refDog",
        ]


class PlanosForm(forms.ModelForm):
    class Meta:
        model = models.Planos
        fields = []



class CachorroForm(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "idCliente",
            "dogEspecial",
        ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = []

