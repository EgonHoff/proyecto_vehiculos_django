# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth import logout

class RegistroUsuarioView(FormView):
    form_class = UserCreationForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            permission = Permission.objects.get(codename='visualizar_catalogo')
            user.user_permissions.add(permission)
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    

class LogoutPropiaView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


