from django.urls import path, include
from rest_framework import routers
from django.contrib.auth.decorators import login_required

from . import api
from . import views

from clientflow.app.views import FORMS_CACHORRO, FORMS_PEDIDO

router = routers.DefaultRouter()
router.register("CachorroEspecial", api.CachorroEspecialViewSet)
router.register("Entrega", api.EntregaViewSet)
router.register("Pedido", api.PedidoViewSet)
router.register("Plano", api.PlanoViewSet)
router.register("Cachorro", api.CachorroViewSet)
router.register("Cliente", api.ClienteViewSet)


urlpatterns = (
    path("api/v1/", include(router.urls)),

    path("PlanoFlow/<int:pk>/", views.PlanoFlow, name="clientflow_PlanoFlow"),
    path("Plano/", login_required(views.PlanoListView.as_view()), name="clientflow_Plano_list"),
    path("Plano/create/", views.PlanoCreateView.as_view(), name="clientflow_Plano_create"),
    path("Plano/update/<int:pk>/", views.PlanoUpdateView.as_view(), name="clientflow_Plano_update"),

    # path("DogClient/renovar/<int:carrinho>", views.renovarPlano, name="pg_renovarPlano"),

    path("CheckOut/<int:carrinho>", views.checkout, name="clientflow_checkout"),
    path("CheckOut/Fim/<int:carrinho>", views.fimDoFlow, name="clientflow_fimDoFlow"),
    path("NewCarrinho/", views.adicionarAoCarrinho, name="adicionar_ao_carrinho"),

    path("CachorroEspecial/", views.checkout, name="clientflow_CachorroEspecial_list"),
    path("CachorroEspecial/create/", views.CachorroEspecialCreateView.as_view(), name="clientflow_CachorroEspecial_create"),
    path("CachorroEspecial/detail/<int:pk>/", views.CachorroEspecialDetailView.as_view(), name="clientflow_CachorroEspecial_detail"),
    path("CachorroEspecial/update/<int:pk>/", views.CachorroEspecialUpdateView.as_view(), name="clientflow_CachorroEspecial_update"),

    path("EntregaFlow/<int:pedido>", views.pedidoWizard.as_view(FORMS_PEDIDO), name="clientflow_EntregaFlow"),
    path("Entrega/create/", views.EntregaCreateView.as_view(), name="clientflow_Entrega_create"),
    path("Entrega/detail/<int:pk>/", views.EntregaDetailView.as_view(), name="clientflow_Entrega_detail"),
    path("Entrega/update/<int:pk>/", views.EntregaUpdateView.as_view(), name="clientflow_Entrega_update"),

    path("PedidoFlow/<int:plano>/<int:dog>", views.PedidoFlow, name="clientflow_PedidoFlow"),
    path("DogDash/", login_required(views.dogdash), name="dogdash"),
    path("Pedido/", login_required(views.PedidoListView.as_view()), name="clientflow_Pedido_list"),
    path("Carrinho/", login_required(views.CarrinhoListView.as_view()), name="clientflow_Carrinho_list"),

    path("Pedido/create/", views.PedidoCreateView.as_view(), name="clientflow_Pedido_create"),
    path("Pedido/detail/<int:pk>/", views.PedidoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("Pedido/update/<int:pk>/", views.PedidoUpdateView.as_view(), name="clientflow_Pedido_update"),

    path("Pedido/delete/confirm/<int:pk>", views.PedidoDeleteConfirmView, name="clientflow_Pedido_delete_confirm"),
    path("Pedido/delete/<int:pk>", views.PedidoDeleteView, name="clientflow_Pedido_delete"),



    path("DogFlow/", views.cachorroWizard.as_view(FORMS_CACHORRO), name="clientflow_dogflow"),
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
    path("MinhaConta/", views.profile_view, name="user-profile"),
    path("MinhaConta/update/", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/update/<int:carrinho>", views.profile_update_view, name="user-profile-update"),
    path("MinhaConta/Novo/<int:dog>", views.profile_simple_view, name="user-profile-simple",),

)
