from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SucursalViewSet,
    UserViewSet,
    LoginView,
    PerfilView,
    DashboardGerenteApiView,
    DashboardEncargadoApiView,
    DashboardEmpleadoApiView,
    AsistenciaView,
    AsistenciasTodasView,
    EmpleadosListView,
    EmpleadoDetailView,
    EmpleadosListCreateView,
)

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'empleados', UserViewSet, basename='empleados')  # <-- línea corregida

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('dashboard/gerente/', DashboardGerenteApiView.as_view(), name='dashboard-gerente'),
    path('dashboard/encargado/', DashboardEncargadoApiView.as_view(), name='dashboard-encargado'),
    path('dashboard/empleado/', DashboardEmpleadoApiView.as_view(), name='dashboard-empleado'),
    path('asistencia/', AsistenciaView.as_view(), name='asistencia'),
    path('asistencias-todas/', AsistenciasTodasView.as_view(), name='asistencias-todas'),
]
