from django.views import generic
from . import models
from . import forms
from django.shortcuts import redirect, render
from django.forms.models import construct_instance
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage


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
        instance.dog = dog
        instance.valor = dog.calculodia * plano.refeicoes
        savedInstance = instance.save()
        return redirect('clientflow_EntregaFlow', pedido = instance)
    except Exception as e:
        return errorView(request, e)

FORMS_PEDIDO = [
    ("Entrega", forms.EntregaForm),
    ]
TEMPLATES_PEDIDO = {
    "Entrega": "app/pedido_multipageform.html",
    }
class pedidoWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES_PEDIDO[self.steps.current]]
    def done(self, form_list, form_dict, **kwargs):
        pedidoInstance = models.Pedido.objects.get(self.pedido)
        return redirect('clientflow_Pedido_detail', pk = pedidoInstance)


def PlanoFlow(request, pk):
    try:
        instance = models.Cachorro.objects.get(pk=pk)
    except models.Cachorro.DoesNotExist:
        return handler500(request)
    planos = models.Plano.objects.all
    valorMes = instance.calculomes
    valorDia = instance.calculodia
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
    model = models.Cachorro
    form_class = forms.CachorroForm

class CachorroListFlowView(generic.ListView):
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
# INSTANCE_DICT = {
#     }

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
        savedCachorro = cachorroInstance.save()
        tempReq = cachorroInstance
        # self.instance_dict = None
        # self.storage.reset()
        return redirect('clientflow_CachorroFlow_list')


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
