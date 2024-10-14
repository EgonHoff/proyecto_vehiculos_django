from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import VehiculoForm
from .models import Vehiculo

# Create your views here.

def index(request):
    return render(request, 'index.html')

class VehiculoFormView(PermissionRequiredMixin,FormView):
    template_name = 'vehiculo_form.html'
    form_class = VehiculoForm

    permission_required = 'vehiculo.can_add_vehiculo'

    def get_success_url(self) -> str:
        return reverse("addV")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def handle_no_permission(self):
        return redirect(reverse('index'))

class ListaVehiculos(PermissionRequiredMixin,ListView):
    model = Vehiculo
    template_name = 'lista_vehiculo.html'
    context_object_name = 'vehiculos'
    permission_required = 'visualizar_catalogo'

    def handle_no_permission(self):
        return redirect(reverse('login'))