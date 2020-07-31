from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import *
from crispy_forms.layout import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import uuid


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["nome","sobrenome","email","telefone","areatelefone","cep","cpf","rua","nascimento","numero","complemento","cidade","estado",]
    nascimento = forms.DateField(
    widget=forms.DateInput(format='%d/%m/%Y'),
    input_formats=('%d/%m/%Y', )
    )
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML("<p class='control-label text-center'>Precisamos de mais alguns dados para finalizar sua compra</p>"),
            HTML("<div class='row mx-auto' style='white-space: nowrap;'>"),
            Field('nome', wrapper_class="col-6"),
            Field('sobrenome', wrapper_class="col-6"),
            HTML("</div>"),
            Field('email', wrapper_class="col-12"),
            HTML("<div class='row mx-auto' style='white-space: nowrap;'>"),
            Field('areatelefone', wrapper_class="col-4"),
            Field('telefone', wrapper_class="col-8"),
            HTML("</div>"),
            Field('cpf'),
            Field('cep'),
            Field('rua'),
            Field('nascimento'),
            Field('numero'),
            Field('complemento'),
            Field('cidade'),
            Field('estado'),
            HTML('<button type="submit" id="submit-btn"></button>'),
        )

class ClienteNovoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email",]
    def clean(self):
        username = self.cleaned_data['email']
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password1']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'O email "%s" já esta em uso.' % username)
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ClienteNovoForm, self).__init__(*args, **kwargs)

        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields.pop('username')
        self.fields['email'].widget.attrs.update({'class' : 'textinput mt-2 mb-3'})
        self.fields['password1'].widget.attrs.update({'class' : 'textinput mt-2 mb-3'})
        self.fields['password2'].widget.attrs.update({'class' : 'textinput mt-2 mb-3'})

class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['dia']
    def __init__(self, *args, **kwargs):
        super(EntregaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            InlineCheckboxes('dia'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )
class EntregaForm2(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['periodo',]
    def __init__(self, *args, **kwargs):
        super(EntregaForm2 , self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            InlineCheckboxes('periodo'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )
class EntregaForm3(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['preferencia','frequencia']
    def __init__(self, *args, **kwargs):
        super(EntregaForm3 , self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            HTML('<div class="card"><div class="card-body"><p class="card-heading">Próxima entrega</p><p class="card-text">{{dia|join:", "}}</p><p class="card-text">{{periodo|join:", "}}</p></div></div>'),
            InlineRadios('preferencia'),
            InlineRadios('frequencia'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )
class SaboresForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = ['sabores']
    def __init__(self, *args, **kwargs):
        super(SaboresForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            InlineCheckboxes('sabores'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )


class PedidoForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = []


class PlanoForm(forms.ModelForm):
    class Meta:
        model = models.Plano
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
            InlineRadios('sexo'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
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
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            InlineRadios('castrado'),
            Field('raca', placeholder="Digite aqui..."),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )

class CachorroForm3(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "nascimento",
        ]
    peso = forms.DecimalField(max_digits=3, decimal_places=1,initial='')
    pesoideal = forms.DecimalField(label = "Peso estimado do cachorro adulto", max_digits=3, decimal_places=1, initial='', required=False)
    def __init__(self, *args, **kwargs):
        super(CachorroForm3, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            Field('nascimento', css_class=""),
            Field('pesoideal', placeholder="Ex. 10,3kg"),
            Field('peso', placeholder="Ex. 10,3kg"),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )

class CachorroForm4 (forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["atividade",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm4, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            InlineRadios('atividade'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )
class CachorroForm5(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["fisico",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm5, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
            Field('fisico'),
        )
class CachorroEspecialForm(forms.ModelForm):
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
            HTML('<button name="wizard_goto_step" class="btn-back" type="submit" value="{{ wizard.steps.prev }}"><svg width="31px" height="22px" viewBox="0 0 31 22" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><path d="M11.2306 0.421231C11.7798 0.994106 11.7798 1.94508 11.2414 2.52941L4.70545 9.50702L29.611 9.50702C30.3755 9.50702 31 10.1716 31 10.9965C31 11.8214 30.3755 12.486 29.611 12.486L4.70545 12.486L11.2522 19.4636C11.7906 20.0479 11.7798 20.9874 11.2414 21.5718C10.6923 22.1446 9.82008 22.1446 9.27093 21.5603L0.398402 12.0506C0.279958 11.9131 0.18305 11.7642 0.107676 11.5808C0.0323029 11.3975 0 11.2027 0 11.008C0 10.6184 0.139979 10.2518 0.398402 9.96532L9.27093 0.455604C9.79854 -0.140186 10.6815 -0.151643 11.2306 0.421231L11.2306 0.421231Z" id="Path" fill="#17437A" stroke="none" /> </svg></button>'),
            Field('condicao'),
            Field('medicamento'),
            Field('descricao'),
            Field('anexo'),
            HTML('<div class="footer margin-footer"><input type="submit" class="btn-next" value="Continuar"/></div>'),
        )
