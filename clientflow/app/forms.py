from django import forms
from . import models


class CachorroEspecialForm(forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = []

class PlanosForm(forms.ModelForm):
    class Meta:
        model = models.Planos
        fields = []

class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = []

class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = []

class CachorroForm(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "idCliente",
            "dogEspecial",
        ]


class PedidoForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = [
            "idClient",
            "idPlano",
            "idEntrega",
            "refDog",
        ]


class LeadForm(forms.ModelForm):
    class Meta:
        model = models.Lead
        fields = []
