from django.urls import path
from .views import RegistroUsuarioView, LoginView, PerfilView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]
