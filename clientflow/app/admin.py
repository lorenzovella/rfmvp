from django.contrib import admin
from django import forms

from . import models


class CachorroEspecialAdminForm(forms.ModelForm):

    class Meta:
        model = models.CachorroEspecial
        fields = "__all__"


class CachorroEspecialAdmin(admin.ModelAdmin):
    form = CachorroEspecialAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]

class PlanosAdminForm(forms.ModelForm):

    class Meta:
        model = models.Planos
        fields = "__all__"


class PlanosAdmin(admin.ModelAdmin):
    form = PlanosAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]

class ClienteAdminForm(forms.ModelForm):

    class Meta:
        model = models.Cliente
        fields = "__all__"

class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm
    list_display = [
    "created",
    "last_updated",
    ]
    readonly_fields = [
    "created",
    "last_updated",
    ]

class EntregaAdminForm(forms.ModelForm):

    class Meta:
        model = models.Entrega
        fields = "__all__"


class EntregaAdmin(admin.ModelAdmin):
    form = EntregaAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]

class CachorroAdminForm(forms.ModelForm):

    class Meta:
        model = models.Cachorro
        fields = "__all__"


class CachorroAdmin(admin.ModelAdmin):
    form = CachorroAdminForm
    list_display = [
    "last_updated",
    "created",
    ]
    readonly_fields = [
    "last_updated",
    "created",
    ]


class PedidoAdminForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = "__all__"


class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]





admin.site.register(models.CachorroEspecial, CachorroEspecialAdmin)
admin.site.register(models.Planos, PlanosAdmin)
admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.Entrega, EntregaAdmin)
admin.site.register(models.Cachorro, CachorroAdmin)
admin.site.register(models.Pedido, PedidoAdmin)
