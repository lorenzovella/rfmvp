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
    path("Carrinho/", login_required(views.CarrinhoListView.as_view()), name="clientflow_Carrinho_list"),
    path("NewCarrinho/", views.adicionarAoCarrinho, name="adicionar_ao_carrinho"),
    path("CheckOut/<int:carrinho>", views.checkout, name="clientflow_checkout"),
    path("CompraConcluida/<int:carrinho>", views.fimDoFlow, name="clientflow_fimDoFlow"),

    # path("DogClient/renovar/<int:carrinho>", views.renovarPlano, name="pg_renovarPlano"),

    path("CachorroEspecial/", views.checkout, name="clientflow_CachorroEspecial_list"),
    path("CachorroEspecial/create/", views.CachorroEspecialCreateView.as_view(), name="clientflow_CachorroEspecial_create"),
    path("CachorroEspecial/detail/<int:pk>/", views.CachorroEspecialDetailView.as_view(), name="clientflow_CachorroEspecial_detail"),
    path("CachorroEspecial/update/<int:pk>/", views.CachorroEspecialUpdateView.as_view(), name="clientflow_CachorroEspecial_update"),

    path("Entrega/create/", views.EntregaCreateView.as_view(), name="clientflow_Entrega_create"),
    path("Entrega/detail/<int:pk>/", views.EntregaDetailView.as_view(), name="clientflow_Entrega_detail"),
    path("Entrega/update/<int:pk>/", views.EntregaUpdateView.as_view(), name="clientflow_Entrega_update"),

    path("CarrinhoDetail/", login_required(views.CarrinhoListView2.as_view()), name="clientflow_Carrinho_2"),
    path("Pedido/", login_required(views.PedidoListView.as_view()), name="clientflow_Pedido_list"),
    path("Plano/", login_required(views.PlanoListView.as_view()), name="clientflow_Plano_list"),


    path("Pedido/create/", views.PedidoCreateView.as_view(), name="clientflow_Pedido_create"),
    # path("Pedido/detail/<int:pk>/", views.PedidoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("Fatura/<int:pk>/", views.PagtoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("Pedido/update/<int:pk>/", views.PedidoUpdateView.as_view(), name="clientflow_Pedido_update"),

    path("Pedido/delete/confirm/<int:pk>", views.PedidoDeleteConfirmView, name="clientflow_Pedido_delete_confirm"),
    path("Pedido/delete/<int:pk>", views.PedidoDeleteView, name="clientflow_Pedido_delete"),

    path("Carrinho/delete/confirm/<int:pk>", views.CarrinhoDeleteConfirmView, name="clientflow_Carrinho_delete_confirm"),
    path("Carrinho/delete/<int:pk>", views.CarrinhoDeleteView, name="clientflow_Carrinho_delete"),

    path("Cachorro/inFlow", login_required(views.CachorroListFlowView.as_view()), name="clientflow_CachorroFlow_list"),
    path("Cachorro/", login_required(views.CachorroListView.as_view()), name="clientflow_Cachorro_list"),
    path("Cachorro/delete/confirm/<int:pk>", views.CachorroDeleteConfirmView, name="clientflow_Cachorro_delete_confirm"),
    path("Cachorro/delete/<int:pk>", views.CachorroDeleteView, name="clientflow_Cachorro_delete"),
    # path("Cachorro/create/", views.CachorroCreateView.as_view(), name="clientflow_Cachorro_create"),
    path("Cachorro/detail/<int:pk>/", views.CachorroDetailView.as_view(), name="clientflow_Cachorro_detail"),
    path("Cachorro/update/<int:pk>/", views.CachorroUpdateView.as_view(), name="clientflow_Cachorro_update"),



    path("Cliente/", views.ClienteListView.as_view(), name="clientflow_Cliente_list"),
    path("Cliente/create/", views.ClienteCreateView.as_view(), name="clientflow_Cliente_create"),
    path("Cliente/detail/<int:pk>/", views.ClienteDetailView.as_view(), name="clientflow_Cliente_detail"),
    path("Cliente/update/<int:pk>/", views.ClienteUpdateView.as_view(), name="clientflow_Cliente_update"),

    # path("Cadastro/", views.signup_view, name="sign-up"),
    path("DogDash/", login_required(views.dogdash), name="dogdash"),
    path("Interno/", staff_member_required(views.pedidosDash), name="pedidosDash",),
    path("teste/", views.teste, name="teste",),
    path("MinhaConta/", login_required(views.profile_view), name="user-profile"),
    path("MinhaConta/update/", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/update/<int:carrinho>", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/Novo/<int:pedido>/<int:dog>/", views.profile_simple_view, name="user-profile-simple",),

    path("Pedido/suspender/confirm/<int:pk>", views.suspendePlanoConfirm,name="pg_suspende_confirm"),
    path("Pedido/suspender/<int:pk>", views.suspendePlano,name="pg_suspende"),
    path("Pedido/cancela/confirm/<int:pk>", views.cancelaPlanoConfirm,name="pg_cancela_confirm"),
    path("Pedido/cancela/<int:pk>", views.cancelaPlano,name="pg_cancela"),

)
