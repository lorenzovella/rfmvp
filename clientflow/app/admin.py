from django.contrib import admin
from django import forms

from . import models

class ClienteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = "__all__"
class CachorroAdminForm(forms.ModelForm):
    class Meta:
        model = models.Cachorro
        fields = "__all__"

class CachorroEspecialAdminForm(forms.ModelForm):
    class Meta:
        model = models.CachorroEspecial
        fields = "__all__"

class PlanoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Plano
        fields = "__all__"

class EntregaAdminForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = "__all__"

class CarrinhoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Carrinho
        fields = "__all__"

class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = "__all__"


class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm
    list_display = [
    "id",
    "user",
    "nome",
    "sobrenome",
    "email",
    "telefone",
    "areatelefone",
    "cep",
    "cpf",
    "numero",
    "complemento"    ,
    "created",
    "last_updated",
    ]
    readonly_fields = [
    "created",
    "last_updated",
    ]

class PlanoAdmin(admin.ModelAdmin):
    form = PlanoAdminForm
    list_display = [
        "nome",
        "refeicoes",
        "descricao",
        "subdescricao",
        "condicaofrete",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]

class EntregaAdmin(admin.ModelAdmin):
    form = EntregaAdminForm
    list_display = [
        "frequencia",
        "periodo",
        "dia",
        "preferencia",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]

class CachorroEspecialAdmin(admin.ModelAdmin):
    form = CachorroEspecialAdminForm
    list_display = [
        "Cachorro",
        "condicao",
        "medicamento",
        "descricao",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]




class CachorroAdmin(admin.ModelAdmin):
    form = CachorroAdminForm
    list_display = [
    "id",
    "idCliente",
    "nome",
    "sabores",
    "calculomes",
    "created",
    ]
    readonly_fields = [
    "last_updated",
    "created",
    ]

class CarrinhoAdmin(admin.ModelAdmin):
    form = CarrinhoAdminForm
    list_display = [
    "id",
    "plano",
    "status_adesao",
    "pagseguro_plano",
    "pagseguro_adesao",
    "last_updated",
    "created",
    ]
    readonly_fields = [
    "last_updated",
    "created",
    ]


class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = [
        "id",
        "idClient",
        "valor",
        "status",
        "idPlano",
        "idEntrega",
        "idDog",
        "idCarrinho",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]





admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.Plano, PlanoAdmin)
admin.site.register(models.Entrega, EntregaAdmin)
admin.site.register(models.CachorroEspecial, CachorroEspecialAdmin)
admin.site.register(models.Cachorro, CachorroAdmin)
admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.Carrinho, CarrinhoAdmin)
