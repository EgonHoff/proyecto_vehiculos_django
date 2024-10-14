from django.urls import path
from .views import VehiculoFormView, ListaVehiculos

urlpatterns = [
    path('add/', VehiculoFormView.as_view(),name = 'addV'),
    path('list/', ListaVehiculos.as_view(), name='listar_vehiculos'),
]