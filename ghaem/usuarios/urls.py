from django.urls import path
from .views import LoginView, PerfilView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]
