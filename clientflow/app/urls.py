from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

from clientflow.app.views import FORMS_CACHORRO

router = routers.DefaultRouter()
router.register("CachorroEspecial", api.CachorroEspecialViewSet)
router.register("Entrega", api.EntregaViewSet)
router.register("Pedido", api.PedidoViewSet)
router.register("Plano", api.PlanoViewSet)
router.register("Cachorro", api.CachorroViewSet)
router.register("Cliente", api.ClienteViewSet)


urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("CachorroEspecial/", views.CachorroEspecialListView.as_view(), name="clientflow_CachorroEspecial_list"),
    path("CachorroEspecial/create/", views.CachorroEspecialCreateView.as_view(), name="clientflow_CachorroEspecial_create"),
    path("CachorroEspecial/detail/<int:pk>/", views.CachorroEspecialDetailView.as_view(), name="clientflow_CachorroEspecial_detail"),
    path("CachorroEspecial/update/<int:pk>/", views.CachorroEspecialUpdateView.as_view(), name="clientflow_CachorroEspecial_update"),

    path("Entrega/", views.EntregaListView.as_view(), name="clientflow_Entrega_list"),
    path("Entrega/create/", views.EntregaCreateView.as_view(), name="clientflow_Entrega_create"),
    path("Entrega/detail/<int:pk>/", views.EntregaDetailView.as_view(), name="clientflow_Entrega_detail"),
    path("Entrega/update/<int:pk>/", views.EntregaUpdateView.as_view(), name="clientflow_Entrega_update"),

    path("Pedido/", views.PedidoListView.as_view(), name="clientflow_Pedido_list"),
    path("Pedido/create/", views.PedidoCreateView.as_view(), name="clientflow_Pedido_create"),
    path("Pedido/detail/<int:pk>/", views.PedidoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("Pedido/update/<int:pk>/", views.PedidoUpdateView.as_view(), name="clientflow_Pedido_update"),

    path("Plano/", views.PlanoListView.as_view(), name="clientflow_Plano_list"),
    path("Plano/create/", views.PlanoCreateView.as_view(), name="clientflow_Plano_create"),
    path("PlanoFlow/<int:pk>/", views.PlanoFlow, name="clientflow_PlanoFlow"),
    path("Plano/update/<int:pk>/", views.PlanoUpdateView.as_view(), name="clientflow_Plano_update"),

    path("Cachorro/", views.CachorroListView.as_view(), name="clientflow_Cachorro_list"),
    # path("Cachorro/create/", views.CachorroCreateView.as_view(), name="clientflow_Cachorro_create"),
    path("Cachorro/delete/confirm/<int:pk>", views.CachorroDeleteConfirmView, name="clientflow_Cachorro_delete_confirm"),
    path("Cachorro/delete/<int:pk>", views.CachorroDeleteView, name="clientflow_Cachorro_delete"),
    path("Cachorro/detail/<int:pk>/", views.CachorroDetailView.as_view(), name="clientflow_Cachorro_detail"),
    path("Cachorro/update/<int:pk>/", views.CachorroUpdateView.as_view(), name="clientflow_Cachorro_update"),

    path("Cliente/", views.ClienteListView.as_view(), name="clientflow_Cliente_list"),
    path("Cliente/create/", views.ClienteCreateView.as_view(), name="clientflow_Cliente_create"),
    path("Cliente/detail/<int:pk>/", views.ClienteDetailView.as_view(), name="clientflow_Cliente_detail"),
    path("Cliente/update/<int:pk>/", views.ClienteUpdateView.as_view(), name="clientflow_Cliente_update"),

    path("DogFlow/", views.cachorroWizard.as_view(FORMS_CACHORRO), name="clientflow_dogflow"),

)
