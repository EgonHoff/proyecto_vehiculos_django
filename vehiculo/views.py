from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import VehiculoForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

class VehiculoFormView(FormView):
    template_name = 'vehiculo_form.html'
    form_class = VehiculoForm

    def get_success_url(self) -> str:
        return reverse("addV")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)