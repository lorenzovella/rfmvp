from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import *
from crispy_forms.layout import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

footerHtml=Div(Submit("submit","Continuar",css_class="btn-next"), css_class="footer margin-footer")
goBackBtn = HTML('<button name="wizard_goto_step" class="btn-back col-10" type="submit" value="{{ wizard.steps.prev }}"><svg width="22px" height="22px" viewBox="0 0 22 22"><path d="M0.385618 11.8615L0.346067 11.8082L0.326292 11.7905L0.286742 11.7638L0.266966 11.7283C0.227416 11.675 0.197753 11.6306 0.16809 11.5862L0.138427 11.5418L0.108764 11.4885C0.0889888 11.4441 0.0791011 11.3908 0.0593258 11.3464L0.0395506 11.3286L0.0197753 11.222L0 11.1066L0 11.0355L0 10.9645L0 10.8934L0.0197753 10.7868L0.0395506 10.6891L0.0593258 10.6536C0.0791011 10.6003 0.0889888 10.547 0.108764 10.5115L0.138427 10.4671L0.16809 10.4227C0.197753 10.3694 0.227416 10.325 0.266966 10.2895L0.286742 10.2362L0.326292 10.2095L0.346067 10.1829L0.385618 10.1296L0.425169 10.1118L11.2818 0.359709C11.8157 -0.119903 12.6661 -0.119903 13.2099 0.359709C13.7339 0.839322 13.7339 1.60315 13.2099 2.08276L4.65708 9.77432L20.6256 9.77432C21.3771 9.77432 22 10.325 22 11C22 11.675 21.3771 12.2257 20.6256 12.2257L4.65708 12.2257L13.2099 19.9084C13.7339 20.3969 13.7339 21.1696 13.2099 21.6403C12.6661 22.1199 11.8157 22.1199 11.2818 21.6403L0.385618 11.8615Z" id="Icon" fill="#203976" stroke="none" /></svg></button>')

class CustomAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com.br'})
        self.fields['username'].label = "Seu e-mail"
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'.  .  .  .  .  .  .  .  .  .  .'})
        self.fields['password'].label = "Senha"

class ClienteFormLead(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["nome","email"]
    def __init__(self, *args, **kwargs):
        super(ClienteFormLead, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})

class ClienteFormEspecial(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["nome","areatelefone","telefone"]
    def __init__(self, *args, **kwargs):
        super(ClienteFormEspecial, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})
        self.fields['areatelefone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['telefone'].widget.attrs.update({'class' : 'form-control'})


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["nome","sobrenome","telefone","areatelefone","cep","cpf","rua","nascimento","numero","bairro","complemento","cidade","estado",]
    nascimento = forms.DateField(
    widget=forms.DateInput(format='%d/%m/%Y'),
    input_formats=('%d/%m/%Y', )
    )
    cep = forms.CharField(widget=forms.TextInput)
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML("<p class='dash-title text-center'>Precisamos de mais alguns dados para finalizar sua compra</p>"),
            Field('nome', template="app/custom_components/textinput.html"),
            Field('sobrenome', template="app/custom_components/textinput.html"),
            Field('cpf', template="app/custom_components/textinput.html"),
            Field('nascimento', template="app/custom_components/textinput.html"),
            Field('areatelefone', template="app/custom_components/textinput.html"),
            Field('telefone', template="app/custom_components/textinput.html"),
            Field('cep', template="app/custom_components/textinput.html"),
            Field('rua', template="app/custom_components/textinput.html"),
            Field('numero', template="app/custom_components/textinput.html"),
            Field('bairro', template="app/custom_components/textinput.html"),
            Field('complemento', template="app/custom_components/textinput.html"),
            Field('cidade', template="app/custom_components/textinput.html"),
            Field('estado', template="app/custom_components/textinput.html"),
        )

class ClienteNovoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","email",]
    def clean(self):
        first_name = self.cleaned_data['first_name']
        email = self.cleaned_data['email']
        username = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'O email "%s" já esta em uso.' % username)
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ClienteNovoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].help_text = ''
        self.fields['first_name'].widget.attrs.update({'class' : 'textinput mt-2 mb-3','required':''})
        self.fields['email'].help_text = ''
        self.fields['email'].widget.attrs.update({'class' : 'textinput mt-2 mb-3'})


class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['dia']
    def __init__(self, *args, **kwargs):
        super(EntregaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            Field('dia', template="app/custom_components/checkbox.html"),
            footerHtml,
        )
class EntregaForm2(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['periodo',]
    def __init__(self, *args, **kwargs):
        super(EntregaForm2 , self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            Field('periodo', template="app/custom_components/checkbox.html"),
            footerHtml,
        )
class EntregaForm3(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ['preferencia','frequencia']
    def __init__(self, *args, **kwargs):
        super(EntregaForm3 , self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            # HTML('<div class="card"><div class="card-body"><p class="card-heading">Próxima entrega</p><p class="card-text">{{dia|join:", "}}</p><p class="card-text">{{periodo|join:", "}}</p></div></div>'),
            Field('preferencia', template="app/custom_components/radio.html"),
            Field('frequencia', template="app/custom_components/radio.html"),
            footerHtml,
        )
class SaboresForm(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ['sabores']
    def __init__(self, *args, **kwargs):
        super(SaboresForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('sabores', template="app/custom_components/multi-select.html"),
            footerHtml,
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
            Div(
                Div(
                    HTML(
                    '<p class="dash-title"><span style="font-weight:600">Olá</span> Humano,</p>'),
                    HTML('<p class="card-dash-subtitle" style="margin-top:-20px;font-size: min(3.5vw, 0.825em);white-space: nowrap;margin-bottom: -10px;">                    Caso tenha outro cão você pode inserir no final</p>'),
                    css_class="col-10 col-lg-6 d-flex flex-column mx-auto"),css_class="row"),
            Field('nome', placeholder="Digite aqui o nome do seu cão", template="app/custom_components/textinput.html"),
            Field('sexo', template="app/custom_components/radio.html"),
            footerHtml,
        )
        # self.fields['sexo'].widget.attrs.update({'newattr' : 'attrvalue'})

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
            goBackBtn,
            Field('castrado', template="app/custom_components/radio_unchecked.html"),
            Field('raca', placeholder="Digite aqui...", template="app/custom_components/textinput.html"),
            footerHtml,
        )

class CachorroForm3(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = [
            "nascimento",
        ]
    peso = forms.DecimalField(max_digits=3, min_value=1, decimal_places=1,initial='')
    pesoideal = forms.DecimalField(label = "Peso estimado do cachorro adulto", max_digits=3, decimal_places=1, initial='', required=False)
    def __init__(self, *args, **kwargs):
        super(CachorroForm3, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            Field('nascimento', placeholder="Mês / Ano", template="app/custom_components/textinput.html"),
            Field('peso', placeholder="Ex. 10,3kg", template="app/custom_components/textinput.html"),
            Field('pesoideal', placeholder="Ex. 10,3kg", template="app/custom_components/textinput.html"),
            footerHtml,
        )

class CachorroForm4 (forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["atividade",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm4, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            InlineRadios('atividade', template="app/custom_components/radio_sub.html"),
            footerHtml,
        )
class CachorroForm5(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = ["fisico",]
    def __init__(self, *args, **kwargs):
        super(CachorroForm5, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            Field('fisico', template="app/custom_components/radio.html"),
            footerHtml,
        )
class CachorroEspecialForm(forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = [
            "condicao",
            "medicamento",
            "descricao",
        ]
    def __init__(self, *args, **kwargs):
        super(CachorroEspecialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            goBackBtn,
            Field('condicao', template="app/custom_components/checkbox.html"),
            Field('medicamento', template="app/custom_components/radio.html"),
            Field('descricao', template="app/custom_components/textarea.html"),
            footerHtml,
        )
