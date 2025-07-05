from django.urls import path

from .views import AsistenciaView
from .views import (
    LoginView,
    PerfilView,
    DashboardGerenteApiView,
    DashboardEncargadoApiView,
    DashboardEmpleadoApiView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),

    # Dashboards protegidos por rol
    path('dashboard/gerente/', DashboardGerenteApiView.as_view(), name='dashboard-gerente'),
    path('dashboard/encargado/', DashboardEncargadoApiView.as_view(), name='dashboard-encargado'),
    path('dashboard/empleado/', DashboardEmpleadoApiView.as_view(), name='dashboard-empleado'),
]

urlpatterns += [
    path('asistencia/', AsistenciaView.as_view(), name='asistencia'),
]
