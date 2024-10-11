from django.urls import path
from django.contrib.auth.views import LoginView
from .views import RegistroUsuarioView, LogoutPropiaView


urlpatterns = [
    path('register/', RegistroUsuarioView.as_view(),name = 'addU'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutPropiaView.as_view(), name='logout'),
]