from django.views import generic
from . import models
from . import forms


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
