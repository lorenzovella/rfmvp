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


class PlanosListView(generic.ListView):
    model = models.Planos
    form_class = forms.PlanosForm


class PlanosCreateView(generic.CreateView):
    model = models.Planos
    form_class = forms.PlanosForm


class PlanosDetailView(generic.DetailView):
    model = models.Planos
    form_class = forms.PlanosForm


class PlanosUpdateView(generic.UpdateView):
    model = models.Planos
    form_class = forms.PlanosForm
    pk_url_kwarg = "pk"


class CachorroListView(generic.ListView):
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
    instance = models.Cachorro.objects.get(pk=pk)
    return render(request,'app/cachorro_delete_confirm.html',{'obj':instance })

def CachorroDeleteView(request, pk):
    instance = models.Cachorro.objects.get(pk=pk)
    # if(instance.Name == request.user):
    info = instance.delete()
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
    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form=form, **kwargs)
    #     if self.steps.current == "1":
    #         context.update({'step_subheading': "", "step_label": "Class details",})
    #     return context

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
        savedCachorro = cachorroInstance.save()
        tempReq = cachorroInstance
        # self.instance_dict = None
        # self.storage.reset()
        return redirect('clientflow_Cachorro_list')


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
