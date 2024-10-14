# proyecto_vehiculos_django

## CONSOLIDACION M6

Estado inicial del proyecto

## Tecnologias utilizadas

- Vs-code
- GoogleChrome
- Python 3.12.4

## Creación del Entorno virtual con VirtualEnvwrapper

- Nombre entorno : proyecto_vehiculos_django
- Revisar requeriments.txt y env_log.txt para mas información

## Aplicación Vehiculo

- Utilizar comando django-admin startapp vehiculo

## Creacion del modelo vehiculo

- proyecto_vehiculos_django\vehiculo\models.py

```{python}
class Vehiculo(models.Model):
    MARCAS = [
        ('Fiat','Fiat'),
        ('Chevrolet','Chevrolet'),
        ('Ford','Ford'),
        ('Toyota','Toyota'),
    ]

    CATEGORIAS = [
        ('Particular','Particular'),
        ('Transporte','Transporte'),
        ('Carga','Carga'),
    ]

    marca = models.CharField(max_length=20,choices=MARCAS,default='Ford')
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50)
    serial_motor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20,choices=CATEGORIAS,default='Particular')
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.categoria})"
```
## Agregar a INSTALLED_APPS

-proyecto_vehiculos_django\config\settings.py
```{python}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vehiculo',  <-----
]
```
## Realizar migraciones

- py manage.py makemigrations
- py manage.py migrate

## Creacion de index.html y Formulario con sus vistas

- proyecto_vehiculos_django\vehiculo\views.py
- proyecto_vehiculos_django\vehiculo\forms.py
- proyecto_vehiculos_django\vehiculo\urls.py
- proyecto_vehiculos_django\templates\index.html
- proyecto_vehiculos_django\vehiculo\templates\vehiculo_form.html

### Rutear URLS de la app

- proyecto_vehiculos_django\config\urls.py
```{python}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('vehiculo/', include('vehiculo.urls')),
]
```
- proyecto_vehiculos_django\vehiculo\urls.py
```{python}
urlpatterns = [
    path('add/', VehiculoFormView.as_view(),name = 'addV'),
]
```

### Endpoints

- http://127.0.0.1:8000/ <------  index.html
- http://127.0.0.1:8000/vehiculo/add/ <------- vehiculo_form.html

## Agregar registros a la base de datos con el formulario

| Marca      | Modelo              | Serial Carroceria | Serial Motor | Categoría   | Precio |
|------------|---------------------|-------------------|--------------|-------------|--------|
| Fiat       | Punto               | 254AADD           | 4521475      | Particular  | 9200   |
| Fiat       | Furgoneta Ducato     | 25ED235           | 8554122      | Transporte  | 19000  |
| Ford       | F-150 Lightning      | QS41252           | 2547896      | Carga       | 22000  |
| Toyota     | 4Runner              | 34RF123           | 4587563      | Carga       | 25000  |
| Chevrolet  | Corvette             | 4TQWE5            | 2512545      | Particular  | 60000  |

## Agregar menú con Bootstrap

-proyecto_vehiculos_django\config\settings.py
```{python}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'vehiculo',
]
```
### Se crean plantillas base.html y navbar.html con bootstrap

- proyecto_vehiculos_django\templates\base.html
- proyecto_vehiculos_django\templates\navbar.html

### Se extienden a los archivos html de las vistas

```{python}
{% extends "base.html" %}
{% block content %}
{% include "navbar.html" %}
```
- agregando lo siguiente a navbar.html se logra redireccionar a las vistas de index y formulario
```{python}
<a class="nav-link active" aria-current="page" href={% url "index" %}>Inicio</a>
<a class="nav-link" href={% url "addV" %}>Agregar</a>
```

## Permiso para visualizar catálogo

```{python}
    class Meta:
        permissions = [
            ("visualizar_catalogo", "Puede visualizar Catálogo de Vehículos"),
            ("can_add_vehiculo", "Puede agregar un vehículo"),
        ]
```
## Registro nuevo usuario

- django-admin startapp users
- migraciones 
- formulario registro nuevos usuarios
- proyecto_vehiculos_django\users\views.py
```{python}
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
            permission = Permission.objects.get(codename='visualizar_catalogo') <------ PERMISO
            user.user_permissions.add(permission)                               <------ PERMISO
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        return render(request, self.template_name, {'form': form})
```
Por defecto cada vez que se registra un usuario nuevo viene con el permiso anteriormente creado de visualizar el catalogo.
- para logout
```{python}
from django.contrib.auth import logout

class LogoutPropiaView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
```
- para login de usarios se utiliza el modulo importado directo a urls.py
```{python}
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register/', RegistroUsuarioView.as_view(),name = 'addU'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutPropiaView.as_view(), name='logout'),
]
```
## Listar Vehiculos

- vista en proyecto_vehiculos_django\vehiculo\views.py
```{python}
class ListaVehiculos(ListView):
    model = Vehiculo
    template_name = 'lista_vehiculo.html'
    context_object_name = 'vehiculos'
```
- se crea proyecto_vehiculos_django\vehiculo\templates\lista_vehiculo.html
- ruteado en proyecto_vehiculos_django\vehiculo\urls.py
```{python}
urlpatterns = [
    path('add/', VehiculoFormView.as_view(),name = 'addV'),
    path('list/', ListaVehiculos.as_view(), name='listar_vehiculos'), <-----
]
```
- Con el contexto entregado en html se lista
```{html} 
        {% for vehiculo in vehiculos %}
            <tr>
                <td>{{ vehiculo.marca }}</td>
                <td>{{ vehiculo.modelo }}</td>
                <td>{{ vehiculo.serial_carroceria }}</td>
                <td>{{ vehiculo.serial_motor }}</td>
                <td>{{ vehiculo.categoria }}</td>
                <td>{{ vehiculo.precio }}</td>
                <td>
                    {% if vehiculo.precio <= 10000 %}
                        Bajo
                    {% elif vehiculo.precio > 10000 and vehiculo.precio <= 30000 %}
                        Medio
                    {% elif vehiculo.precio > 30000 %}
                        Alto
                    {% endif %}
                </td>
            </tr>
```
- En navbar.html se utiliza clausulas IF para mostrar o redirigir botones
```{html}
          {% if user.is_authenticated and 'vehiculo.can_add_vehiculo' in perms %}
          <li class="nav-item">
            <a class="nav-link" href={% url "addV" %}>Agregar</a>
          </li>
          {% endif %}
```
- Se utiliza PermissionRequiredMixin para controlar si se usan directamente los endpoints
```{python}
class ListaVehiculos(PermissionRequiredMixin,ListView):
    model = Vehiculo
    template_name = 'lista_vehiculo.html'
    context_object_name = 'vehiculos'
    permission_required = 'visualizar_catalogo'

    def handle_no_permission(self):
        return redirect(reverse('login'))
```
Con esto si alguien no autenticado intenta apretar 'Listar' sera redirigido a la pantalla de login, Igualmente si alguien conoce el endpoint y lo utiliza directamente tambien sera redireccionado a la vista de login.