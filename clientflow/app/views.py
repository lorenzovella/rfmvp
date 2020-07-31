from . import forms
from . import models
from django.views import generic
from django.shortcuts import redirect, render
from django.forms.models import construct_instance
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login, authenticate
from clientflow.app.calculadora import calcularFator
from clientflow.app import pagseguro
from formtools.wizard.views import SessionWizardView
from decimal import Decimal
from datetime import date
from math import ceil
import uuid

precoKgRacao = 50

def handler404(request,exception):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response
def handler500(request):
    context = {}
    response = render(request, "500.html", context=context)
    response.status_code = 500
    return response
def errorView(request,e):
    return render(request,"error.html",{'erro':e})

def profile_view(request):
    username = None
    if request.user.is_authenticated == True:
        cliente = request.user.cliente
    return render(request, 'registration/profile.html', {'user':cliente})

def profile_update_view(request,carrinho=0):
    clienteInstance = models.User.objects.get(pk=request.user.id).cliente
    if request.method == "POST":
        form = forms.ClienteForm(request.POST, instance=clienteInstance)
        if form.is_valid():
            form.save()
            if carrinho is not 0:
                return redirect('clientflow_checkout', carrinho)
            return redirect('user-profile')
    else:
        form = forms.ClienteForm(instance=clienteInstance)
    return render(request, 'registration/edit_profile.html',{'form':form} )

def profile_simple_view(request, dog):
    if request.method == "POST":
        form = forms.ClienteNovoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            randPass = User.objects.make_random_password()
            user = form.save(commit=False)
            user.username = email
            user.set_password( randPass )
            user.save()
            user.refresh_from_db()
            dogInstance = models.Cachorro.objects.get(pk = dog)
            dogInstance.idCliente = user.cliente
            dogInstance.save()
            user.cliente.email = email
            user.cliente.nome = form.cleaned_data['first_name']
            user.save()
            user = authenticate(username=email, password=randPass)
            passReset = PasswordResetForm({'email': email})
            if passReset.is_valid():
                passReset.save(request=HttpRequest(), use_https=True)
            login(request, user)
            return redirect('clientflow_PlanoFlow', dog)
    elif request.user.is_authenticated == False:
        form = forms.ClienteNovoForm()
    elif request.user.is_authenticated == True:
        return redirect('clientflow_Cachorro_list')
    return render(request,'registration/sign_up.html',{'form':form,'dog':dog})

def dogdash(request):
    return render(request,'app/dogdash.html',{'user':request.user.cliente})

def fimDoFlow(request,carrinho):
    cart = models.Carrinho.objects.get(pk=carrinho)
    if cart.item.first().idClient == request.user.cliente:
        #pedidos = cart.item.all()
        return render(request, 'app/checkout_fimdoflow.html',{'pedido':cart.item.first().pk})
    return handler500(request)

def checkout(request,carrinho):
    cart = models.Carrinho.objects.get(pk=carrinho)
    valor = "{:.2f}".format( cart.get_valor_carrinho() )
    pedido = cart.item.first()
    pedidos = cart.item.all()
    if request.user.cliente == pedido.idClient:
        if request.method == "POST":
            card = request.POST
            session = pagseguro.criarSession()
            hash = pagseguro.criarHash(session,valor,card['number'].replace(" ",""),card['brand'],card['cvc'],card['expm'],card['expy'])
            cart.pagseguro_adesao = pagseguro.aderirPlano(cart.pagseguro_plano, carrinho, hash, card['name'], request.user.cliente)
            if type(cart.pagseguro_adesao) is dict:
                for pedido in pedidos:
                    pedido.status= 'Pedido em aberto'
                    pedido.observacoes = cart.pagseguro_adesao
                    pedido.save()
                return errorView(request, cart.pagseguro_adesao)
            else:
                for pedido in pedidos:
                    pedido.status = 'Pedido finalizado pelo cliente'
                    pedido.save()
            cart.save()
            return redirect('clientflow_fimDoFlow', carrinho)
            # cobranca = pagseguro.cobrarPlano(pedido.idClient.nome+" - "+ str(carrinho), cart.plano, valor, '1', str(carrinho), cart.pagseguro_adesao)
            # redirect('clientflow_Pedido_detail', carrinho)
        if request.user.cliente.cpf==0:
            return redirect('user-profile-update', carrinho)

        return render(request,"app/checkout_cartao.html",{'plano':cart.plano, 'valor': "{:.2f}".format(cart.get_valor_carrinho()) })
    else:
        return handler500(request)

def adicionarAoCarrinho(request):
    pedidos = models.Pedido.objects.filter(status ='Pedido em aberto', idClient = request.user.cliente)
    if pedidos.count() == 0:
        return errorView(request,"não foram encontrados pedidos em aberto")

    newCarrinho = models.Carrinho()

    strPlano = "Pedido para o "
    for pedido in pedidos:
        strPlano += pedido.idDog.nome +", "
    strPlano = strPlano[:-2]

    newCarrinho.plano = strPlano
    savedCarrinho = newCarrinho.save()

    for pedido in pedidos:
        pedido.idCarrinho = newCarrinho
        pedido.save()

    valor = "{:.2f}".format( newCarrinho.get_valor_carrinho() )
    codigoPlano = pagseguro.criarPlano(strPlano,str(newCarrinho.pk),str(valor))
    newCarrinho.pagseguro_plano = codigoPlano['pg']
    savedCarrinho = newCarrinho.save()

    if request.user.cliente.cpf==0:
        return redirect('user-profile-update', newCarrinho)
    return redirect('clientflow_checkout', newCarrinho)


class CachorroEspecialListView(generic.ListView):
    model = models.CachorroEspecial
    form_class = forms.CachorroEspecialForm


class CachorroEspecialCreateView(generic.CreateView):
    model = models.CachorroEspecial
    form_class = forms.CachorroEspecialForm


class CachorroEspecialDetailView(generic.DetailView):
    model = models.CachorroEspecial
    form_class = forms.CachorroEspecialForm


class CachorroEspecialUpdateView(generic.UpdateView):
    model = models.CachorroEspecial
    form_class = forms.CachorroEspecialForm
    pk_url_kwarg = "pk"


class EntregaListView(generic.ListView):
    model = models.Entrega
    form_class = forms.EntregaForm


class EntregaCreateView(generic.CreateView):
    model = models.Entrega
    form_class = forms.EntregaForm


class EntregaDetailView(generic.DetailView):
    model = models.Entrega
    form_class = forms.EntregaForm


class EntregaUpdateView(generic.UpdateView):
    model = models.Entrega
    form_class = forms.EntregaForm
    pk_url_kwarg = "pk"

class PedidoListView(generic.ListView):
    def get_queryset(self):
        return self.model.objects.filter(idClient = self.request.user.cliente).exclude(status ='Pedido em aberto')
    model = models.Pedido
    form_class = forms.PedidoForm

class CarrinhoListView(generic.ListView):
    template_name = "app/carrinho_list.html"
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() == 0:
            return redirect('clientflow_Cachorro_list')
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        return models.Pedido.objects.filter(status ='Pedido em aberto', idClient = self.request.user.cliente)

    model = models.Pedido
    form_class = forms.PedidoForm



class PedidoCreateView(generic.CreateView):
    model = models.Pedido
    form_class = forms.PedidoForm


class PedidoDetailView(generic.DetailView):
    model = models.Pedido
    form_class = forms.PedidoForm


class PedidoUpdateView(generic.UpdateView):
    model = models.Pedido
    form_class = forms.PedidoForm
    pk_url_kwarg = "pk"

def PedidoFlow(request, plano, dog):
    try:
        instance = models.Pedido()
        plano = models.Plano.objects.get(pk=plano)
        dog = models.Cachorro.objects.get(pk=dog)
        instance.idPlano = plano
        instance.idDog = dog
        instance.valor = precoKgRacao * plano.refeicoes * dog.calculodia / 1000
        savedInstance = instance.save()
        return redirect('clientflow_EntregaFlow', pedido = instance)
    except Exception as e:
        return errorView(request, e)

FORMS_PEDIDO = [
    ("Sabores", forms.SaboresForm),
    ("Entrega", forms.EntregaForm),
    ("Entrega - 2", forms.EntregaForm2),
    ("Entrega - 3", forms.EntregaForm3),
    ]
TEMPLATES_PEDIDO = {
    "Sabores": "app/pedido_multipageform.html",
    "Entrega": "app/pedido_multipageform.html",
    "Entrega - 2": "app/pedido_multipageform.html",
    "Entrega - 3": "app/pedido_multipageform.html",
    }

class pedidoWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES_PEDIDO[self.steps.current]]
    def get_context_data(self, form, **kwargs):
        context = super(pedidoWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == "Entrega - 3":
            data_entrega = self.get_cleaned_data_for_step('Entrega') # zero indexed
            data_entrega2 = self.get_cleaned_data_for_step('Entrega - 2') # zero indexed
            context.update( { 'dia': data_entrega['dia'], 'periodo' : data_entrega2['periodo'] })
        return context
    def done(self, form_list, form_dict, **kwargs):
        pedidoInstance = models.Pedido.objects.get(pk=self.kwargs['pedido'])
        # salva entrega
        entregaInstance = models.Entrega()
        entregaFormArray = [
            form_dict['Entrega'].cleaned_data,
            form_dict['Entrega - 2'].cleaned_data,
            form_dict['Entrega - 3'].cleaned_data,
            ]
        for parsedForms in entregaFormArray:
            for key, value in parsedForms.items():
                setattr(entregaInstance, key, value)
        savedEntrega = entregaInstance.save()
        pedidoInstance.idEntrega = entregaInstance
        # salva sabores
        saboresForm = form_dict['Sabores'].cleaned_data
        pedidoInstance.sabores = saboresForm['sabores']
        # relaciona usuario ao pedido
        pedidoInstance.idClient = self.request.user.cliente
        # salva pedido
        savedPedido = pedidoInstance.save()
        return redirect('clientflow_Carrinho_list')

def PlanoFlow(request, pk):
    try:
        instance = models.Cachorro.objects.get(pk=pk)
    except models.Cachorro.DoesNotExist:
        return handler500(request)
    planos = models.Plano.objects.all()
    for obj in planos:
        setattr(obj, "valor", "{:.2f}".format( precoKgRacao/1000 * obj.refeicoes * float(instance.calculodia)  )  )
        setattr(obj, "valordia", "{:.2f}".format( float(obj.valor)/float(30) ) )

    return render(request,'app/plano_list.html',{'planos':planos,'dog':instance})



class PlanoListView(generic.ListView):
    model = models.Plano
    form_class = forms.PlanoForm


class PlanoCreateView(generic.CreateView):
    model = models.Plano
    form_class = forms.PlanoForm


class PlanoDetailView(generic.DetailView):
    model = models.Plano
    form_class = forms.PlanoForm


class PlanoUpdateView(generic.UpdateView):
    model = models.Plano
    form_class = forms.PlanoForm
    pk_url_kwarg = "pk"


class CachorroListView(generic.ListView):
    def get_queryset(self):
        return self.model.objects.filter(idCliente = self.request.user.cliente)
    model = models.Cachorro
    form_class = forms.CachorroForm

class CachorroListFlowView(generic.ListView):
    def get_queryset(self):
        return self.model.objects.filter(idCliente = self.request.user.cliente)
    template_name = "app/cachorroflow_list.html"
    model = models.Cachorro
    form_class = forms.CachorroForm


class CachorroCreateView(generic.CreateView):
    model = models.Cachorro
    form_class = forms.CachorroForm


class CachorroDetailView(generic.DetailView):
    model = models.Cachorro
    form_class = forms.CachorroForm


class CachorroUpdateView(generic.UpdateView):
    model = models.Cachorro
    form_class = forms.CachorroForm
    pk_url_kwarg = "pk"

def CachorroDeleteConfirmView(request, pk):
    try:
        instance = models.Cachorro.objects.get(pk=pk)
    except models.Cachorro.DoesNotExist:
        return handler500(request)
    return render(request,'app/cachorro_delete_confirm.html',{'obj':instance })

def CachorroDeleteView(request, pk):
    try:
        instance = models.Cachorro.objects.get(pk=pk)
        info = instance.delete()
    except models.Cachorro.DoesNotExist:
        return handler500(request)
    return render(request,'app/cachorro_delete.html',{'info':info })

def PedidoDeleteConfirmView(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/pedido_delete_confirm.html',{'obj':instance })

def PedidoDeleteView(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
        if instance.status == "Pedido em aberto":
            info = instance.delete()
        else:
            return handler500(request)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/pedido_delete.html',{'info':info })



FORMS_CACHORRO = [
    ("CachorroForm", forms.CachorroForm),
    ("CachorroForm2", forms.CachorroForm2),
    ("CachorroForm3", forms.CachorroForm3),
    ("CachorroForm4", forms.CachorroForm4),
    ("CachorroForm5", forms.CachorroForm5),
    ("CachorroEspecialForm", forms.CachorroEspecialForm),
    ]
TEMPLATES_CACHORRO = {
    "CachorroForm": "app/cachorro_multipageform.html",
    "CachorroForm2": "app/cachorro_multipageform.html",
    "CachorroForm3": "app/cachorro_multipageform.html",
    "CachorroForm4": "app/cachorro_multipageform.html",
    "CachorroForm5": "app/cachorro_multipageform.html",
    "CachorroEspecialForm": "app/cachorroespecial_multipageform.html",
    }

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class cachorroWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES_CACHORRO[self.steps.current]]
    def done(self, form_list, form_dict, **kwargs):
        cachorroInstance = models.Cachorro()
        cachorroFormArray = [
            form_dict['CachorroForm'].cleaned_data,
            form_dict['CachorroForm2'].cleaned_data,
            form_dict['CachorroForm3'].cleaned_data,
            form_dict['CachorroForm4'].cleaned_data,
            form_dict['CachorroForm5'].cleaned_data,
            ]
        for parsedForms in cachorroFormArray:
            for key, value in parsedForms.items():
                 setattr(cachorroInstance, key, value)
        dogEspecial = form_dict['CachorroEspecialForm'].cleaned_data
        if(dogEspecial):
            dogEspecialInstance = models.CachorroEspecial()
            for key, value in dogEspecial.items():
                setattr(dogEspecialInstance,key,value)
            savedDogEspecial = dogEspecialInstance.save()
            cachorroInstance.dogEspecial = dogEspecialInstance
        # calculo filhote
        if(calculate_age(cachorroInstance.nascimento) < 1):
            gramaspordia = round( 416*(float(cachorroInstance.peso)**0.75)*(2.718**(-0.87*float(cachorroInstance.peso/cachorroInstance.pesoideal))-0.1) )
            kgpormes = ceil( gramaspordia * 0.028 )
        # calculo dog adulto
        else:
            fator = calcularFator(cachorroInstance.atividade, cachorroInstance.nascimento, cachorroInstance.fisico, cachorroInstance.castrado)
            gramaspordia = round(fator * 0.63 * (float(cachorroInstance.peso) ** 0.75  ) )
            kgpormes = ceil( gramaspordia * 0.028 )
        cachorroInstance.calculodia = Decimal.from_float(gramaspordia)
        cachorroInstance.calculomes = Decimal(kgpormes)

        if self.request.user.is_authenticated:
            cachorroInstance.idCliente = self.request.user.cliente
            savedCachorro = cachorroInstance.save()
            return redirect('clientflow_PlanoFlow', cachorroInstance)
        savedCachorro = cachorroInstance.save()
        return redirect('user-profile-simple', dog = cachorroInstance)
        # self.instance_dict = None
        # self.storage.reset()

class ClienteListView(generic.ListView):
    model = models.Cliente
    form_class = forms.ClienteForm


class ClienteCreateView(generic.CreateView):
    model = models.Cliente
    form_class = forms.ClienteForm


class ClienteDetailView(generic.DetailView):
    model = models.Cliente
    form_class = forms.ClienteForm


class ClienteUpdateView(generic.UpdateView):
    model = models.Cliente
    form_class = forms.ClienteForm
    pk_url_kwarg = "pk"
