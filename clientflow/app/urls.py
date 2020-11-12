from django.urls import path, include
from rest_framework import routers
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import api
from . import views

from clientflow.app.views import FORMS_CACHORRO, FORMS_ENTREGA

router = routers.DefaultRouter()
router.register("CachorroEspecial", api.CachorroEspecialViewSet)
router.register("Entrega", api.EntregaViewSet)
router.register("Pedido", api.PedidoViewSet)
router.register("Plano", api.PlanoViewSet)
router.register("Cachorro", api.CachorroViewSet)
router.register("Cliente", api.ClienteViewSet)


urlpatterns = (
    path("api/v1/", include(router.urls)),

    path("DogFlow/", views.cachorroWizard.as_view(FORMS_CACHORRO), name="clientflow_dogflow"),
    path("PlanoFlow/<int:dog>/", views.PlanoFlow, name="clientflow_PlanoFlow"),
    path("PedidoFlow/<int:plano>/<int:dog>", views.PedidoFlow, name="clientflow_PedidoFlow"),
    path("EntregaFlow/<int:pedido>", views.entregaWizard.as_view(FORMS_ENTREGA), name="clientflow_EntregaFlow"),
    path("Carrinho/", views.CarrinhoListView.as_view(), name="clientflow_Carrinho_list"),
    path("NewCarrinho/", views.adicionarAoCarrinho, name="adicionar_ao_carrinho"),
    path("CheckOut/<int:carrinho>", views.checkout, name="clientflow_checkout"),
    path("CompraConcluida/<int:carrinho>", views.fimDoFlow, name="clientflow_fimDoFlow"),


    path("CarrinhoDetail/", views.CarrinhoListView2.as_view(), name="clientflow_Carrinho_2"),
    path("Plano/", login_required(views.PlanoListView.as_view()), name="clientflow_Plano_list"),
    path("Fatura/<int:pk>/", views.PagtoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("Pedido/", login_required(views.PedidoListView.as_view()), name="clientflow_Pedido_list"),

    path("Pedido/delete/confirm/<int:pk>", views.PedidoDeleteConfirmView, name="clientflow_Pedido_delete_confirm"),
    path("Pedido/delete/<int:pk>", views.PedidoDeleteView, name="clientflow_Pedido_delete"),

    path("Carrinho/delete/confirm/<int:pk>", views.CarrinhoDeleteConfirmView, name="clientflow_Carrinho_delete_confirm"),
    path("Carrinho/delete/<int:pk>", views.CarrinhoDeleteView, name="clientflow_Carrinho_delete"),

    path("Cachorro/", login_required(views.CachorroListView.as_view()), name="clientflow_Cachorro_list"),
    path("Cachorro/delete/confirm/<int:pk>", views.CachorroDeleteConfirmView, name="clientflow_Cachorro_delete_confirm"),
    path("Cachorro/delete/<int:pk>", views.CachorroDeleteView, name="clientflow_Cachorro_delete"),

    path("cupom/", views.testaCupom, name="cupom"),

    # path("Cadastro/", views.signup_view, name="sign-up"),
    path("DogDash/", login_required(views.dogdash), name="dogdash"),
    path("interno/", staff_member_required(views.pedidosDash), name="pedidosDash",),
    path("entregas/<int:pedido>", staff_member_required(views.entregaInterna), name="entregaInterna",),
    path("entregas/", views.calendar, name="entregas",),
    path("MinhaConta/", login_required(views.profile_view), name="user-profile"),
    path("MinhaConta/update/", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/update/<int:carrinho>", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/Novo/<int:pedido>/<int:dog>/", views.profile_simple_view, name="user-profile-simple",),

    path("MinhaConta/Especial/<int:dog>/", views.profile_cliente_especial, name="user-profile-especial",),
    path("DogEspecial/<int:dog>/", views.fimDoFlowEspecial, name="clientflow_dogespecial",),

    path("Pedido/suspender/confirm/<int:pk>", views.suspendePlanoConfirm,name="pg_suspende_confirm"),
    path("Pedido/suspender/<int:pk>", views.suspendePlano,name="pg_suspende"),
    path("Pedido/cancela/confirm/<int:pk>", views.cancelaPlanoConfirm,name="pg_cancela_confirm"),
    path("Pedido/cancela/<int:pk>", views.cancelaPlano,name="pg_cancela"),

    path("ra/", views.ra, name="ra",),
    path("ar/", views.ra, name="ar",),


    path("listateste/", views.listagemteste, name="listateste",),
    path("listateste2/", views.listagemteste2, name="listateste2",),
    path("teste/", views.viewteste, name="teste",),
)
