from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("CachorroEspecial", api.CachorroEspecialViewSet)
router.register("Entrega", api.EntregaViewSet)
router.register("Pedido", api.PedidoViewSet)
router.register("Planos", api.PlanosViewSet)
router.register("Cachorro", api.CachorroViewSet)
router.register("Cliente", api.ClienteViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("clientflow/CachorroEspecial/", views.CachorroEspecialListView.as_view(), name="clientflow_CachorroEspecial_list"),
    path("clientflow/CachorroEspecial/create/", views.CachorroEspecialCreateView.as_view(), name="clientflow_CachorroEspecial_create"),
    path("clientflow/CachorroEspecial/detail/<int:pk>/", views.CachorroEspecialDetailView.as_view(), name="clientflow_CachorroEspecial_detail"),
    path("clientflow/CachorroEspecial/update/<int:pk>/", views.CachorroEspecialUpdateView.as_view(), name="clientflow_CachorroEspecial_update"),
    path("clientflow/Entrega/", views.EntregaListView.as_view(), name="clientflow_Entrega_list"),
    path("clientflow/Entrega/create/", views.EntregaCreateView.as_view(), name="clientflow_Entrega_create"),
    path("clientflow/Entrega/detail/<int:pk>/", views.EntregaDetailView.as_view(), name="clientflow_Entrega_detail"),
    path("clientflow/Entrega/update/<int:pk>/", views.EntregaUpdateView.as_view(), name="clientflow_Entrega_update"),
    path("clientflow/Pedido/", views.PedidoListView.as_view(), name="clientflow_Pedido_list"),
    path("clientflow/Pedido/create/", views.PedidoCreateView.as_view(), name="clientflow_Pedido_create"),
    path("clientflow/Pedido/detail/<int:pk>/", views.PedidoDetailView.as_view(), name="clientflow_Pedido_detail"),
    path("clientflow/Pedido/update/<int:pk>/", views.PedidoUpdateView.as_view(), name="clientflow_Pedido_update"),
    path("clientflow/Planos/", views.PlanosListView.as_view(), name="clientflow_Planos_list"),
    path("clientflow/Planos/create/", views.PlanosCreateView.as_view(), name="clientflow_Planos_create"),
    path("clientflow/Planos/detail/<int:pk>/", views.PlanosDetailView.as_view(), name="clientflow_Planos_detail"),
    path("clientflow/Planos/update/<int:pk>/", views.PlanosUpdateView.as_view(), name="clientflow_Planos_update"),
    path("clientflow/Cachorro/", views.CachorroListView.as_view(), name="clientflow_Cachorro_list"),
    path("clientflow/Cachorro/create/", views.CachorroCreateView.as_view(), name="clientflow_Cachorro_create"),
    path("clientflow/Cachorro/detail/<int:pk>/", views.CachorroDetailView.as_view(), name="clientflow_Cachorro_detail"),
    path("clientflow/Cachorro/update/<int:pk>/", views.CachorroUpdateView.as_view(), name="clientflow_Cachorro_update"),
    path("clientflow/Cliente/", views.ClienteListView.as_view(), name="clientflow_Cliente_list"),
    path("clientflow/Cliente/create/", views.ClienteCreateView.as_view(), name="clientflow_Cliente_create"),
    path("clientflow/Cliente/detail/<int:pk>/", views.ClienteDetailView.as_view(), name="clientflow_Cliente_detail"),
    path("clientflow/Cliente/update/<int:pk>/", views.ClienteUpdateView.as_view(), name="clientflow_Cliente_update"),
)
