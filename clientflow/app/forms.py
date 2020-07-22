from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML

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
    def __init__(self, *args, **kwargs):
        super(CachorroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('nome', placeholder="Digite aqui o nome do seu cão"),
            Field('sexo'),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )

class CachorroForm2(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "castrado",
            "raca",
        ]
    def __init__(self, *args, **kwargs):
        super(CachorroForm2, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('castrado'),
            Field('raca', placeholder="Digite aqui..."),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )

class CachorroForm3(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "nascimento",
        ]
    peso = forms.DecimalField(max_digits=3, decimal_places=1,initial='', required=False)
    pesoideal = forms.DecimalField(max_digits=3, decimal_places=1, initial='', required=False)
    def __init__(self, *args, **kwargs):
        super(CachorroForm3, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('nascimento'),
            Field('peso', placeholder="Ex. 10,3kg"),
            Field('pesoideal', placeholder="Ex. 10,3kg", type="hidden"),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )

class CachorroForm4 (forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["atividade",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm4, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('atividade'),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )
class CachorroForm5(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["fisico",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm5, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('fisico'),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )
class CachorroEspecialForm  (forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = [
            "condicao",
            "medicamento",
            "descricao",
            "anexo",
        ]
    def __init__(self, *args, **kwargs):
        super(CachorroEspecialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('condicao'),
            Field('medicamento'),
            Field('descricao'),
            Field('anexo'),
            HTML('{% if wizard.steps.prev %}<button name="wizard_goto_step" class="btn btn-secondary" type="submit" value="{{ wizard.steps.prev }}">Etapa Anterior</button>{% endif %}'),
            HTML('<input type="submit" class="btn btn-primary" value="Enviar"/>'),
        )
