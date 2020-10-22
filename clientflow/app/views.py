import pytz
import datetime
import pendulum
from . import forms
from . import models
from django import forms as djangoforms
from django.db import IntegrityError
from django.views import generic
from django.http import HttpRequest
from django.http import HttpResponse
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
from math import ceil
from ipware import get_client_ip
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon
from schedule.models.events import Event
from schedule.models.rules import Rule
from schedule.models.calendars import Calendar
from . import messagingHandler
from . import rd
class newPasswordResetForm(PasswordResetForm):
    def send_mail(self, *args, **kwargs):
        super().send_mail(*args, **kwargs)


def calculaDescontoProgressivo(consumoKg):
    consumoKg = float(consumoKg)
    precoKg = 55
    if consumoKg < 4 :
        #         #número de vezes a    # % de desconto
        #         #aplicar o desconto   # a cada 100g
        desconto = ( consumoKg - 1 ) * 0.07
    if consumoKg >= 4 and consumoKg < 5:
        desconto = 0.203 + (( consumoKg - 4 ) * 0.055)
    if consumoKg >= 5 and consumoKg < 5.5:
        desconto = 0.26 + (( consumoKg - 5 ) * 0.04)
    if consumoKg >= 5.5 and consumoKg < 9.5:
        desconto = 0.29 + (( consumoKg - 5.5 ) * 0.03)
    if consumoKg >= 9.5 and consumoKg < 12.5:
        desconto = 0.41 + (( consumoKg - 9.5 ) * 0.02)
    if consumoKg >= 12.5:
        desconto = 0.47 + (( consumoKg - 12.5 ) * 0.01)
    desconto = min(desconto,0.5)
    # retorna valor do Kg com desconto aplicado
    return (precoKg*(1-desconto))

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
def errorViewCarrinho(request,e,carrinho):
    return render(request,"error_carrinho.html",{'erro':e, 'carrinho':carrinho})

def profile_view(request):
    username = None
    if request.user.is_authenticated == True:
        cliente = request.user.cliente
    return render(request, 'registration/profile.html', {'user':cliente})

def profile_update_view(request,carrinho=0):
    if request.user.is_authenticated:
        clienteInstance = request.user.cliente
    else:
        clienteInstance = models.Cliente.objects.get(pk = request.session['cliente'])
    if request.method == "POST":
        form = forms.ClienteForm(request.POST, instance=clienteInstance)
        if form.is_valid():
            form.save()
            if carrinho != 0:
                return redirect('clientflow_checkout', carrinho)
            return redirect('user-profile')
    else:
        form = forms.ClienteForm(instance=clienteInstance)
    return render(request, 'registration/edit_profile.html',{'form':form} )

def profile_simple_view(request, pedido, dog):
    if request.method == "POST":
        form = forms.ClienteFormLead(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            nome = form.cleaned_data.get('nome')
            savedInstance = form.save()
            request.session['cliente'] = savedInstance.pk
            dogInstance = models.Cachorro.objects.get(pk = dog)
            dogInstance.idCliente = savedInstance
            dogInstance.save()
            pedidoInstance = models.Pedido.objects.get(pk = pedido)
            pedidoInstance.idClient = savedInstance
            pedidoInstance.save()
            return redirect('clientflow_Carrinho_list')
    elif request.user.is_authenticated == False:
        form = forms.ClienteFormLead()
    elif request.user.is_authenticated == True:
        return redirect('clientflow_Cachorro_list')
    return render(request,'registration/sign_up.html',{'form':form,'dog':dog})

def profile_cliente_especial(request, dog):
    if request.method == "POST":
        form = forms.ClienteFormEspecial(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            nome = form.cleaned_data.get('nome')
            savedInstance = form.save()
            request.session['cliente'] = savedInstance.pk
            dogInstance = models.Cachorro.objects.get(pk = dog)
            dogInstance.idCliente = savedInstance
            dogInstance.save()
            return redirect('clientflow_dogespecial', dogInstance)
    form = forms.ClienteFormEspecial()
    return render(request,'registration/sign_up.html',{'form':form,'dog':dog})

def IndexView(request):
    if request.user.is_authenticated:
        return redirect('dogdash')
    return render(request,'index.html')

def ra(request):
    return render(request, 'ra/index.html')

def calendar(request):
    return render(request, 'app/fullcalendar.html')

def entregaInterna(request, pedido):
    pedido = models.Pedido.objects.get(pk=pedido)
    return render(request, 'app/entrega_interna.html', {'object':pedido} )

def dogdash(request):
    dogCount = models.Cachorro.objects.filter(idCliente = request.user.cliente).count()
    carrinho = models.Carrinho.objects.filter(item__idClient = request.user.cliente).filter(pagseguro_adesao__exact='').last()
    pedido = models.Pedido.objects.filter(status ='Pedido finalizado pelo cliente').last()
    if pedido:
        entrega = Event.objects.get(url = pedido.pk).occurrences_after(datetime.datetime.now(), pytz.timezone('America/Sao_Paulo'), 1)
    else:
        entrega = ""
    hora = "14:00"
    # return render(request,'app/dogdash.html',{'user':request.user.cliente,'dogcount':dogCount, 'carrinho':carrinho, 'entrega':entrega.__next__(), 'hora':hora})
    return render(request,'app/dogdash.html',{'user':request.user.cliente,'dogcount':dogCount, 'carrinho':carrinho, 'entrega':entrega.start.date, 'hora':str(entrega.start.time().hour-3) +"h e "+str(entrega.end.time().hour-3)+"h" })

def pedidosDash(request):
    pedidos = models.Pedido.objects.filter(status ='Pedido finalizado pelo cliente')
    return render(request,'app/listagem_interna.html',{'pedidos':pedidos})

def fimDoFlow(request,carrinho):
    cart = models.Carrinho.objects.get(pk=carrinho)
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        cliente = models.Cliente.objects.get(pk = request.session['cliente'])
        if cart.item.first().idClient == cliente:
            return render(request, 'app/checkout_fimdoflow_conflict.html',{'pedido':cart.item.first().pk})
    if cart.item.first().idClient == cliente:
        #pedidos = cart.item.all()
        return render(request, 'app/checkout_fimdoflow.html',{'pedido':cart.item.first().pk})
    return handler500(request)

def fimDoFlowEspecial(request,dog):
    cachorro = models.Cachorro.objects.get(pk=dog)
    cliente = cachorro.idCliente
    number = str(cliente.areatelefone)+str(cliente.telefone)
    msg = str("Olá! Agradecemos seu interesse no Ração do Futuro! Já estamos com os dados do seu doguinho, "+cachorro.nome+". Como você nos contou que ele é um dog especial, para garantir que ele poderá consumir a Ração do Futuro com segurança, precisamos antes consultar nossos especialistas caninos! Em até dois dias úteis voltaremos a entrar em contato com sua dieta. 🐶")
    messagingHandler.sendMessageT("Um novo dog especial foi cadastrado na platafoma.")
    messagingHandler.sendMessageW(msg, number)
    return render(request, 'app/dogespecial.html')

def listagemteste(request):
    eventosAtivos = Event.objects.values('url')
    pedidosAtivos = models.Pedido.objects.filter(pk__in = eventosAtivos)
    return render(request, 'app/listagem_teste.html',{'lista':pedidosAtivos})

def checkout(request,carrinho):
    cart = models.Carrinho.objects.get(pk=carrinho)
    valor = "{:.2f}".format( cart.get_valor_carrinho() )
    pedido = cart.item.first()
    pedidos = cart.item.all()
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        cliente = models.Cliente.objects.get(pk = request.session['cliente'])
    if cliente == pedido.idClient:
        if request.method == "POST":
            card = request.POST
            session = pagseguro.criarSession()
            hash = pagseguro.criarHash(session,valor,card['number'].replace(" ",""),card['brand'],card['cvc'],card['expm'],card['expy'])
            cart.pagseguro_adesao = pagseguro.aderirPlano(cart.pagseguro_plano, carrinho, hash, card['name'], cliente, get_client_ip(request)[0])
            if type(cart.pagseguro_adesao) is dict:
                for pedido in pedidos:
                    pedido.status= 'Pedido em aberto'
                    pedido.observacoes = cart.pagseguro_adesao
                    pedido.save()
                return errorViewCarrinho(request, cart.pagseguro_adesao, carrinho)
            else:
                for pedido in pedidos:
                    pedido.status = 'Pedido finalizado pelo cliente'
                    pedido.save()
            cart.save()
            send_mail(render_to_string(template_name='email/checkout_subject.txt', context={'dog':pedido.idDog.nome,'pedido':pedido}).strip(),
                render_to_string(template_name='email/checkout_plain.txt', context={'pedido':pedido}).strip(),
                None,
                [pedido.idClient.email],
                html_message = render_to_string(template_name='email/checkout.html')
            )
            saveuser(request, cliente, pedido, pedido.idDog, carrinho)
            saveentrega(pedidos)
            rd.criarLead(cliente, cart.pagseguro_plano)
            return redirect('clientflow_fimDoFlow', carrinho)
        if cliente.cpf=="":
            return redirect('user-profile-update', carrinho)
        return render(request,"app/checkout_cartao.html",{'plano':cart.plano, 'carrinho':cart,'valor': "{:.2f}".format(cart.get_valor_carrinho()), 'desconto': "{:.2f}".format(cart.get_valor_desconto()), 'frete': "{:.2f}".format(cart.get_valor_frete()), 'pedidos':pedidos.count() })
    else:
        return handler500(request)

def saveuser(request, cliente, pedido, dog, carrinho):
    randPass = User.objects.make_random_password()
    try:
        user = User.objects.create_user(cliente.email,cliente.email, randPass)
        user.save()
    except IntegrityError as e:
        doubledUser = models.User.objects.get(username=cliente.email)
        try:
            oldClient = models.Cliente.objects.get(user=doubledUser)
            oldClient.user = None
            oldClient.save()
        finally:
            cliente.user = doubledUser
            cliente.save()
            passReset = newPasswordResetForm({'email': cliente.email})
            if passReset.is_valid():
                passReset.save(request=request, use_https=True, email_template_name='email/boas_vindas_plain.html', html_email_template_name='email/boas_vindas.html')
            return redirect('clientflow_fimDoFlow', carrinho)
    cliente.user = user
    cliente.save()
    user = authenticate(username=cliente.email, password=randPass)
    login(request, user)
    passReset = newPasswordResetForm({'email': cliente.email})
    if passReset.is_valid():
        passReset.save(request=request, use_https=True, email_template_name='email/boas_vindas_plain.html', html_email_template_name='email/boas_vindas.html')

def saveentrega(pedidos):
    for pedido in pedidos:
        weekdayDict = {'Segunda':pendulum.MONDAY,'Terça':pendulum.TUESDAY,'Quarta':pendulum.WEDNESDAY,'Quinta':pendulum.THURSDAY,'Sexta':pendulum.FRIDAY,'Sábado':pendulum.SATURDAY}

        entrega = pedido.idEntrega

        periodo = str(entrega.periodo).split(', ')[-1]
        dia = str(entrega.dia).split(', ')
        diaMap = list(map(lambda x: weekdayDict[x], dia))

        firstEntrega = None
        dt = pendulum.tomorrow()
        while firstEntrega == None:
            if dt.day_of_week in diaMap:
                firstEntrega = dt
            else:
                dt = dt.add(days=1)

        startDict = {"Matutino":8,"Vespertino":12,"Noturno":18}
        start = firstEntrega.replace(hour=startDict[periodo], minute=0)

        endDict = {"Matutino":12,"Vespertino":18,"Noturno":22}
        end = firstEntrega.replace(hour=endDict[periodo], minute=0)

        title = "Pedido "+str(pedido)
        calendar = Calendar.objects.get(pk=1)
        rule = Rule.objects.get(pk = entrega.frequencia)

        event = Event(start=start, end=end, title=title, rule=rule, calendar=calendar, url=str(pedido))
        event.save()

def adicionarAoCarrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedidos = models.Pedido.objects.filter(status ='Pedido em aberto', idClient = cliente)
    else:
        cliente = models.Cliente.objects.get(pk = request.session['cliente'])
        pedidos = models.Pedido.objects.filter(idClient = cliente).filter(status ='Pedido em aberto')
    if pedidos.count() == 0:
        try:
            lastCarrinho = models.Carrinho.objects.filter(item__idClient = cliente).last()
            return redirect('clientflow_checkout', lastCarrinho)
        except models.Carrinho.DoesNotExist:
            return errorView(request, "não foram encontrados pedidos em aberto")

    newCarrinho = models.Carrinho()

    strPlano = "Pedido para o "
    for pedido in pedidos:
        strPlano += pedido.idDog.nome +", "
        pedido.status = 'Carrinho criado'
        pedido.save()
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

    if cliente.cpf == "":
        return redirect('user-profile-update', newCarrinho)
    return redirect('clientflow_checkout', newCarrinho)

def testaCupom(request):
    if request.user.is_authenticated:
        user = request.user.cliente
    else:
        user = models.Cliente.objects.get(pk = request.session['cliente'])
    if request.method == 'GET':
            cupom = request.GET['cupom']
            carrinho = request.GET['carrinho']
            status = validate_coupon(coupon_code=cupom, user=user)
            if status['valid']:
                coupon = Coupon.objects.get(code=cupom)
                descontoResponse = aplicaDesconto(coupon, carrinho, user)
                return HttpResponse(descontoResponse) # Sending an success response
            return HttpResponse(status['message'])
    else:
            return HttpResponse("Request method is not a GET")

def aplicaDesconto(coupon, carrinho, user):
    instance = models.Carrinho.objects.get(pk = carrinho)
    instance.cupom = coupon.code
    instance.save()
    novoValor = "{:.2f}".format( instance.get_valor_carrinho() )
    try:
        pagseguro.descontoPlano(instance.pagseguro_plano,novoValor)
    except:
        return "Erro ao aplicar desconto!"
    coupon.use_coupon(user=user)
    return "{:.2f}".format( instance.get_valor_desconto() )

class PlanoListView(generic.ListView):
    model = models.Plano
    form_class = forms.PlanoForm

class PedidoListView(generic.ListView):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() == 0:
            return redirect('dogdash')
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        return self.model.objects.filter(idClient = self.request.user.cliente).filter(status ='Pedido finalizado pelo cliente')
    model = models.Pedido
    form_class = forms.PedidoForm

class CarrinhoListView(generic.ListView):
    template_name = "app/carrinho_list.html"
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        if self.request.user.is_authenticated:
            client = self.request.user.cliente
            return models.Pedido.objects.filter(idClient = client).filter(status ='Pedido em aberto')
        elif 'cliente' in self.request.session:
            return models.Pedido.objects.filter(idClient = self.request.session['cliente']).filter(status ='Pedido em aberto')
        else:
            return redirect('index')
    model = models.Pedido
    form_class = forms.PedidoForm

class CarrinhoListView2(generic.ListView):
    template_name = "app/carrinho_list2.html"
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        if self.request.user.is_authenticated:
            client = self.request.user.cliente
            return models.Pedido.objects.filter(idClient = client).filter(status ='Pedido em aberto')
        elif 'cliente' in self.request.session:
            return models.Pedido.objects.filter(idClient = self.request.session['cliente']).filter(status ='Pedido em aberto')
        else:
            return redirect('index')
    model = models.Pedido
    form_class = forms.PedidoForm


class PagtoDetailView(generic.DetailView):
    template_name = "app/pagto_detail.html"
    model = models.Pedido
    form_class = forms.PedidoForm

def PlanoFlow(request, dog):
    try:
        instance = models.Cachorro.objects.get(pk=dog)
    except models.Cachorro.DoesNotExist:
        return handler500(request)
    planos = models.Plano.objects.all()
    for obj in planos:
        precoKgRacao = calculaDescontoProgressivo( float(instance.calculomes) * float(obj.refeicoes/28) )
        valorPlano = max((precoKgRacao * obj.refeicoes * float(instance.calculomes)/28)*0.9 + 15,70)
        setattr(obj, "valor", "{:.2f}".format( valorPlano )  )
        setattr(obj, "valordia", "{:.2f}".format( float(valorPlano)/float(obj.refeicoes) ) )

    return render(request,'app/plano_list.html',{'planos':planos,'dog':instance})

def PedidoFlow(request, plano, dog):
    try:
        instance = models.Pedido()
        plano = models.Plano.objects.get(pk=plano)
        dog = models.Cachorro.objects.get(pk=dog)
        instance.idPlano = plano
        instance.idDog = dog
        precoKgRacao = calculaDescontoProgressivo(  float(dog.calculomes)  * float(plano.refeicoes/28) )
        instance.valor = max((precoKgRacao * plano.refeicoes * float(dog.calculomes)/28)*0.9 + 15,70)
        savedInstance = instance.save()
        return redirect('clientflow_EntregaFlow', pedido = instance)
    except Exception as e:
        return errorView(request, e)

FORMS_ENTREGA = [
    ("Entrega", forms.EntregaForm),
    ("Entrega - 2", forms.EntregaForm2),
    ("Entrega - 3", forms.EntregaForm3),
    ]
TEMPLATES_ENTREGA = {
    "Entrega": "app/pedido_multipageform.html",
    "Entrega - 2": "app/pedido_multipageform.html",
    "Entrega - 3": "app/pedido_multipageform.html",
    }

class entregaWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES_ENTREGA[self.steps.current]]
    def get_context_data(self, form, **kwargs):
        context = super(entregaWizard, self).get_context_data(form=form, **kwargs)
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
        # relaciona usuario ao pedido
        if self.request.user.is_authenticated:
            pedidoInstance.idClient = self.request.user.cliente
            # salva pedido
            savedPedido = pedidoInstance.save()
            return redirect('clientflow_Carrinho_list')
        elif 'cliente' in self.request.session:
            pedidoInstance.idClient = models.Cliente.objects.get(pk = self.request.session['cliente'])
            savedPedido = pedidoInstance.save()
            return redirect('clientflow_Carrinho_list')
        savedPedido = pedidoInstance.save()
        return redirect('user-profile-simple', pedido = pedidoInstance, dog = pedidoInstance.idDog)

class CachorroListView(generic.ListView):
    def get_queryset(self):
        return self.model.objects.filter(idCliente = self.request.user.cliente)
    model = models.Cachorro
    form_class = forms.CachorroForm


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

def CarrinhoDeleteConfirmView(request, pk):
    try:
        instance = models.Carrinho.objects.get(pk=pk)
    except models.Carrinho.DoesNotExist:
        return handler500(request)
    return render(request,'app/carrinho_delete_confirm.html',{'obj':instance })

def CarrinhoDeleteView(request, pk):
    try:
        instance = models.Carrinho.objects.get(pk=pk)
        if(instance.item.first().idClient == request.user.cliente):
            info = instance.delete()
        else:
            return handler500(request)
    except models.Carrinho.DoesNotExist:
        return handler500(request)
    return render(request,'app/carrinho_delete.html',{'info':info })

def suspendePlanoConfirm(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/suspende_pg_confirm.html',{'obj':instance })

def suspendePlano(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
        info = pagseguro.suspendePlano(instance.idCarrinho.pagseguro_adesao)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/suspende_pg.html',{'info':info })

def cancelaPlanoConfirm(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/cancela_pg_confirm.html',{'obj':instance })

def cancelaPlano(request, pk):
    try:
        instance = models.Pedido.objects.get(pk=pk)
        info = pagseguro.cancelaPlano(instance.idCarrinho.pagseguro_adesao)
    except models.Pedido.DoesNotExist:
        return handler500(request)
    return render(request,'app/cancela_pg.html',{'info':info })



FORMS_CACHORRO = [
    ("CachorroForm", forms.CachorroForm),
    ("CachorroForm2", forms.CachorroForm2),
    ("CachorroForm3", forms.CachorroForm3),
    ("CachorroForm4", forms.CachorroForm4),
    ("CachorroForm5", forms.CachorroForm5),
    ("CachorroEspecialForm", forms.CachorroEspecialForm),
    ("Sabores", forms.SaboresForm),
    ]
TEMPLATES_CACHORRO = {
    "CachorroForm": "app/cachorro_multipageform.html",
    "CachorroForm2": "app/cachorro_multipageform.html",
    "CachorroForm3": "app/cachorro_multipageform.html",
    "CachorroForm4": "app/cachorro_multipageform.html",
    "CachorroForm5": "app/cachorro_multipageform.html",
    "CachorroEspecialForm": "app/cachorroespecial_multipageform.html",
    "Sabores": "app/cachorro_multipageform.html",
    }

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
        if(dogEspecial['condicao']):
            dogEspecialInstance = models.CachorroEspecial()
            for key, value in dogEspecial.items():
                setattr(dogEspecialInstance,key,value)
            savedDogEspecial = dogEspecialInstance.save()
            cachorroInstance.dogEspecial = dogEspecialInstance
            saboresForm = form_dict['Sabores'].cleaned_data
            cachorroInstance.sabores = saboresForm['sabores']
            savedCachorro = cachorroInstance.save()
            return redirect('user-profile-especial', cachorroInstance)

        # calculo filhote
        if cachorroInstance.calculate_age() < 1:
            kcalpordia = round( 416*(float(cachorroInstance.peso)**0.75)*(2.718**(-0.87*float(cachorroInstance.peso/cachorroInstance.pesoideal))-0.1) )
            gramaspordia = float(kcalpordia) / float(1.5859)
            kgpormes = max(1,ceil( gramaspordia * 0.028 ))
        # calculo dog adulto
        else:
            fator = calcularFator(cachorroInstance.atividade, cachorroInstance.nascimento, cachorroInstance.fisico, cachorroInstance.castrado)
            gramaspordia = round(fator * 0.63 * (float(cachorroInstance.peso) ** 0.75  ) )
            kgpormes = max(1,ceil( gramaspordia * 0.028 ))
        cachorroInstance.calculodia = Decimal.from_float(gramaspordia)
        cachorroInstance.calculomes = Decimal(kgpormes)
        # salva sabores
        saboresForm = form_dict['Sabores'].cleaned_data
        cachorroInstance.sabores = saboresForm['sabores']
        # salva cliente
        if self.request.user.is_authenticated:
            cachorroInstance.idCliente = self.request.user.cliente
        elif 'cliente' in self.request.session:
            cachorroInstance.idCliente = clienteInstance = models.Cliente.objects.get(pk = self.request.session['cliente'])
        savedCachorro = cachorroInstance.save()
        return redirect('clientflow_PlanoFlow', cachorroInstance)
