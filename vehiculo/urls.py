from django.urls import path
from .views import VehiculoFormView

urlpatterns = [
    path('add/', VehiculoFormView.as_view(),name = 'addV')
]