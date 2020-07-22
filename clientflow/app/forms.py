from django import forms
from . import models

class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = []

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
            "nome",
            "sexo",
        ]

class CachorroForm2(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "castrado",
            "raca",
        ]

class CachorroForm3(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "nascimento",
            "peso",
            "pesoideal",
        ]

class CachorroForm4 (forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["atividade",]

class CachorroForm5(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["fisico",]

class CachorroEspecialForm  (forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = [
            "condicao",
            "medicamento",
            "descricao",
            "anexo",
        ]
